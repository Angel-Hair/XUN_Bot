from nonebot import on_command, CommandSession

from .data_source import get_bt_info
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '磁力搜索'
__plugin_usage__ = r"""
不定期神隐的功能
*请各位使用后不要转发*
默认检索排序为相关度，如果需要按更新时间排序，加上参数: -U

-按相关度检索(默认)
bt [关键词]
磁力 [关键词]

-按更新时间检索(参数不区分大小写，但要注意空格)
bt -U [关键词]
磁力 -U [关键词]
""".strip()


@on_command('bt', aliases=('bt', '磁力'), permission=get_bot().level)
async def bt(session: CommandSession):
    url = session.get('url', prompt='关键字给我')
    bt_report = await get_bt_info(url)
    if bt_report:
        await session.send(bt_report)
    else:
        xlogger.error("Not found btInfo")
        await session.send("[ERROR]Not found btInfo")


@bt.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    url = get_url(stripped_arg)

    if session.is_first_run:
        if url:
            session.state['url'] = url
        return

    if not url:
        session.pause('宁就是虚空带师？关键词GKD！')

    session.state[session.current_key] = url

def get_url(words: str) -> str:
    url = ''
    if words != '':
        domain = "www.btmet.xyz"
        if '-U' == words[:2].upper():
            key = words[2:]
            if key != '':
                url = 'https://' + domain + '/search.php?q=' + key + '&c=&l=&o=1'
        else:
            url = 'https://' + domain + '/search.php?q=' + words + '&c=&l=&o=0'

    return url