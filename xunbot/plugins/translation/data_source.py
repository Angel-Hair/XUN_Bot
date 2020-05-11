import http.client
import hashlib
import urllib
import random
import json

from googletrans import Translator
from kth_timeoutdecorator import *

from xunbot import get_bot
from ...xlog import xlogger

TIMELIMIT_TRANSL = get_bot().config.TIMELIMIT_TRANSL
BAIDUAPPID_TRANSL = get_bot().config.BAIDUAPPID_TRANSL
BAIDUKEY_TRANSL = get_bot().config.BAIDUKEY_TRANSL
TO_TRANSL = get_bot().config.TO_TRANSL


def baidu_translator(content: str, appid: str, secretKey: str, fromLang: "str = 'auto'", toLang: "str = 'zh'") -> str:
    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)
    q= content
    sign = appid + q + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
    salt) + '&sign=' + sign

    try:
        httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        result_all = response.read().decode("utf-8")
        result = json.loads(result_all)

        return result['trans_result'][0]['dst']
    except Exception as e:
        xlogger.error(e)
    finally:
        if httpClient:
            httpClient.close()


@timeout(TIMELIMIT_TRANSL)
async def get_transl_of_content(content: str) -> str:
    transl_d = {}
    google_translator = Translator()
    xlogger.info("Loading Google translation")
    transl_d['Google 翻译'] = google_translator.translate(content, dest = TO_TRANSL).text

    if BAIDUAPPID_TRANSL and BAIDUKEY_TRANSL:
        xlogger.info("Loading Baidu translation")
        transl_d['Baidu 翻译'] = baidu_translator(content, BAIDUAPPID_TRANSL, BAIDUKEY_TRANSL, 'auto', TO_TRANSL[:2])

    repass = ""
    putline = []
    for k in transl_d.keys():
        td = transl_d[k]
        if td:
            putline.append("【{}】\n> {}".format(k, td))
        else:
            xlogger.error("[ERROR] {} service returned empty.".format(k))
    repass = "\n".join(putline)

    return repass