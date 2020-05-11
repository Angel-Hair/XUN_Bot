import json
import requests
from os import path
from random import choice

import thulac

from xunbot import get_bot
from ...hanziconv import HanziConv
from ...xlog import xlogger

RECOMMENDER_MUSIC = get_bot().config.RECOMMENDER_MUSIC
PLAYLIST_MUSIC = get_bot().config.PLAYLIST_MUSIC


async def get_recommend(music_command: str):
    music_command = HanziConv.toSimplified(music_command)
    xlogger.debug("Start fetching keywords……")
    keywords = []
    user_words_path = path.join(path.dirname(__file__), "user_words.txt")
    user_words = []
    with open(user_words_path,'r', encoding='UTF-8') as f:
        for line in f:
            usr = str(line.strip('\n'))
            if usr.lower() in music_command.lower():
                keywords.append(usr.lower())
            user_words.append(usr)

    thu1 = thulac.thulac()
    words = thu1.cut(music_command)
    
    for word in words:
        if (word[0].lower() not in keywords) and ((word[1] in ['a', 't', 'np', 'id', 'i']) or (word[1] == 'v'  and (word[0] not in ['推荐', '来', '听', '着']))):
            keywords.append(word[0])

    inline = "+".join(keywords)

    return inline

def getzhuanji(url: str, headers: dict):
    xlogger.debug("Start getting album information: {}".format(url))
    zhuanji = dict()
    gedan_data = requests.get(url, headers=headers).text
    gedan_json = json.loads(gedan_data, strict=False)
    zj = choice(gedan_json['result']['playlists'])
    zhuanji['zj_id'] = zj['id']
    zhuanji['zj_name'] = zj['name'].strip()
    zhuanji['zj_creator'] = zj['creator']['nickname'].strip()

    return zhuanji

def getmusic(url: str, headers: dict):
    xlogger.debug("Start getting music information: {}".format(url))
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

async def get_song_of_music(keywords: str):
    xlogger.info("KEYWORDS: {}".format(keywords))
    repass = ""
    infot = []

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

    if RECOMMENDER_MUSIC: infot.append("[推荐者]@" + zhuanji['zj_creator'])
    if PLAYLIST_MUSIC: infot.append("[来自163歌单]" + zhuanji['zj_name'])

    return repass, infot