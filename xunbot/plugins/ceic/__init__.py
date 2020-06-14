from aiocqhttp.exceptions import Error as CQHttpError
from nonebot import scheduler

from ...xlog import xlogger
from .data_source import Ceicinfo
from xunbot import get_bot

EM = get_bot().config.EM
CEICONLYCN = get_bot().config.CEICONLYCN


__plugin_name__ = '地震通报'
__plugin_usage__ = r"""
【群技能】【被动技能】地震通报（误差±10min）
""".strip()


xlogger.info("Loading CeicInfo……")
ceic = Ceicinfo(EM, CEICONLYCN)

@scheduler.scheduled_job('cron', minute='*')
async def _():
    mesg = await ceic.getceicinfo()
    if mesg:
        bot = get_bot()
        group_list = await bot.get_group_list()
        try:
            for group in group_list:
                xlogger.info("send group {} mesg……".format(group['group_name']))
                await bot.send_group_msg(group_id=group['group_id'], message=mesg)
        except CQHttpError as e:
            xlogger.error(e)
