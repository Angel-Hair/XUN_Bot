import requests
from lxml import etree
import time
import feedparser
from urllib import parse

from kth_timeoutdecorator import *
from xunbot import get_bot

from ...xlog import xlogger

TIMELIMIT_ANIME = get_bot().config.TIMELIMIT_ANIME
MAXINFO_ANIME = get_bot().config.MAXINFO_ANIME


async def from_anime_get_info(key_word: str) -> str:
    repass = ""
    url = 'https://share.dmhy.org/topics/rss/rss.xml?keyword=' + parse.quote(key_word)
    try:
        xlogger.debug("Now starting get the {}".format(url))
        repass = await get_repass(url)
    except TimeoutException as e:
        xlogger.error("Timeout! {}".format(e))
    
    return repass


@timeout(TIMELIMIT_ANIME)
async def get_repass(url: str) -> str:
    repass = ""
    putline = []

    d = feedparser.parse(url)
    url_list = [e.link for e in d.entries]

    if len(url_list) > MAXINFO_ANIME:
        url_list = url_list[:MAXINFO_ANIME]

    for u in url_list:
        html_data = requests.get(u)
        html = etree.HTML(html_data.text)
        
        magent = html.xpath('.//a[@id="a_magnet"]/text()')[0]
        title = html.xpath('.//h3/text()')[0]
        item = html.xpath('//div[@class="info resource-info right"]/ul/li')
        class_a = item[0].xpath('string(.)')[5:].strip().replace("\xa0","").replace("\t","")
        size = item[3].xpath('string(.)')[5:].strip()
        
        putline.append("【{}】| {}\n【{}】| {}".format(class_a, title, size, magent))
    
    repass = '\n\n'.join(putline)

    return repass