import http.client
import hashlib
import urllib
import random
import json
import sys

from googletrans import Translator
from pydeeplator.deepL import DeepLTranslator
from pydeeplator.deepL import TranslateLanguageEnum, TranslateModeType

sys.path.append('../../../')
from config import TIMELIMIT_TRANSL, BAIDUAPPID_TRANSL, BAIDUKEY_TRANSL, TO_TRANSL
from kth_timeoutdecorator import *


def deepl_translator(content: str) -> str:
    result = DeepLTranslator(
        translate_str=content,
        target_lang=TranslateLanguageEnum.ZH,
        translate_mode=TranslateModeType.SENTENCES,
    ).translate()

    return result['result']


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
        print (e)
    finally:
        if httpClient:
            httpClient.close()


@timeout(TIMELIMIT_TRANSL)
async def get_transl_of_content(content: str) -> str:
    transl_d = {}
    google_translator = Translator()

    transl_d['Google 翻译'] = google_translator.translate(content, dest = TO_TRANSL).text
    transl_d['Baidu 翻译'] = baidu_translator(content, BAIDUAPPID_TRANSL, BAIDUKEY_TRANSL, 'auto', TO_TRANSL[:2])
    if TO_TRANSL[:2] == 'zh':
        transl_d['DeepL 翻译'] = deepl_translator(content)

    repass = ""
    putline = []
    for k in transl_d.keys():
        td = transl_d[k]
        if td:
            putline.append("【{}】\n> {}".format(k, td))
        else:
            print("[ERROR] {} service returned empty.".format(k))
    repass = "\n".join(putline)

    return repass