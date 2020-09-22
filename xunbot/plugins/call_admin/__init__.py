import time

from nonebot import on_command, CommandSession, permission

from ...xlog import xlogger
from xunbot import get_bot

Bot = get_bot()

CALL_BLACK_DICT = Bot.config.CALL_BLACK_DICT
SUPERUSERS = Bot.config.SUPERUSERS

__plugin_name__ = '致电管理员'
__plugin_usage__ = r"""
让小寻帮忙致电管理员

*请不要发无意义的内容*

call_admin [致电内容]
致电管理员 [内容]

eg.
call_admin 小寻XX功能失效了
致电管理员 希望加入XX功能
""".strip()


@on_command('call_admin', aliases=('call_admin', '致电管理员', '致電管理員'), permission=Bot.level)
async def call_admin(session: CommandSession):
    id = session.event['user_id']
    
    if id not in CALL_BLACK_DICT:
        info = session.get('info', prompt='给我你需要致电的信息')
        xlogger.info("Get Information: {} \nfrom ID: {}".format(info, id))

        if SUPERUSERS:
            sender_info = "\n——@{}({}) | {}".format(session.event['sender']['nickname'], id, 
                time.strftime("%Y-%m-%d", time.localtime(session.event['time'])))
            
            for admin in SUPERUSERS:
                await Bot.send_private_msg(user_id=admin, message="您有一条致电的信息：")
                await Bot.send_private_msg(user_id=admin, message=info + sender_info)
            await session.send("致电成功:)")
            xlogger.info("Successful call admin")
        else:
            await session.send("……管理员鸽了，知道管理员在哪儿摸鱼的话请把他拖回来~")
    else:
        xlogger.info("ID: {} wanna call admin, but in blacklist".format(id))
        await session.send("致电失败:)\n您已被列入黑名单，无法致电")


@call_admin.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        if arg:
            session.state['info'] = arg
        return

    if not arg:
        session.pause('管理员让我给宁带个话：宁搁这儿虚空致电呢？GKD把信息给我！')

    session.state[session.current_key] = arg