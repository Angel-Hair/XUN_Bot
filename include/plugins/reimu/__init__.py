from nonebot import on_command, CommandSession

from .data_source import from_reimu_get_info


@on_command('reimu', aliases=('reimu', '上车', '查找资源'))
async def reimu(session: CommandSession):
    key_word = session.get('key_word', prompt='你想到哪儿下车？')
    reimu_report = await from_reimu_get_info(key_word)
    if reimu_report:
        await session.send(reimu_report)
    else:
        await session.send("[ERROR]Not found reimuInfo")


@reimu.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['key_word'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('没时间等了！快说你要去哪里？')

    session.state[session.current_key] = stripped_arg

