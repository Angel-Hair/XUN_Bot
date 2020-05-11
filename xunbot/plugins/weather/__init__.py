from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import thulac

from ...hanziconv import HanziConv
from .data_source import get_weather_of_city
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '天气查询'
__plugin_usage__ = r"""
天气 [地区]
查天气 [地区]
[NLP模块] XXXX天气XXXX地区XXXX
ps: 目前只支持国内地区查询
""".strip()


@on_command('weather', aliases=('天气', '查天气', '天氣', '查天氣'), permission=get_bot().level)
async def weather(session: CommandSession):
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    weather_report = await get_weather_of_city(city)
    if weather_report:
        await session.send(weather_report)
    else:
        xlogger.error("Not found weatherInfo")
        await session.send("[ERROR]Not found weatherInfo")


@weather.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['city'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg


@on_natural_language(keywords={'天气', '天氣'}, permission=get_bot().level)
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    stripped_msg = HanziConv.toSimplified(stripped_msg)
    thu1 = thulac.thulac(filt=True)
    words = thu1.cut(stripped_msg)

    city = None
    for word in words:
        if word[1] == 'ns':
            # ns 词性表示地名
            city = word[0]
            break

    return IntentCommand(90.0, 'weather', current_arg=city or '')
