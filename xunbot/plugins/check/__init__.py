from random import choice

from nonebot import on_command, CommandSession, permission

from .data_source import Check
from ...xlog import xlogger
from xunbot import get_bot

Bot = get_bot()
MAX_PERFORMANCE_PERCENT = Bot.config.MAX_PERFORMANCE_PERCENT
PROCESS_NAME_LIST = Bot.config.PROCESS_NAME_LIST
SUPERUSERS = Bot.config.SUPERUSERS


__plugin_name__ = '自我检查'
__plugin_usage__ = r"""
进行一次简单的自我检查
如果检查出问题会通知管理员的

*注意并不能检测所有问题，如果发现了问题，请及时反馈*

check [无参数]
自检 [无参数]
""".strip()


xlogger.info("Loading CheckInfo……")
check = Check(Bot.config.PROCESS_NAME_LIST)

@on_command('check', aliases=('check', '自检', '自檢'), permission=Bot.level)
async def music_recommend(session: CommandSession):
    if await permission.check_permission(session.bot, session.event, 0xF000):
        check_report_admin = await check.get_check_info()
        if check_report_admin:
            await session.send(check_report_admin)
        else:
            xlogger.error("Not found Check Report")
            await session.send("[ERROR]Not found Check Report")
    else:
        check_report = await check.get_check_easy(MAX_PERFORMANCE_PERCENT)
        more_info = '[CQ:at,qq={}]'.format(choice(list(SUPERUSERS))) if (SUPERUSERS and session.event['message_type'] == 'group') else "\n……管理员鸽了，知道管理员在哪儿摸鱼的话请把他拖回来维护~"
        if check_report:
            await session.send(check_report + more_info)
            check_report_admin = await check.get_check_info()
            if check_report_admin and SUPERUSERS:
                for admin in SUPERUSERS:
                    await Bot.send_private_msg(user_id=admin, message='我好像生病了……')
                    await Bot.send_private_msg(user_id=admin, message=check_report_admin)
        else: await session.send("I'm fine, thanks. ^_^")