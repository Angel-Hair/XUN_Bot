import datetime

from nonebot import on_command, CommandSession, permission

from .pyLunarCalendar import lunar
from ...xlog import xlogger
from xunbot import get_bot

Bot = get_bot()

__plugin_name__ = '黄历'
__plugin_usage__ = r"""
“民俗社会科学项目，不搞封建迷信，宜忌意义在于民间是将红白事合理分开，避免今日您宴请宾客，邻居办白事情况出现，引起邻里纠纷社会分裂。”

lunar [日期(Y-M-D)]
黄历 [日期(Y-M-D)]
黄历 [无参数]

ps. 无参数时，默认日期为当日，另外注意日期的格式为: 年-月-日

eg.
lunar 2019-2-4
黄历 2019-2-4
黄历 # 默认为当日
""".strip()


@on_command('lunarcalendar', aliases=('lunar', '黄历', '黃曆'), permission=Bot.level)
async def lunarcalendar(session: CommandSession):
    date_str = session.current_arg_text.strip()

    if date_str:
        try:
            xlogger.debug("Start check date info: {}".format(date_str))
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')

        except Exception as e:
            xlogger.warning(e)
            await session.send("日期格式错误！")
            await session.send("注意日期的格式为: 年-月-日\neg. 黄历 2019-2-4")
        
        else:
            report = await get_lunar_report(date)
            await session.send(report)
    
    else:
        date = datetime.datetime.today()
        report = await get_lunar_report(date)
        await session.send(report)
    
async def get_lunar_report(date: datetime.datetime) -> str:
    lunar_date = lunar.Lunar(date)
    # dic = {
    #     '农历': '%s %s[%s]年 %s%s' % (lunar_date.lunarYearCn, lunar_date.year8Char, lunar_date.chineseYearZodiac, lunar_date.lunarMonthCn, lunar_date.lunarDayCn),
    #     '星期': lunar_date.weekDayCn,
    #     '星座': lunar_date.starZodiac,
    #     '彭祖百忌': lunar_date.get_pengTaboo(),
    #     '吉神方位': lunar_date.get_luckyGodsDirection(),
    #     '今日胎神': lunar_date.get_fetalGod(),
    #     '宜': lunar_date.goodThing,
    #     '忌': lunar_date.badThing,
    # }
    report = "{}   {}   {}\n【宜】：{}\n【忌】：{}\n【彭祖百忌】：{}\n【今日胎神】：{}\n【吉神方位】：{}\n".format(
        '%s %s[%s]年 %s%s' % (lunar_date.lunarYearCn, lunar_date.year8Char, lunar_date.chineseYearZodiac, lunar_date.lunarMonthCn, lunar_date.lunarDayCn),
        lunar_date.weekDayCn,
        lunar_date.starZodiac,
        ' '.join(lunar_date.goodThing),
        ' '.join(lunar_date.badThing),
        lunar_date.get_pengTaboo(),
        lunar_date.get_fetalGod(),
        ' '.join(lunar_date.get_luckyGodsDirection()),
        )

    return report