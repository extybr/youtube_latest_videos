##############################
#  Example: (without proxy)  #
# $> python rss.py           #
# $> python rss.py g         #
##############################

import sys
import os
import feedparser
from typing import List, Tuple

red = '\033[31m'
blue = '\033[36m'
yellow = '\033[33m'
normal = '\033[0m'

Data = Tuple[str, str]
Data_array = List[Data]


def get_latest_videos_from_rss(_channel_id: str, number_videos=5) -> Data_array:
    rss_url = (f'https://www.youtube.com/feeds/videos.xml?'
               f'channel_id={_channel_id}')
    feed = feedparser.parse(rss_url)

    _videos = []
    for entry in feed.entries[:number_videos]:
        _title = entry.title
        _url = entry.link
        _videos.append((_title, _url))

    return _videos


def get_urls(start_file_name='') -> Data_array:
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
            _name, _id = '', ''
            for line in text:
                if line.startswith('name='):
                    _name = line.strip()[5:]
                elif line.startswith('id='):
                    _id = line.strip()[3:]
                    _ids = (_name, _id)
                    if _ids not in urls:
                        urls.append((_name, _id))

    return urls


if __name__ == '__main__':
    urls = []
    try:
        if len(sys.argv) == 2:
            get_urls(sys.argv[1])
        else:
            get_urls()
        for name, channel_id in urls:
            videos = get_latest_videos_from_rss(channel_id)
            print(f' {red}{name}{normal} '.center(50, '*'))
            print()
            for title, url in videos:
                print(f'{blue}{title}{normal}\n{yellow}{url}{normal}\n')
    except KeyboardInterrupt:
        print(' exit! bye ... bye ...')
