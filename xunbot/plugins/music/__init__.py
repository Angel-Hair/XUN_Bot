import re

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from .data_source import get_song_of_music
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '音乐点播'
__plugin_usage__ = r"""
音乐 [音乐名]
来首 [音乐名]
music [音乐名]
[NLP模块] XXXX来首《XXXX》XXX
PS:提供更加完整的信息有助于得到更加精确的音乐，如 音乐名 - 歌手

eg.
音乐 Birthday - 初音ミク
""".strip()


@on_command('music', aliases=('music', '音乐', '来首', '音樂', '來首'), permission=get_bot().level)
async def music(session: CommandSession):
    music_name = session.get('music', prompt='要点播哪首歌呢？')
    music_report = await get_song_of_music(music_name)
    if music_report:
        await session.send(music_report)
    else:
        xlogger.error("Not found Music Report")
        await session.send("音乐获取失败:(")

@music.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['music'] = stripped_arg
        return

    if not stripped_arg:
        session.pause('歌曲名不能为空呢，请重新输入')

    session.state[session.current_key] = stripped_arg

@on_natural_language(keywords={'点播', '来首', '點播', '來首'}, permission=get_bot().level)
async def _(session: NLPSession):
    msg = session.msg_text
    pattern = re.compile('《(.*)》')
    music_name = pattern.findall(msg)[0]

    return IntentCommand(90.0, 'music',  current_arg=music_name or '')