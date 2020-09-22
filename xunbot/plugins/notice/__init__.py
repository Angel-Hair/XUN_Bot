import time

from nonebot import on_command, CommandSession, permission

from ...xlog import xlogger
from xunbot import get_bot

Bot = get_bot()

PUSH_GROUP_DICT = Bot.config.PUSH_GROUP_DICT

__plugin_name__ = '群通知'
__plugin_usage__ = r"""
【管理员功能】
用于管理员通知群的功能

通知 【信息】
push 【信息】
""".strip()


@on_command('notice', aliases=('push', '通知'), permission=0xF000)
async def notice(session: CommandSession):
    info = session.get('info', prompt='请给出需要通知的信息')

    if PUSH_GROUP_DICT:
        header = "🔈群通知🔈\n\n"
        sender_info = "\n\n——{}(管理员) 发布于 {}".format(session.event['sender']['nickname'], 
            time.strftime("%Y-%m-%d", time.localtime(session.event['time'])))
        
        for group in PUSH_GROUP_DICT:
            await Bot.send_group_msg(group_id=group, message=header + info + sender_info)
        await session.send("通知成功:)")
    else:
        await session.send("没有要通知的群，请注意修改config.py文件中对应值")


@notice.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        if arg:
            session.state['info'] = arg
        return

    if not arg:
        session.pause('通知的信息不能为空，请重新输入')

    session.state[session.current_key] = arg