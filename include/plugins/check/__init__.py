from random import choice

from nonebot import on_command, CommandSession, get_bot, permission

from .data_source import Check

Bot = get_bot()

MAX_PERFORMANCE_PERCENT = Bot.config.MAX_PERFORMANCE_PERCENT
PROCESS_NAME_LIST = Bot.config.PROCESS_NAME_LIST
SUPERUSERS = Bot.config.SUPERUSERS

print("[info]loading checkinfo……")
check = Check(Bot.config.PROCESS_NAME_LIST)

@on_command('check', aliases=('check', '自检', '自檢'), permission=Bot.level)
async def music_recommend(session: CommandSession):
    if await permission.check_permission(session.bot, session.event, 0xF000):
        check_report_admin = await check.get_check_info()
        if check_report_admin:
            await session.send(check_report_admin)
    else:
        check_report = await check.get_check_easy(MAX_PERFORMANCE_PERCENT)
        more_info = '[CQ:at,qq={}]'.format(choice(list(SUPERUSERS))) if SUPERUSERS else "\n……管理员鸽了，请有知道的人把管理员拖回来维护~"
        if check_report:
            await session.send(check_report + more_info)
            check_report_admin = await check.get_check_info()
            if check_report_admin and SUPERUSERS:
                for admin in SUPERUSERS:
                    await Bot.send_private_msg(user_id=admin, message='我好像生病了……')
                    await Bot.send_private_msg(user_id=admin, message=check_report_admin)
        else: await session.send("I'm fine, thanks. ^_^")