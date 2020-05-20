from typing import List, Dict, Set

from nonebot.default_config import *

HOST = '0.0.0.0'
PORT = 8080

NICKNAME = {'XUN', '小寻', '小尋'}

COMMAND_START = {'', '/', '!', '／', '！'}

SUPERUSERS = {123456} # 管理员（你）的QQ号


# ————————以下是部分功能模块需要的额外配置，请参见github上的说明进行配置————————

# Permission类
PERMISSION_LEVEL: int = 6 # 权限等级值，建议不要设置为8以下

# KEY类
SAUCENAO_KEY: str = "" # SauceNAO 的 API key
BAIDUAPPID_TRANSL: str = "" # Baidu翻译 的 APP ID
BAIDUKEY_TRANSL: str = "" # Baidu翻译 的 SecretKey
RSSHUBAPP:str = "https://rsshub.app" # RSSHub自部署的域名

# Max/Min类
EM :float = 4.0 # 地震速报功能的最低震级
MAXINFO_REIMU: int = 3 # 上车功能查找目的地的最大数
MAXINFO_ANIME: int = 4 # 搜番功能查找番剧的最大数
MAXINFO_BT: int = 4 # 磁力搜索功能查找资源的最大数
MAXLINE_JD: int = 7 # 日语词典功能查找条目的内容所允许的最大行书
MAXWOED_JD: int = 250 # 日语词典功能查找条目的内容所允许的最大字数
MAX_PERFORMANCE_PERCENT: List[int] = [92,92,92] # 自检功能中的服务器占用比率最高值，顺序分别对应CPU、内存和硬盘
MAX_RSS_P: int = 2
MAX_RSS_G: int = 5
MAX_RSS_D: int = 5 # 以上三个分别为RSS订阅功能的个人(private)、群(group)、讨论组(discuss)订阅的最大订阅数限制

# TimeLimit类
TIMELIMIT_IMAGE: float = 7 # 识图功能的时间限制
TIMELIMIT_REIMU: float = 12 # 上车功能的时间限制
TIMELIMIT_JD: float = 7 # 日语词典功能的时间限制
TIMELIMIT_TRANSL: float = 7 # 翻译功能的时间限制
TIMELIMIT_ANIME: float = 7 # 搜番功能的时间限制

# Bool类
CONFIGURATION_WIZARD: bool = True # 设置每次运行时是否需要确认运行配置向导
XDEBUG: bool = True # 日志是否输出DEBUG
BUILTIN_PLUGINS = True # 是否加载nonebot的默认插件
CEICONLYCN: bool = True # 是否只报道国内地震
RECOMMENDER_MUSIC: bool = False # 音乐推荐功能的回复是否显示推荐者
PLAYLIST_MUSIC: bool = True # 音乐推荐功能的回复是否显示来源歌单
MORE_COMPLEX: bool = False # 是否提供更加复杂的计算库

# 其他
CALCULATE_LIST: Dict[str, str] = {
    'numpy':'np',
    'math':'',
    'scipy':''
    } # 就按功能种需要提供的计算库名与可选的别名(仅在MORE_COMPLEX为真时有效)
PROCESS_NAME_LIST: Set[str] = {} # 自检功能种需要提供的格外检查的进程名
TO_TRANSL: str = "zh-CN" # 翻译功能中指定翻译功能的目标语言
RSSINTERVAL: dict = {
    # 'weeks': 0, 
    # 'days': 0, 
    'hours': 1, 
    # 'minutes': 0, 
    # 'second': 0
    } 
    # RSS订阅功能的检查间隔, 作为 scheduled_job 的的参数传入，默认值的意思为每隔1小时检测一次。
    # 详细配置参考：https://apscheduler.readthedocs.io/en/latest/modules/triggers/interval.html?highlight=interval#module-apscheduler.triggers.interval

# —————————————————————————————————————————————————————————————————————————