from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import thulac

from .data_source import get_definition_of_word


@on_command('jpd', aliases=('日典', 'jd'))
async def jpd(session: CommandSession):
    city = session.get('word', prompt='你想查询哪个单词呢？')
    jpd_report = await get_definition_of_word(city)
    if jpd_report:
        await session.send(jpd_report)
    else:
        await session.send("[ERROR]Not found jpdInfo")


@jpd.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['word'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要查询的单词不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg
