import json
import requests

async def get_anime(anime: str) -> str:
    response = requests.get('https://trace.moe/api/search?url={}'.format(anime))
    anime_json = json.loads(response.text)

    repass = ""
    for anime in anime_json["docs"][:3]:
        anime_name = anime["anime"]
        episode = anime["episode"]
        at = int(anime["at"])
        m, s = divmod(at, 60)
        similarity = anime["similarity"]

        putline = "[ {} ][{:0>2d}][{}:{}] 相似度:{:.2%}".format(anime_name, episode, m, s, similarity)
        if repass:
            repass = "\n".join([repass, putline])
        else:
            repass = putline

    return repass