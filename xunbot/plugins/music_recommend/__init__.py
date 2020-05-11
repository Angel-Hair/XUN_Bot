from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand 

from .data_source import get_song_of_music, get_recommend
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '音乐推荐'
__plugin_usage__ = r"""
推荐首 [描述]
推荐一首 [描述]
推荐音乐 [描述]
音乐推荐 [描述]
[NLP模块] XXXX推进首XXXX

eg: 给屑SK推荐一首适合一个人孤零零回家路上平地摔后倍感伤心回家后没人关心只能孤独的打开QQ的歌
eg: 推荐首打麻将的时候可以摸到天和字一色大四喜四暗刻单骑六倍役满的歌
""".strip()


@on_command('music_recommend', aliases=('推荐音乐', '音乐推荐', '推荐首', '推荐一首', '推薦音樂', '音樂推薦', '推薦首', '推薦一首'), permission=get_bot().level)
async def music_recommend(session: CommandSession):
    music_command = session.get('command', prompt='你想听什么样的音乐呢？')
    keywords = await get_recommend(music_command)
    music_report, infot = await get_song_of_music(keywords)
    if music_report:
        await session.send(music_report)
        for info in infot:
            await session.send(info)
    else:
        xlogger.error("Not found musicInfo")
        await session.send("[ERROR]Not found musicInfo")

@music_recommend.args_parser
async def _(session: CommandSession):
    arg = session.current_arg

    if session.is_first_run:
        if arg:
            session.state['command'] = arg
        return

    if not arg:
        session.pause('描述不能为空呢，请重新输入')

    session.state[session.current_key] = arg

@on_natural_language(keywords={'推荐一首', '推荐首', '推薦一首', '推薦首'}, permission=get_bot().level)
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()

    return IntentCommand(90.0, 'music_recommend', current_arg=stripped_msg or '')
