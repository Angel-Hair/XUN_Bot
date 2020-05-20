<div align="center">

# XUN_Langskip

[![GitHub](https://img.shields.io/github/license/Angel-Hair/XUN_Bot)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
[![QQ 群](https://img.shields.io/badge/qq%E7%BE%A4-nb%E7%BE%A4%E6%88%91%E5%9C%A8%E9%87%8C%E9%9D%A2-green)](https://jq.qq.com/?_wv=1027&k=5OFifDh)
![Code Name](https://img.shields.io/badge/%E5%BC%80%E5%8F%91%E4%BB%A3%E5%8F%B7-Langskip-9cf)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/Angel-Hair/XUN_Bot)

XUN 是一个基于 [NoneBot](https://github.com/richardchien/nonebot) 和 [酷Q](https://cqp.cc) 的功能型QQ机器人，目前提供了音乐点播、音乐推荐、天气查询、RSSHub订阅、使用帮助、识图、识番、搜番、上车、磁力搜索、地震速报、计算、日语词典、翻译、自我检查，权限等级功能，由于是为了完成自己在群里的承诺，一时兴起才做的，所以写得比较粗糙，大家见谅。

</div>

## 功能说明

<details>
<summary><mark> 点击展开功能说明</mark></summary>

### 使用帮助

![14.png](https://i.loli.net/2020/05/11/XyjdrLvspH7wQSF.png)
![15.png](https://i.loli.net/2020/05/11/WrVMNAfEc9DuxyG.png)

用于查询功能列表和功能的食用帮助。*部分简单的功能没有实例。*

不带参数时返回功能列表，带参数时返回对应功能的食用说明，**注意参数不区分大小写**。

### 自我检查

![12.png](https://i.loli.net/2020/04/24/NkiQBzbreF5ESuR.png)
![13.png](https://i.loli.net/2020/04/24/u2Ikdzop4Xcn3ZS.png)

管理员目前唯一有特权的功能（~~枯了，管理员地位堪比清洁工~~

非管理员调用此功能只会得到一个简单的回复，而管理员则会得到一个完整服务器状态检查表。

另外，在群聊中，非管理员进行自检时如果发现危险，会有对应的回应并@任意一位管理员，然后向所有管理员发送一个包含完整服务器状态检查表的通知（如上图所示）。*若`SUPERUSERS`的值未填写，则不会有以上反应。*

### 识图

![1.png](https://i.loli.net/2020/01/04/FtiUZnSTPmCz3hJ.png)

此功能整合了以前的 SauceNAO 和 ascii2d 两个功能，主要针对ACG图像和推图，本来打算加入各主流搜索引擎识图功能的，但是发现并没用公开API，如果对接 Selenium 倒是可以实现，但是未免有点浪费资源，所以就没继续写了……

> XUN: 其实就是懒……

*由于功能中采用了 SauceNAO 提供的服务，如果需要使用识图功能，需要你先去 [SauceNAO](https://saucenao.com/) 申请一个API key，并修改 `config.py` 中 `SAUCENAO_KEY` 的值。*

**需要注意的是加入了超时机制，如果 SauceNAO 和 ascii2d 其中一个在检索的时候超时则不会有对应的结果！如果需要修改超时时间，需要修改 `config.py` 中的对应值， 详细配置请参考上面 [配置](#user-content-配置) 这一节的内容。**

### 计算

![2.png](https://i.loli.net/2020/03/28/sS8XPAm1yKpQJYf.png)

任何使用 Python 来计算的公式都可以使用此功能来计算，**但要注意你所需要的计算结果一定要赋值给名为 `END` (注意大小写)的变量，也就是说如果你只发送命令 `1+1` 是不会有任何结果，正确的命令为 `END=1+1` 。另外如果你需要得到更多变量的值，则一定不要命令任何变量为`END`，在这种情况下，默认会回复一个包含计算过程所有变量的值空间字典。**

看到这里聪明的你可能已经猜出来了，这个功能的原理就是利用Python中的 `exec` 函数来实现的，不过不用担心安全审计问题，在执行`exec`函数前会自动调用相应的审计函数来进行检查，如果检查出可能会损害服务器的命令会进行相应的报错，并不会执行其命令。**欢迎大家找出安全审计的漏洞并提出，我尽量会在第一时间内修复的。**

**!!!出于安全考虑，该功能在7.0-beta版本之后移除了__import__模块，任何用于计算的被信任的库需要被单独写入 `CALCULATE_LIST` 的值当中来引入，请注意正确配置 `MORE_COMPLEX` 和 `CALCULATE_LIST` 这两项，详细配置请参考上面 [配置](#user-content-配置) 这一节的内容。!!!**

### 音乐点播

![3.png](https://i.loli.net/2020/01/04/jqALO8ZvXmzfx6h.png)

这个基本的功能相信不用我更多的介绍了吧，**需要注意的是音乐名用《》括起来或者使用标准格式: 命令+空格，另外使用 歌名-歌手 的格式可以使结果更准确。**

### 音乐推荐

![4.png](https://i.loli.net/2020/01/04/bs9deW4gLmXPcAC.png)

输入 `对应命令 + 你需要音乐的描述` 就可以得到推荐音乐的回复，其中包含该歌曲所被包含歌单的信息。

### 识番(原搜番功能)

![5.png](https://i.loli.net/2020/01/04/9nPh3kQM7cbz4rE.png)

该功能利用了![trace.moe](https://trace.moe/)公共API，会得到对应图片的番剧名称和时间锚点。

**！注意，此功能原名为 搜番 ，在8.8-beta版本后被正式更名为 识番 ！**

### 搜番

![11.png](https://i.loli.net/2020/04/16/6cml3THnrEkpvSR.png)

修改 `config.py` 中的 `MAXINFO_ANIME` 此值，可以更改回复时返回的资源数目，详细配置请参考上面 [配置](#user-content-配置) 这一节的内容。

*与识番功能搭配食用，味道更佳~*

### 天气查询

![6.png](https://i.loli.net/2020/01/04/Sd7FZkI2w5n9c4b.png)

命令中包含‘小寻’和‘天气’这两个关键字和一个地名就可以得到对应地名的天气了。**注意只能查询国内的天气。**

### 地震速报

![7.png](https://i.loli.net/2020/01/04/rjl3mY7M4NodIct.png)

被动技能，不需要主动调用。默认情况下只会报道发生在国内的地震并且要求震级大于等于4.0，如果需要报道周边国家的地震或者需要修改最低震级，需要修改 `config.py` 中的对应值，详细配置请参考上面 [配置](#user-content-配置) 这一节的内容。

**注意启用该功能会每隔一分钟检索一次 [国家地震台网](http://news.ceic.ac.cn/) ,比较消耗资源，如果不需要启用该功能，只需要在 `\plugins\` 目录下删掉对应 `ceic` 文件夹并重启XUN就可以了。**

### 日语词典

![9.png](https://i.loli.net/2020/03/28/SG7fdCcPRMxmuDt.png)

此功能没有启用 `自然语言处理器` 模块，所以请用 `标准命令格式 + 查询单词` 的形式来使用，将会得到对应单词的部分词典释义。**过长或者行数过多的释义段将会被省略，并给出提示。**

**应提灯喵汉化组所需做的功能，如果不需要该功能，只需要在 `\plugins\` 目录下删掉对应 `japanese_dictionary` 文件夹并重启XUN就可以了。**

### 翻译

![10.png](https://i.loli.net/2020/03/30/JZ3Un1wSmAyHDl8.png)

翻译功能可以自动识别源语言，默认目标语言为中文，如要更改可修改 `config.py` 中 `TO_TRANSL` 的值，**由于采用了 百度翻译开放平台 提供的服务，需要你先去 [百度翻译开放平台](http://api.fanyi.baidu.com/) 申请一个APP ID 和 密钥，并修改 `BAIDUKEY_TRANSL` 和 `BAIDUAPPID_TRANSL` 的值。** 详细配置请参考上面 [配置](#user-content-配置) 这一节的内容。

### RSSHub订阅

![16.png](https://i.loli.net/2020/05/11/jYOKsrZVwzebBoG.png)

需要对接 [RSSHub](https://docs.rsshub.app/) 进行食用的功能，将你的RSSHub域名填入 `config.py` 中的 `RSSHUBAPP` 对应值，默认的更新时间为1小时检查一次，如果需要调整，需要修改 `config.py` 中的 `RSSINTERVAL` ，注意该值是作为 `scheduled_job` 的的参数传入的，如果不知道怎么修改，请参考 [官方说明](https://apscheduler.readthedocs.io/en/latest/modules/triggers/interval.html?highlight=interval#module-apscheduler.triggers.interval)，不建议设置为10分钟以下。**订阅列表保存在根目录下的 `rss.csv` 文件里**。

确认订阅前会分别进行一次路由测试(检查该路由是否能够正确连通)和上限检查(检查是否已经达到订阅上限)，失败的话并不会订阅。

另外群订阅只能由管理员、群主或者群管理员通过群聊添加和修改，讨论组订阅只能由管理员订阅，而个人订阅只需要私聊即可。

### 磁力搜索

![17.png](https://i.loli.net/2020/05/20/zVJUjPbCo13nXcv.png)

默认检索时按相似度排序，如果需要按更新时间排序，需要在关键词前加入 ` -U `  参数(不区分大小写，但注意前后空格)

修改 `config.py` 中的 `MAXINFO_BT` 此值，可以更改回复时返回的资源数目，详细配置请参考上面 [配置](#user-content-配置) 这一节的内容。

**关于此功能我不会再有过多的描述了，请自行体会。**

### 上车(已暂停更新，使用时可能会出现报错或者无反应)

![8.png](https://i.loli.net/2020/01/16/J5NSW2BfbjMK6VZ.png)

注意此功能没有启用 `自然语言处理器` 模块，所以请用 `标准命令格式 + 目的地关键词` 的形式来告诉XUN你想要去的目的地。

*7.6-beta版本后加入了通过输入关键词 `最近的存档` 来查看最新的投稿的选项*

**关于此功能我不会再有过多的描述了，请自行体会。**

</details>
<br>

## 部署

由于XUN基于 [NoneBot](https://github.com/richardchien/nonebot) 和 [酷Q](https://cqp.cc)，所以在使用前需要了解这两个的基本食用方法：

* [NoneBot官方手册](https://nonebot.cqp.moe)
* [酷Q](https://cqp.cc)

```bash
# 克隆代码
git clone https://github.com/Angel-Hair/XUN_Bot.git
cd XUN_Bot

# 创建虚拟环境
python -m venv venv
.\venv\Scripts\activate # Windows
source ./venv/bin/activate # Linux

# 安装依赖
pip install -r requirements.txt

# 运行
python bot.py
```

## 权限等级列表

序号为等级值，由下至上兼容，等级值越大，权限等级越底，权限管理越松。

1. SUPERUSER :最高等级、管理员级
2. PRIVATE_FRIEND :好友级
3. GROUP_OWNER :群主级
4. GROUP_ADMIN :群管理级
5. GROUP_MEMBER :群员级
6. PRIVATE_GROUP :群私聊级
7. DISCUSS :讨论组级
8. PRIVATE_DISCUSS :讨论组私聊级
9. PRIVATE_OTHER :其它私聊级
10. EVERYBODY :最低等级、无限级

**注意XUN的权限管理和NoneBot的不一样，只需要设置 `PERMISSION_LEVEL` 的值，XUN的权限管理虽然基于NoneBot的权限声明，但差别很大，因为xun的权限等级是由下至上完全兼容的，也就是说如果设置为讨论组级，那么包括群私聊、群员一直到管理员，对这些人的功能使用权都会开放！另外，不建议将等级值设置为8以下。**

## 配置

### 快速配置

首先备份根目录下面的 `config.py` 文件，下面将对 `config.py` 中的一些比较重要的值进行说明，**需要注意如果只是修改这部分的值，并不能获得更好的体验**，这部分的内容是给希望能够快速上线体验功能的人准备的（~~指逃课~~，如果不希望快速上线，建议阅读下面的 [详细配置](#user-content-详细配置) 这一节的内容。

#### 1、`SUPERUSERS`

> SUPERUSERS = {123456} # 管理员（你）的QQ号

设置为管理员权限的QQ号，可填写多个，类型为Set，虽然目前设置有管理员特权的功能只有自检功能，能设还是尽量多射几个。

#### 2、`SAUCENAO_KEY` & `BAIDUAPPID_TRANSL` & `BAIDUKEY_TRANSL`

> SAUCENAO_KEY = "" # SauceNAO 的 API key | 类型为str  
> BAIDUAPPID_TRANSL = "" # Baidu翻译 的 APP ID | 类型为str  
> BAIDUKEY_TRANSL = "" # Baidu翻译 的 SecretKey | 类型为str  

你需要去单独申请的这几个API key，链接我就放这儿了，自己去申请吧。

* [百度翻译开放平台](http://api.fanyi.baidu.com/)
* [SauceNAO](https://saucenao.com/)

*当然也可以不填写，但会影响部分功能的效果，比如Baidu的kay没填的话，翻译功能就只会提供Google的部分；而如果SauceNAO的key没填的话，识图功能就只会提供ascii2d的部分。*

#### 3、RSSHub的对接

> RSSHUBAPP = "https://rsshub.app" # RSSHub自部署的域名

RSSHub订阅功能需要对接你自己部署的RSSHub服务器，关于如何部署RSSHub，请参考[RSSHub主页](https://docs.rsshub.app/)。

**注意，不设置的话则完全无法使用RSSHub订阅功能，但定时器又会定时检查更新，平白消耗资源，如果确定不需要此功能，只需要在 `\plugins\` 目录下删掉对应 `rss` 文件夹并重启XUN就可以了。**

*另外之所以不把地震通报功能设计为对接该功能订阅国家地震台网的模式，是为了方便和我一样RSSHub在墙外的用户（海外节点无法正常访问一些网站）。*

#### 4、你需要地震通报功能吗

> \plugins\ceic

因为启用 地震通报 功能会每隔一分钟检索一次 [国家地震台网](http://news.ceic.ac.cn/) ，会比较消耗网络资源，请确认你的服务器是否能够负担得起网络资源的消耗，如果不需要启用该功能，只需要在 `\plugins\` 目录下删掉对应 `ceic` 文件夹并重启XUN就可以了。另外该功能并不能当作地震**速**报来用，不仅是因为其自身的延迟，本身地震台网延迟就比较大的。

### 详细配置

<details>
<summary><mark> 点击展开详细配置</mark></summary>


修改 `config.py` 中的以下字段，填入对应值(注意备份):

```python
# ……省略的代码……

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
# —————————————————————————————————————————————————————————————————————————
```

对应的说明：

* NoneBot类
  * `SUPERUSERS` ：管理员的QQ号，也就是你的QQ号，虽然目前还没有为管理员设置更多的权限服务，以后会计划开发的……另外，此字段为NoneBot自带配置字段，更多的说明可以参见NoneBot中对此字段的[描述](https://nonebot.cqp.moe/guide/basic-configuration.html#%E9%85%8D%E7%BD%AE%E8%B6%85%E7%BA%A7%E7%94%A8%E6%88%B7)。
* Permission类
  * `PERMISSION_LEVEL` ：权限等级值，请参考 [权限等级列表](#user-content-权限等级列表) 进行配置，**建议不要设置为8以下**。
* KEY类
  * `SAUCENAO_KEY` ：在 识图 功能中采用了 SauceNAO 提供的服务，如果需要使用识图功能，需要你先去 [SauceNAO](https://saucenao.com/) 申请一个API key。
  * `BAIDUAPPID_TRANSL` ：在 翻译 功能中采用了 百度翻译开放平台 提供的服务，如果需要使用翻译功能，需要你先去 [百度翻译开放平台](http://api.fanyi.baidu.com/) 申请一个APP ID 和 密钥。
  * `BAIDUKEY_TRANSL` ：在 翻译 功能中采用了 百度翻译开放平台 提供的服务，如果需要使用翻译功能，需要你先去 [百度翻译开放平台](http://api.fanyi.baidu.com/) 申请一个APP ID 和 密钥。
  * `RSSHUBAPP` ：在 RSSHub订阅 功能中需要对接部署的RSSHub域名，如果需要使用RSSHub订阅功能，需要你自己部署RSSHub服务，部署方法参考 [RSSHub主页](https://docs.rsshub.app/)。
* Max/Min类
  * `EM` ：设置 地震速报 功能中的通报的最低震级，只有震级大于等于该值才会被报道。推荐设置为4.0。
  * `MAXINFO_REIMU` ：在 上车 功能中配置查找的目的地的数量限制，最多只能显示指定数量的目的地，推荐设置为3，**注意此项会影响`TIMELIMIT_REIMU`的配置**，一般每增加1就需要`TIMELIMIT_REIMU`至少增加1.5。
  * `MAXINFO_ANIME` ：在 搜番 功能中配置查找的资源的数量限制，最多只能显示指定数量的番剧数，推荐设置为4。
  * `MAXINFO_BT` ：在 磁力搜索 功能中配置查找的资源的数量限制，最多只能显示指定数量的资源数，推荐设置为4。
  * `MAXLINE_JD` ：在 日文词典 功能中查找条目的内容所允许的最大行书，超过该条数的内容将被省略，并报出提示。
  * `MAXWOED_JD` ：在 日文词典 功能查找条目的内容所允许的最大字数，超过该字数的内容将被省略，并报出提示。
  * `MAX_PERFORMANCE_PERCENT` :  在 自我检查 功能中的服务器占用比率最高值，需填入长度为3的list，根据顺序分别对应CPU、内存和硬盘的最大占有率，如果超过该值，在群聊中，进行自检时会有对应的回应，并向所有管理员发送通知。
  * `MAX_RSS_P`&`MAX_RSS_G`&`MAX_RSS_D` ：在 RSSHub订阅 功能中分别对应私人、群、讨论组的订阅数最大值，超过该值则不会完成订阅，并报出提示。
* TimeLimit类
  * `TIMELIMIT_IMAGE` ：在 识图 功能中设置的时间限制，单位为(s)，如果检索某个API来源时超时的话，会在控制台报出相应的警告，在回复中则不会有对应的内容。请根据服务器的网络环境自行设置，推荐设置在5~10之间。
  * `TIMELIMIT_JD` ：在 日文词典 功能中设置的时间限制，单位为(s)，详细介绍同上。
  * `TIMELIMIT_TRANSL` ：在 翻译 功能中设置的时间限制，单位为(s)，详细介绍同上。
  * `TIMELIMIT_ANIME` ： 在 搜番 功能中设置的时间限制，单位为(s)，详细介绍同上。
  * `TIMELIMIT_REIMU` ：在 上车 功能中设置的时间限制，单位为(s)，如果检索某个API来源时超时的话，会在控制台报出相应的警告，在回复中则不会有对应的内容。请根据服务器的网络环境和`MAXINFO_REIMU`的值自行设置，推荐设置在9~14之间。
* Bool类
  * `CEICONLYCN` ：在 地震速报 功能中是否只报道国内地震，如果只需要报道国内地震请设置为True。推荐设置为True。
  * `RECOMMENDER_MUSIC` ：在 音乐推荐 功能中是否需要回复显示推荐者。
  * `PLAYLIST_MUSIC` ：在 音乐推荐 功能中是否需要回复显示来源歌单。
  * `MORE_COMPLEX` ：在 计算 功能中是否需要引入更加用于复杂计算的库(如numpy、math等)，否则将只能计算最基本的公式。
* 其他
  * `CALCULATE_LIST` ：在 计算 功能中需要引入的计算库名与可选的别名，类型为dict，键为库名，值为别名。**此项仅在`MORE_COMPLEX`为真时有效，需要注意被引入的库应该已被正确安装在机器上，且能够被执行环境所引用！**
  * `PROCESS_NAME_LIST` ：在 自我检查 功能中需要提供的格外检查的进程名，如果发现同名的进程中至少有一个进程的状态不是"running"的时候，在群聊中，进行自检时会有对应的回应，并向所有管理员发送通知。
  * `TO_TRANSL` : 在 翻译 功能中指定翻译的目标语言，默认为中文，其他语言的列表请参考 [百度翻译开发者手册](http://api.fanyi.baidu.com/doc/21) 和 [Googletrans](https://github.com/ssut/py-googletrans)
  * `RSSINTERVAL` : 在 RSSHub订阅 功能中检查订阅列表更新的时间间隔，每个时间键的值类型应该为int，默认值的意思为每隔1小时检测一次，如果想设置为每半小时检查一次，应该注释掉`hour`行，取消`minutes`行的注释，并把对应值`0`改为`30`。不建议设置为10分钟以下。该值其实是作为 `scheduled_job` 的的参数传入的，详细说明参考 [官方说明](https://apscheduler.readthedocs.io/en/latest/modules/triggers/interval.html?highlight=interval#module-apscheduler.triggers.interval)。

</details>
<br>

## 食用方法

由于部分功能都导入了 NoneBot 的 `自然语言处理器` 模块，所以这些功能含有命令的关键词就可以随意地调教XUN了~

### 基本用法[注意空格]

>@XUN [命令] ……  
>XUN [命令] ……  
>小寻 [命令] ……  

### 使用帮助

XUN 在 alpha1.0 版本后加入了使用帮助功能，其中包含更加详细的帮助和实例，以下是其食用方法：

1、查询功能列表
  >小寻 help

2、查询功能使用帮助
  >小寻 help [功能名称]

## 计划功能

除了上面功能说明中提到的完善计划，还将计划加入以下功能:

* 开发框架
* 游戏战绩查询
* ~~骚话~~ 嘴臭

> XUN: ~~有生之年~~ 史 诗 巨 坑  
> AH: 下属不许啵上司嘴！

## alpha阶段的庆祝

为了庆祝小寻终于一步步升级到alpha阶段，我特地来采访下群主SK：

> AH: xun要升级到alpha版本了  
> AH: 我来采访下你  
> AH: 有什么想法没有？  

> SK: 识图快了吗(恶臭表情)  

> AH: 哈？  
> AH: 我问你想法呢，没让你提你的屑建议  
 
> SK: 那……  
> SK: 我想看小寻的色图  

> AH: 太屑了  
> AH: 给爷爬  

## 开源许可证

本项目使用 [LGPLv3](https://github.com/Angel-Hair/XUN_Bot/blob/master/LICENSE) 许可证，由于本项目的特殊性，本项目的源码中出现在 NoneBot 文档的部分（例如作为其示例代码），不使用 LGPLv3 许可，而使用和 NoneBot 一样的 MIT 许可。
