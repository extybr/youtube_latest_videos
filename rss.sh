#!/bin/bash

# example:
# $> ./rss.sh channels.txt

red='\033[31m'
green='\033[32m'
blue='\033[36m'
yellow='\033[033m'
normal='\033[0m'

PROXY=$(cat ./proxy)

if [ $# -ne 1 ]; then
  echo -e "${red}1 parameter was expected, but $# were passed${normal}"
  exit 0
fi

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
    html=$(curl -s --location $PROXY --max-time 7 "${CHANNEL_URL}")
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

# Получение последних видео
result=$(get_latest_videos_from_html | head -n "${NUM_VIDEOS}")

# Вывод последнего видео
echo "${result}" | sed -n "1p" | while IFS='|' read -r title url; do
    printf "${yellow}%s${normal}" "*********************  "
    echo -en "${red}${title}${normal}"
    printf "${yellow}%s${normal}\\n" "  *********************"
    echo -e "${blue}${url}${normal}"
    printf "${yellow}%s${normal}\\n\\n" "********************************************************"
done

# Вывод предпоследнего видео
echo "${result}" | sed -n "2p" | while IFS='|' read -r title url; do
    echo -e "${red}${title}${normal}"
    echo -e "${blue}${url}${normal}"
    echo
done

# Вывод последних видео
echo "${result}" | sed -n "3,+${NUM_VIDEOS}p" | while IFS='|' read -r title url; do
    echo -e "${green}${title}${normal}"
    echo -e "${blue}${url}${normal}"
    echo
done

done
