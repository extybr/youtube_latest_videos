import sys
import os
import subprocess
import re
import time

RED = '\033[31m'
BLUE = '\033[36m'
YELLOW = '\033[033m'
DEFAULT = '\033[0m'


def get_list_link(urls):
    pattern1 = (r'"accessibility":{"accessibilityData":{"label":".+"}}},'
                r'"descriptionSnippet"')
    pattern2 = r'"descriptionSnippet"'
    pattern3 = r'"url":"/watch.+",'
    pattern4 = r'","webPageType":"WEB_PAGE_TYPE_WATCH"'
    
    while urls:
        try:
            name, url = urls.pop(0)
            curl = f'curl -s --location --max-time 5 {url}'
            html = subprocess.getoutput(curl)
            sample1 = re.compile(pattern1)
            title1 = sample1.search(html)
            sample2 = re.compile(pattern2)
            title2 = sample2.search(html)
            sample3 = re.compile(pattern3)
            title3 = sample3.search(html)
            sample4 = re.compile(pattern4)
            title4 = sample4.search(html)
            
            if title1 and title2 and title3 and title4:
                title = html[title1.start() + 47:title2.start() - 5]
                print(f'{RED}{name}{DEFAULT}: {BLUE}{title}{DEFAULT}')
                link = html[title3.start() + 13:title4.start()]
                print(f'{YELLOW}https://www.youtube.com/watch{link}{DEFAULT}\n')
            else:
                urls.insert(0, (name, url))
                get_list_link(urls)
        except Exception as error:
            print(f'{RED}{str(error)}{DEFAULT}\n')

        if urls:
            time.sleep(3)


def get_urls(start_file_name=''):
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
    return urls


if __name__ == "__main__":
    urls = []
    file_name = ''
    if len(sys.argv) == 2:
        if sys.argv[1].startswith('https://'):
            urls = [('channel', sys.argv[1])]
        else:
            get_urls(sys.argv[1])
    else:
        get_urls()
    get_list_link(urls)
