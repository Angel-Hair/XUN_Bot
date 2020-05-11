from nonebot import on_command, CommandSession

from .data_source import from_anime_get_info
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '搜番'
__plugin_usage__ = r"""
搜索动漫资源

搜番  [番剧名称或者关键词]
anime  [番剧名称或者关键词]

eg.
搜番 Aria
""".strip()


@on_command('anime', aliases=('anime', '搜番'), permission=get_bot().level)
async def anime(session: CommandSession):
    key_word = session.get('key_word', prompt='需要的番剧名称是什么？')
    anime_report = await from_anime_get_info(key_word)
    if anime_report:
        await session.send(anime_report)
    else:
        xlogger.warning("Not found animeInfo")
        await session.send("[ERROR]Not found animeInfo")


@anime.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['key_word'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('番名GKD!')

    session.state[session.current_key] = stripped_arg

