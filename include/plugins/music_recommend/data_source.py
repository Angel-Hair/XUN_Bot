import json
import requests
from random import choice

def getzhuanji(url: str, headers: dict):
    zhuanji = dict()
    gedan_data = requests.get(url, headers=headers).text
    gedan_json = json.loads(gedan_data, strict=False)
    zj = choice(gedan_json['result']['playlists'])
    zhuanji['zj_id'] = zj['id']
    zhuanji['zj_name'] = zj['name'].strip()
    zhuanji['zj_creator'] = zj['creator']['nickname'].strip()

    return zhuanji

def getmusic(url: str, headers: dict):
    music = dict()
    musics_data = requests.get(url, headers=headers).text
    musics_json = json.loads(musics_data, strict=False)
    msc = choice(musics_json['result']['tracks'])
    music['music_name'] = msc['name'].strip()
    music['music_artists'] = msc['artists'][0]['name'].strip()

    return music

def getalldata(keywords):

    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0'

    # 首先随机获取指定专辑
    url1 = 'http://music.163.com/api/search/get/web?s={}&type=1000&limit=3'.format(keywords)
    zhuanji = getzhuanji(url1, headers)

    # 然后随机获取专辑中的音乐
    url2 = 'http://music.163.com/api/playlist/detail?id={}'.format(zhuanji['zj_id'])
    music = getmusic(url2, headers)

    return zhuanji, music

async def get_song_of_music(keywords: str) -> str:

    print("[info]KEYWORDS:", keywords)

    if not keywords:
        return "", "意向分析失败:("

    zhuanji, music = getalldata(keywords)
    n = 0
    while(not music['music_name']):
        if n == 3:
            return "", "[ERROR]Not found music name"
        zhuanji, music = getalldata(keywords)
        n+=1
    
    url3 = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p=1&n=1&w=' + "-".join([music['music_name'], music['music_artists']])
    data_text = requests.get(url3).text
    data_json = json.loads(data_text[9:-1])
    songid = data_json["data"]["song"]["list"][0]["songid"]
    repass = "[CQ:music,type=qq,id=" + str(songid) + "]"
    # infot = "[推荐者: " + zhuanji['zj_creator'] + " ;来源歌单: " + zhuanji['zj_name'] + "]"
    infot = "[来自163歌单]" + zhuanji['zj_name']

    return repass, infot