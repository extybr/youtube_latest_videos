#######################
#  Example:           #
# $> python rss.py    #
# $> python rss.py g  #
#######################

import sys
import os
import feedparser

red = '\033[31m'
blue = '\033[36m'
yellow = '\033[33m'
normal = '\033[0m'


def get_latest_videos_from_rss(channel_id: str, num_videos=5) -> list:
    rss_url = (f"https://www.youtube.com/feeds/videos.xml?"
               f"channel_id={channel_id}")
    feed = feedparser.parse(rss_url)
    
    videos = []
    for entry in feed.entries[:num_videos]:
        title = entry.title
        url = entry.link
        videos.append((title, url))
    
    return videos


def get_urls(start_file_name='') -> list:
    files = []
    for file in os.listdir():
        if start_file_name:
            if file.startswith(start_file_name) and file.endswith('.txt'):
                files.append(file)
        else:
            if file.endswith('.txt'):
                files.append(file)
    
    for file_name in files:
        with open(file_name, 'r', encoding='utf-8') as text:
            name, _id = '', ''
            for line in text:
                if line.startswith('name='):
                    name = line.strip()[5:]
                elif line.startswith('id='):
                    _id = line.strip()[3:]
                    _ids = (name, _id)
                    if _ids not in urls:
                        urls.append((name, _id))

    return urls


if __name__ == "__main__":
    urls = []
    if len(sys.argv) == 2:
        get_urls(sys.argv[1])
    else:
        get_urls()
    for name, channel_id in urls:
        videos = get_latest_videos_from_rss(channel_id)
        print(f' {red}{name}{normal} '.center(50, '*') + '\n')
        for title, url in videos:
            print(f"{blue}{title}{normal}\n{yellow}{url}{normal}\n")
