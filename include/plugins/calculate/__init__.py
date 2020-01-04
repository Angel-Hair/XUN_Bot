from nonebot import on_command, CommandSession

from .data_source import get_end_calculate


@on_command('calculate', aliases=('计算', 'exp'))
async def calculate(session: CommandSession):
    code_str = session.get('calculate', prompt='请输入公式或代码……')
    code_report = await get_end_calculate(code_str)
    if code_report:
        await session.send(code_report)
    else:
        await session.send('计算结果命名空间似乎为空呢_(:3 」∠)_\n请注意结果变量一定要命令为"END"哦~')

@calculate.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['calculate'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('请输入公式或代码……')

    session.state[session.current_key] = stripped_arg