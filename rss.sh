#!/bin/bash
#./rss.sh channels.txt

red='\033[31m'
green='\033[32m'
blue='\033[36m'
normal='\033[0m'

# Получаем список каналов
ids=$(cat "$1" | grep -oP 'id=[^=]+' | sed 's/id=//g')

# Итерируемся по списку с id-каналами
for id in ${ids}
do

# URL страницы канала
CHANNEL_URL="https://www.youtube.com/feeds/videos.xml?channel_id=${id}"

# Количество последних видео для получения
NUM_VIDEOS=5

# Функция загрузки HTML-страницы
get_html() {
    html=$(curl -s --location --max-time 3 "${CHANNEL_URL}")
}

# Функция для получения последних видео из HTML-страницы
get_latest_videos_from_html() {
    # Загружаем HTML страницу канала
    if get_html; then

    # Извлекаем названия и ссылки на видео
    titles=$(echo -e "${html}" | grep -oP '<title>[^<]+' | sed 's/<title>//g')
    urls=$(echo -e "${html}" | grep -oP '<link rel="alternate" href="[^"]+' | sed 's/<link rel="alternate" href="//g')

    # Соединяем названия и ссылки на видео
    paste -d'|' <(echo "${titles}") <(echo "${urls}")
    else get_latest_videos_from_html
    fi
}

# Получение и вывод последних видео
get_latest_videos_from_html | head -n "${NUM_VIDEOS}" | while IFS='|' read -r title url; do
    echo -e "${green}${title}${normal}"
    echo -e "${blue}${url}${normal}"
    echo
done

done
