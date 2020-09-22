import time

from nonebot import on_command, CommandSession, permission

from .data_source import get_msg_from_board, save_msg_board
from ...xlog import xlogger
from xunbot import get_bot

Bot = get_bot()
MAX_MGB_WORD = Bot.config.MAX_MGB_WORD
MAX_MGB_LIST = Bot.config.MAX_MGB_LIST


__plugin_name__ = '留言板'
__plugin_usage__ = r"""
在留言板上进行留言或者查看留言

注意留言字数不要超过{}字
最多查看最后{}条留言

mgb [留言]
留言板 [留言]
ps.无参数时，为查看留言

eg.
mgb sk是屑的天花板
留言板 skwlp
mgb #查看留言
""".format(MAX_MGB_WORD,MAX_MGB_LIST).strip()


@on_command('message_board', aliases=('mgb', '留言板'), permission=Bot.level)
async def message_board(session: CommandSession):
    msg = session.current_arg_text.strip()
    if msg:
        if len(msg) <= MAX_MGB_WORD:
            save_msg_board(session.event['sender'], msg, session.event['time'])
            await session.send("留言成功:)")
        else:
            await session.send("留言失败:(\n超过字数限制，请不要超过{}字。".format(MAX_MGB_WORD))
    else:
        message_board_report = await get_msg_from_board(MAX_MGB_LIST)
        await session.send(message_board_report)