import requests
import math

async def get_r6smessage_of_username(username: str) -> str: 
    result = r6s_result(username)

    if result:
        ranks = ''
        if not result['rank_kd'] == 'Undefined':
            ranks = '【排名战】\n > KD:{}\n > 胜负比:{}\n > 游戏场数:{}\n'.\
                format(result['rank_kd'],result['rank_wl'],result['rank_played'])

        mmrs = ''
        if not result['mmr_list'] == 'Undefined':
            mmrs += '【排名战段位】\n > 区域\t赛季\t最终MMR\t最高MMR\n'
            for i,rank in enumerate(result['mmr_list']):
                mmrs += ' > ' + rank['region'] + '\t' + \
                    rank['season'] + '\t' + rank['mmr'] + '\t' + rank['max_mmr']
                if not i == len(result['mmr_list']) - 1:
                    mmrs += '\n'
        
        repass = ' > 等级:{}\n【综合数据】\n > KD:{}\n > 胜负比:{}\n > 游戏场数:{}\n > 爆头击杀率:{}\n{}{}'.\
            format(result['apac_level'],result['kd'],result['wl'],result['played'],result['kh'],ranks,mmrs)

        return repass
    else:
        return f"用户「{username}」未找到"

def r6s_result(username: str) -> dict:
    base_url = "https://www.r6s.cn/Stats?username="
    url = base_url + str(username) + '&platform='
    headers = {
        'Host': 'www.r6s.cn',
        'referer': 'https://www.r6s.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    response = requests.get(url,headers = headers)
    r6_json = response.json()
    if r6_json:
        apac_level = r6_json['Basicstat'][0]['level']
        # 综合
        kd = r6_json['StatGeneral'][0]['kills']/r6_json['StatGeneral'][0]['deaths']
        kh = r6_json['StatGeneral'][0]['headshot']/r6_json['StatGeneral'][0]['kills']
        wl = r6_json['StatGeneral'][0]['won']/r6_json['StatGeneral'][0]['lost']
        played = r6_json['StatGeneral'][0]['played']
        
        # 排位
        if len(r6_json['StatCR']) > 1:
            rank_kd = r6_json['StatCR'][1]['kills']/r6_json['StatCR'][1]['deaths']
            rank_wl = r6_json['StatCR'][1]['won']/r6_json['StatCR'][1]['lost']
            rank_played = r6_json['StatCR'][1]['played']

            # 亚服排名
            mmr_list = []
            for rank in r6_json['SeasonRanks']:
                rank_dict = {}
                rank_dict['region'] = str(rank['region'].upper())
                rank_dict['season'] = 'Y' + str(math.floor(rank['season']/3)) + \
                    'S' + str(4 if rank['season']%4 == 0 else rank['season']%4)
                rank_dict['mmr'] = str(round(rank['mmr']))
                rank_dict['max_mmr'] = str(round(rank['max_mmr']))

                mmr_list.append(rank_dict)

        result = {
            'apac_level':str(apac_level),
            'kd':str(round(kd,2)),
            'kh':str(round(kh,2)),
            'wl':str(round(wl,2)),
            'played':str(played),
            'rank_kd':str(round(rank_kd,2)) if 'rank_kd' in vars() else 'Undefined',
            'rank_wl':str(round(rank_wl,2)) if 'rank_wl' in vars() else 'Undefined',
            'rank_played':str(rank_played) if 'rank_played' in vars() else 'Undefined',
            'mmr_list':mmr_list if 'mmr_list' in vars() else 'Undefined'
            }

    else:
        result = {}

    return result