from .data_source import ceicinfo

import nonebot
from aiocqhttp.exceptions import Error as CQHttpError

import sys
sys.path.append('../../../')
from config import EM, CEICONLYCN

print("[info]loading ceicinfo……")
ceic = ceicinfo(EM, CEICONLYCN)

@nonebot.scheduler.scheduled_job('cron', minute='*')
async def _():
    bot = nonebot.get_bot()
    group_list = await bot.get_group_list()
    mesg = await ceic.getceicinfo()
    if mesg:
        try:
            for group in group_list:
                print("send group {} mesg……".format(group['group_name']))
                await bot.send_group_msg(group_id=group['group_id'], message=mesg)
        except CQHttpError:
            pass
