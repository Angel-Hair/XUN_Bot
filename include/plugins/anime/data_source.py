import requests
from lxml import etree
import sys
import time

sys.path.append('../../../')
from config import TIMELIMIT_ANIME, MAXINFO_ANIME
from kth_timeoutdecorator import *

async def from_anime_get_info(key_word: str) -> str:
    repass = ""
    url = 'https://share.dmhy.org/topics/list?keyword=' + key_word
    try:
        print("[info]Now starting get the {}".format(url))
        repass = await get_repass(url)
    except TimeoutException as e:
        print("[warning] {}".format(e))
    
    return repass

@timeout(TIMELIMIT_ANIME)
async def get_repass(url: str) -> str:
    repass = ""
    putline = []

    html_data = requests.get(url)
    html = etree.HTML(html_data.text)
    
    anime_list = html.xpath('//div[@class="clear"]/table/tbody/tr')
    if len(anime_list) > MAXINFO_ANIME:
        anime_list = anime_list[:MAXINFO_ANIME]
    
    for anime in anime_list:
        class_a = anime.xpath('./td[@width="6%"]//font/text()')[0]
        title = anime.xpath('./td[@class="title"]/a')[0].xpath('string(.)').strip()
        magent_long = anime.xpath('./td/a[@class="download-arrow arrow-magnet"]/@href')[0]
        magent = magent_long[:magent_long.find('&')]
        size = anime.xpath('./td[last()-4]/text()')[0]

        putline.append("【{}】| {}\n【{}】| {}".format(class_a, title, size, magent))
    
    repass = '\n\n'.join(putline)

    return repass