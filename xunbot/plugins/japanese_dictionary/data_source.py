from lxml import etree
import requests
import re

from kth_timeoutdecorator import *

from ...xlog import xlogger
from xunbot import get_bot

TIMELIMIT_JD = get_bot().config.TIMELIMIT_JD
MAXLINE_JD = get_bot().config.MAXLINE_JD
MAXWOED_JD = get_bot().config.MAXWOED_JD


@timeout(TIMELIMIT_JD)
async def get_definition_of_word(word: str) -> str:
    is_hidden = False
    url = 'https://www.weblio.jp/content/' + word
    xlogger.debug("[info] Now get definition from: {}".format(url))
    html_data = requests.get(url)
    html = etree.HTML(html_data.text)

    notfound = html.xpath('//div[@id="nrCntTH"]/p/text()')
    if notfound:
        return notfound[0]

    source = html.xpath('//div[@class="pbarTL"]')
    definition = []
    d_html = html.xpath('//div[@class="kiji"]')
    for d in d_html:
        definition.append(d.xpath('string(.)').replace("  ","\n").replace("\n\n","\n").strip())
    
    repass = ""
    putline = []
    for s, d in zip(source, definition):
        line_is_hidden = False
        d = d.replace("\n ", "\n")
        pattern_1 = re.compile(r'(document.write)(.*)(\);)')
        pattern_2 = re.compile(r'(\n出典)(.*)(\))')
        d = pattern_1.sub(r'', d)
        d = pattern_2.sub(r'', d)
        d = re.sub(r'\n.\n', "\n", d)
        line_num = d.count("\n")
        if line_num > MAXLINE_JD:
            is_hidden = True
            line_is_hidden = True
            index = 0
            for i in range(MAXLINE_JD):
                index = d.find("\n", index+1)
            d = d[:index].strip()
        if len(d) > MAXWOED_JD:
            is_hidden = True
            line_is_hidden = True
            d = d[:MAXWOED_JD].strip()
        if line_is_hidden:
            d += "……\n[Note]……有内容被省略……"
        putline.append("【{}】\n{}".format(s.xpath('string(.)').strip(),d))
    repass = "\n\n".join(putline)
    if is_hidden:
        repass += "\n\n[Note]有条目过长被省略，更多释义请参考: {}".format(url)

    return repass