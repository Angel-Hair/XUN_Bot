import json
import requests

from ...xlog import xlogger


async def get_anime(anime: str) -> str:
    url = 'https://trace.moe/api/search?url={}'.format(anime)
    xlogger.debug("[info]Now starting get the {}".format(url))
    response = requests.get(url)
    anime_json = json.loads(response.text)
    if anime_json == 'Error reading imagenull': return "图像源错误，注意必须是静态图片哦"

    repass = ""
    for anime in anime_json["docs"][:3]:
        anime_name = anime["anime"]
        episode = anime["episode"]
        at = int(anime["at"])
        m, s = divmod(at, 60)
        similarity = anime["similarity"]

        putline = "[ {} ][{}][{}:{}] 相似度:{:.2%}".format(anime_name, episode if episode else '?', m, s, similarity)
        if repass:
            repass = "\n".join([repass, putline])
        else:
            repass = putline

    return repass