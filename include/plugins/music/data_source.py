import json
import requests

async def get_song_of_music(music: str) -> str:
    url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?aggr=1&cr=1&flag_qc=0&p=1&n=1&w=' + music
    data_text = requests.get(url).text
    data_json = json.loads(data_text[9:-1])
    songid = data_json["data"]["song"]["list"][0]["songid"]
    repass = "[CQ:music,type=qq,id=" + str(songid) + "]"
    print(repass)

    return repass