# XUN_beta6.6

## 介绍

XUN 是一个基于 [NoneBot](https://github.com/richardchien/nonebot) 和 [酷Q](https://cqp.cc) 的功能性QQ机器人，目前提供了点播、音乐推荐、天气查询、识图、搜番、上车、地震速报功能，由于是为了完成自己在群里的承诺，一时兴起才做的，所以写得比较粗糙，大家见谅。

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
python run.py
```

## 配置

修改 `config.py` 中的以下字段，填入对应值(注意备份):

```python
# ……省略的代码……

SUPERUSERS = {123456} # 管理员（你）的QQ号

# ————————以下是部分功能模块需要的额外配置，请参见github上的说明进行配置————————

SAUCENAO_KEY = "" # SauceNAO 的 API key | 类型为str
EM = 4.0 # 地震速报功能的最低震级 | 类型为float
CEICONLYCN = True # 是否只报道国内地震 | 类型为bool
RECOMMENDER_MUSIC = False # 音乐推荐功能的回复是否显示推荐者 | 类型为bool
PLAYLIST_MUSIC = True # 音乐推荐功能的回复是否显示来源歌单 | 类型为bool
MAXINFO_REIMU = 3 # 上车功能查找目的地的最大数 | 类型为int(>0)
TIMELIMIT_IMAGE = 7 # 识图功能的时间限制 | 类型为float
TIMELIMIT_REIMU = 12 # 上车功能的时间限制 | 类型为float

# —————————————————————————————————————————————————————————————————————————
```

对应的说明：

* `SUPERUSERS` ：管理员的QQ号，也就是你的QQ号，虽然目前还没有为管理员设置更多的权限服务，以后会计划开发的……另外，此字段为NoneBot自带配置字段，更多的说明可以参见NoneBot中对此字段的[描述](https://nonebot.cqp.moe/guide/basic-configuration.html#%E9%85%8D%E7%BD%AE%E8%B6%85%E7%BA%A7%E7%94%A8%E6%88%B7)。
* `SAUCENAO_KEY` ：在 识图 功能中采用了 SauceNAO 提供的服务，如果需要使用识图功能，需要你先去 [SauceNAO](https://saucenao.com/) 申请一个API key。
* `EM` ：设置 地震速报 功能中的通报的最低震级，只有震级大于等于该值才会被报道。推荐设置为4.0。
* `CEICONLYCN` ：在 地震速报 功能中是否只报道国内地震，如果只需要报道国内地震请设置为True。推荐设置为True。
* `RECOMMENDER_MUSIC` ：在 音乐推荐 功能中是否需要回复显示推荐者。
* `PLAYLIST_MUSIC` ：在 音乐推荐 功能中是否需要回复显示来源歌单。
* `MAXINFO_REIMU` ：在 上车 功能中配置查找的目的地的数量限制，最多只能显示指定数量的目的地，推荐设置为3，**注意此项会影响`TIMELIMIT_REIMU`的配置**，一般每增加1就需要`TIMELIMIT_REIMU`至少增加1.5。
* `TIMELIMIT_IMAGE` ：在 识图 功能中设置的时间限制，单位为(s)，如果检索某个API来源时超时的话，会在控制台报出相应的警告，在回复中则不会有对应的内容。请根据服务器的网络环境自行设置，推荐设置在5~10之间。
* `TIMELIMIT_REIMU` ：在 上车 功能中设置的时间限制，单位为(s)，如果检索某个API来源时超时的话，会在控制台报出相应的警告，在回复中则不会有对应的内容。请根据服务器的网络环境和`MAXINFO_REIMU`的值自行设置，推荐设置在9~14之间。

## 食用方法

由于大部分功能都导入了 NoneBot 的 `自然语言处理器` 模块，所以基本上含有命令的关键词就可以随意地调教XUN了~

### 标准用法[注意空格]

>@XUN [命令] ……  
>XUN [命令] ……  
>小寻 [命令] ……  

### 各功能对应的命令[注意一个功能可能对应多个命令]:

* 计算: '计算', 'exp' [可使用任何基于python的语法，但要注意结果变量一定要命令为"END"]
* 天气查询：'天气', '天气预报', '查天气'
* 识图：'image', '搜图', '识图' [已整SauceNAO和ascii2d功能]
* 识番剧: 'whatanime', '搜番', '识番'
* 上车：'reimu', '上车', '查找资源'
* 音乐点播：'音乐', '点播', '来首', '给朕来首' [注意音乐名用《》或者标准格式 命令+空格，使用 歌名-歌手 可以更准确]
* 音乐推荐：'推荐音乐', '音乐推荐', '推荐一首'
* 地震速报(被动技能)：误差±10分钟

## 功能说明

<details>
<summary><mark>点击展开功能说明</mark></summary>

### 识图

![1.png](https://i.loli.net/2020/01/04/FtiUZnSTPmCz3hJ.png)

此功能整合了以前的 SauceNAO 和 ascii2d 两个功能，主要针对ACG图像和推图，本来打算加入各主流搜索引擎识图功能的，但是发现并没用公开API，如果对接 Selenium 倒是可以实现，但是未免有点浪费资源，所以就没继续写了……

> XUN: 其实就是懒……

**需要注意的是加入了超时机制，如果 SauceNAO 和 ascii2d 其中一个在检索的时候超时则不会有对应的结果！如果需要修改超时时间，需要修改 `config.py` 中的对应值， 详细配置请参考上面 [配置](#user-content-配置) 这一节的内容。**

### 计算

![2.png](https://i.loli.net/2020/01/05/4h8uvrM5tkGQxPs.png)

任何使用 Python 来计算的公式都可以使用此功能来计算，**但要注意你所需要的计算结果一定要赋值给名为 `END` 的变量，也就是说如果你只发送命令 `1+1` 是不会有任何结果，正确的命令为 `END=1+1` 。另外如果你需要得到更多变量的值，则一定不要命令任何变量为`END`，在这种情况下，默认会回复一个包含计算过程所有变量的值空间字典。**

看到这里聪明的你可能已经猜出来了，这个功能的原理就是利用Python中的 `exec` 函数来实现的，不过不用担心安全审计问题，在执行`exec`函数前会自动调用相应的审计函数来进行检查，如果检查出可能会损害服务器的命令会进行相应的报错，并不会执行其命令。

### 音乐点播

![3.png](https://i.loli.net/2020/01/04/jqALO8ZvXmzfx6h.png)

这个基本的功能相信不用我更多的介绍了吧，**需要注意的是音乐名用《》括起来或者使用标准格式: 命令+空格，另外使用 歌名-歌手 的格式可以使结果更准确。**

### 音乐推荐

![4.png](https://i.loli.net/2020/01/04/bs9deW4gLmXPcAC.png)

输入 `对应命令 + 你需要音乐的描述` 就可以得到推荐音乐的回复，其中包含该歌曲所被包含歌单的信息。

### 搜番

![5.png](https://i.loli.net/2020/01/04/9nPh3kQM7cbz4rE.png)

该功能利用了![trace.moe](https://trace.moe/)公共API，会得到对应图片的番剧名称和时间锚点。

### 天气查询

![6.png](https://i.loli.net/2020/01/04/Sd7FZkI2w5n9c4b.png)

命令中包含‘小寻’和‘天气’这两个关键字和一个地名就可以得到对应地名的天气了。**注意只能查询国内的天气。**

### 地震速报

![7.png](https://i.loli.net/2020/01/04/rjl3mY7M4NodIct.png)

被动技能，不需要主动调用。默认情况下只会报道发生在国内的地震并且要求震级大于等于4.0，如果需要报道周边国家的地震或者需要修改最低震级，需要修改 `config.py` 中的对应值，详细配置请参考上面 [配置](#user-content-配置) 这一节的内容。

**注意启用该功能会每隔一分钟检索一次 ![国家地震台网](http://news.ceic.ac.cn/) ,比较消耗资源，如果不需要启用该功能，只需要在 `\include\plugins\` 目录下删掉对应 `ceic` 文件夹并重启XUN就可以了。**

### 上车

![8.png](https://i.loli.net/2020/01/16/J5NSW2BfbjMK6VZ.png)

注意此功能没有启用 `自然语言处理器` 模块，所以请用 `标准命令格式 + 目的地关键词` 的形式来告诉XUN你想要去的目的地。

**关于此功能我不会再有过多的描述了，请自行体会。**

</details>
<br>

## 计划功能

除了上面功能说明中提到的完善计划，还将计划加入以下功能:

* 开发框架
* 游戏战绩查询
* 关注消息动态转发
* ~~骚话~~ 嘴臭

> XUN: ~~有生之年~~ 史 诗 巨 坑  
> AH: 下属不许啵上司嘴！

## 开源许可证

本项目使用 [LGPLv3](https://github.com/Angel-Hair/XUN_Bot/blob/master/LICENSE) 许可证，由于本项目的特殊性，本项目的源码中出现在 NoneBot 文档的部分（例如作为其示例代码），不使用 LGPLv3 许可，而使用和 NoneBot 一样的 MIT 许可。
