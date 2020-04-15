from nonebot import on_command, CommandSession

from .data_source import from_anime_get_info


@on_command('anime', aliases=('anime', '搜番'))
async def anime(session: CommandSession):
    key_word = session.get('key_word', prompt='需要的番剧名称是什么？')
    anime_report = await from_anime_get_info(key_word)
    if anime_report:
        await session.send(anime_report)
    else:
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

