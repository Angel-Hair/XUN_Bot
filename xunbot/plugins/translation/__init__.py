from nonebot import on_command, CommandSession

from .data_source import get_transl_of_content
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '翻译'
__plugin_usage__ = r"""
自动识别源语言的翻译

翻译 [单词或者句子]
transl [单词或者句子]
""".strip()


@on_command('translation', aliases=('翻译', 'transl', '翻譯'), permission=get_bot().level)
async def translation(session: CommandSession):
    content = session.get('content', prompt='需要给出你想翻译的内容')
    transl_report = await get_transl_of_content(content)
    if transl_report:
        await session.send(transl_report)
    else:
        xlogger.error("Not found translInfo")
        await session.send("[ERROR]Not found translInfo")


@translation.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['content'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('要翻译的内容不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg
