from nonebot.default_config import *

HOST = '0.0.0.0'
PORT = 8080

NICKNAME = {'小寻', 'XUN', '小尋'}

COMMAND_START = {'', '/', '!', '／', '！'}

SUPERUSERS = {123456} # 管理员（你）的QQ号

# ————————以下是部分功能模块需要的额外配置，请参见github上的说明进行配置————————

# KEY类
SAUCENAO_KEY = "" # SauceNAO 的 API key | 类型为str
BAIDUAPPID_TRANSL = "" # Baidu翻译 的 APP ID | 类型为str
BAIDUKEY_TRANSL = "" # Baidu翻译 的 SecretKey | 类型为str

# Max/Min类
EM = 4.0 # 地震速报功能的最低震级 | 类型为float
MAXINFO_REIMU = 3 # 上车功能查找目的地的最大数 | 类型为int>0
MAXINFO_ANIME = 4 # 搜番功能查找番剧的最大数 | 类型为int>0
MAXLINE_JD = 7 # 日语词典功能查找条目的内容所允许的最大行书 | 类型为int>0
MAXWOED_JD = 300 # 日语词典功能查找条目的内容所允许的最大字数 | 类型为int>0

# TimeLimit类
TIMELIMIT_IMAGE = 7 # 识图功能的时间限制 | 类型为float
TIMELIMIT_REIMU = 12 # 上车功能的时间限制 | 类型为float
TIMELIMIT_JD = 7 # 日语词典功能的时间限制 | 类型为float
TIMELIMIT_TRANSL = 7 # 翻译功能的时间限制 | 类型为float
TIMELIMIT_ANIME = 7 # 搜番功能的时间限制 | 类型为float

# Bool类
CEICONLYCN = True # 是否只报道国内地震 | 类型为bool
RECOMMENDER_MUSIC = False # 音乐推荐功能的回复是否显示推荐者 | 类型为bool
PLAYLIST_MUSIC = True # 音乐推荐功能的回复是否显示来源歌单 | 类型为bool
MORE_COMPLEX = False # 是否提供更加复杂的计算库 | 类型为bool

# 其他
CALCULATE_LIST = {
    'numpy':'np',
    'math':'',
    'scipy':''
    } # 需要提供的计算库名与可选的别名(仅在MORE_COMPLEX为真时有效) | 类型为dict
TO_TRANSL = "zh-CN" # 指定翻译功能的目标语言 | 类型为str

# —————————————————————————————————————————————————————————————————————————