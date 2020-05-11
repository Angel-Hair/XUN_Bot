from nonebot import on_command, CommandSession

from .data_source import get_end_calculate
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '计算'
__plugin_usage__ = r"""
提供基于python的复杂计算
内置有各种计算库，如:np, math, scipy(前提是管理员有配置)

计算  [计算公式]
exp  [计算公式]

注意如果只需要输出结果，需要将结果变量命令为END(注意大小写)

eg.
exp a=np.array([1, 2]);END=np.average(a, weights=[1,2])
""".strip()


@on_command('calculate', aliases=('计算', 'exp', '計算'), permission=get_bot().level)
async def calculate(session: CommandSession):
    code_str = session.get('calculate', prompt='请输入公式或代码……')
    code_report = await get_end_calculate(code_str)
    if code_report:
        await session.send(code_report)
    else:
        xlogger.warning("Calculation result is empty.")
        await session.send('计算结果命名空间似乎为空呢_(:3 」∠)_\n请注意结果变量一定要命令为"END"(注意大小写)哦~')

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