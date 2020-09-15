from nonebot import on_command, CommandSession

from .data_source import get_r6smessage_of_username
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '彩虹六号战绩查询'
__plugin_usage__ = r"""
彩虹六号战绩查询

彩虹六号战绩 [游戏名称]
r6s [游戏名称]
r6战绩 [游戏名称]

eg.
r6s Original_04
""".strip()


@on_command('r6s', aliases=('彩虹六号战绩', 'r6s', 'r6战绩'), permission=get_bot().level)
async def translation(session: CommandSession):
    content = session.get('content', prompt='需要给出你想查询的游戏名称')
    r6s_report = await get_r6smessage_of_username(content)
    if r6s_report:
        await session.send(r6s_report)
    else:
        xlogger.error("Not found userName")
        await session.send("[ERROR]Not found userName")


@translation.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['content'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('游戏名称不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg