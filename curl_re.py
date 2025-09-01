#################################################################
#  Example:                                                     #
# $> python curl_re.py                                          #
# $> python curl_re.py g                                        #
# $> python curl_re.py https://www.youtube.com/@tseries/videos  #
#################################################################

import sys
import os
import subprocess
import re
import time

RED = '\033[31m'
BLUE = '\033[36m'
YELLOW = '\033[033m'
DEFAULT = '\033[0m'


def get_list_link() -> None:
    start_title = (r'"accessibility":{"accessibilityData":{"label":".+"}}},'
                   r'"descriptionSnippet"')
    end_title = r'"descriptionSnippet"'
    start_link = r'"url":"/watch.+",'
    end_link = r'","webPageType":"WEB_PAGE_TYPE_WATCH"'

    while urls:
        try:
            name, url = urls.pop(0)
            curl = f'curl -s --location {PROXY} --max-time 7 {url}'
            html = subprocess.getoutput(curl)
            result_start_title = re.compile(start_title)
            sample_start_title = result_start_title.search(html)
            result_end_title = re.compile(end_title)
            sample_end_title = result_end_title.search(html)
            result_start_link = re.compile(start_link)
            sample_start_link = result_start_link.search(html)
            result_end_link = re.compile(end_link)
            sample_end_link = result_end_link.search(html)

            sample_title = sample_start_title and sample_end_title
            sample_link = sample_start_link and sample_end_link
            if sample_title and sample_link:
                title = html[sample_start_title.start() + 47:
                             sample_end_title.start() - 5]
                print(f'{RED}{name}{DEFAULT}: {BLUE}{title}{DEFAULT}')
                link = html[sample_start_link.start() + 13:
                            sample_end_link.start()]
                print(f'{YELLOW}https://www.youtube.com/watch{link}{DEFAULT}\n')
            else:
                urls.insert(0, (name, url))
                get_list_link()
        except Exception as error:
            print(f'{RED}{str(error)}{DEFAULT}\n')

        if urls:
            time.sleep(3)


def get_urls(start_file_name='') -> None:
    global urls
    files = []
    for file in os.listdir():
        if start_file_name:
            if file.startswith(start_file_name) and file.endswith('.txt'):
                files.append(file)
        else:
            if file.endswith('.txt'):
                files.append(file)

    for file_name in files:
        with open(file_name, 'r', encoding='utf8') as text:
            name, url = '', ''
            for line in text:
                if line.startswith('name='):
                    name = line.strip()[5:]
                elif line.startswith('url='):
                    url = line.strip()[4:]
                    urls.append((name, url))


if __name__ == '__main__':
    if os.uname()[0] == 'Linux':
        PROXY = subprocess.getoutput('cat proxy')
    urls = []
    try:
        if len(sys.argv) == 2:
            if sys.argv[1].startswith('https://'):
                urls = [('channel', sys.argv[1])]
            else:
                get_urls(start_file_name=sys.argv[1])
        else:
            get_urls()
        get_list_link()
    except KeyboardInterrupt:
        print(' exit! bye ... bye ...')
