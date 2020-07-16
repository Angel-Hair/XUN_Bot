import requests
from urllib import parse
from html import unescape
from lxml import etree
from lxml.etree import Element

from xunbot import get_bot
from ...xlog import xlogger

MAXINFO_BT = get_bot().config.MAXINFO_BT


header = {
    "Host": "www.btmet.xyz",
    "Connection": "keep-alive",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0",
    "Accept-Language":"zh-CN,zh;"
}

cookiesDit = {
    'r18':'0'
}

async def get_bt_info(url: str) -> str:
    xlogger.info("Now starting get the {}".format(url))
    html_data = requests.get(url, headers=header, cookies=cookiesDit)
    html = etree.HTML(html_data.text)

    num = html.xpath('//div[@id="wall"]//span/b/text()')[0]
    if num == '0':
        return "没有找到记录"

    div_all = html.xpath('//div[@class="search-item"]')[1:]
    div_all = div_all[:MAXINFO_BT] if len(div_all) > MAXINFO_BT else div_all
    line_list = [await get_item_line(div) for div in div_all]
    
    return "\n\n".join(line_list)

async def get_item_line(div: Element) -> str:
    magent = div.xpath('./div[@class="f_right"]/a/@href')[0]
    size = div.xpath('./div[@class="f_left"]/div[@class="item-bar"]/span/b/font/text()')[0]
    type = div.xpath('./div[@class="f_left"]/div[@class="item-bar"]/span[@class="cpill blue-pill"]/text()')[0].strip()

    title_doc = div.xpath('.//a[@class="smashTitle"]//text()')[0]
    title_code = title_doc[title_doc.find('("')+2 : title_doc.find('")')]
    title_xml_code = parse.unquote(title_code)
    title_xml = etree.HTML(unescape(title_xml_code))
    title = title_xml.xpath('string(.)')

    return "【{}】| {}\n【{}】| {}".format(type, title, size, magent)