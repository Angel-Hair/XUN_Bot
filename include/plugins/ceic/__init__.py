from .data_source import Ceicinfo

from nonebot import get_bot, scheduler
EM = get_bot().config.EM
CEICONLYCN = get_bot().config.CEICONLYCN
from aiocqhttp.exceptions import Error as CQHttpError


print("[info]loading ceicinfo……")
ceic = Ceicinfo(EM, CEICONLYCN)

@scheduler.scheduled_job('cron', minute='*')
async def _():
    bot = get_bot()
    group_list = await bot.get_group_list()
    mesg = await ceic.getceicinfo()
    if mesg:
        try:
            for group in group_list:
                print("send group {} mesg……".format(group['group_name']))
                await bot.send_group_msg(group_id=group['group_id'], message=mesg)
        except CQHttpError:
            pass
