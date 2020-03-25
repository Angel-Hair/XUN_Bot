from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import re

from .data_source import get_song_of_music


@on_command('music', aliases=('音乐', '点播', '来首', '给朕来首', '音樂', '點播', '來首', '給朕來首'))
async def music(session: CommandSession):
    music_name = session.get('music', prompt='要点播哪首歌呢？')
    music_report = await get_song_of_music(music_name)
    if music_report:
        await session.send(music_report)
    else:
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

@on_natural_language(keywords={'点播', '来首', '给朕来首', '點播', '來首', '給朕來首'})
async def _(session: NLPSession):
    msg = session.msg_text
    pattern = re.compile('《(.*)》')
    music_name = pattern.findall(msg)[0]

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'music',  current_arg=music_name or '')