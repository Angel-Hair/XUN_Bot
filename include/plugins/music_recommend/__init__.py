from nonebot import on_command, CommandSession, get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand 

from .data_source import get_song_of_music, get_recommend


@on_command('music_recommend', aliases=('推荐音乐', '音乐推荐', '推荐一首', '推薦音樂', '音樂推薦', '推薦一首'), permission=get_bot().level)
async def music_recommend(session: CommandSession):
    music_command = session.get('command', prompt='你想听什么样的音乐呢？')
    keywords = await get_recommend(music_command)
    music_report, infot = await get_song_of_music(keywords)
    if music_report:
        await session.send(music_report)
        for info in infot:
            await session.send(info)
    else: await session.send("[ERROR]Not found musicInfo")

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

@on_natural_language(keywords={'推荐', '推荐一首', '推荐首', '推薦', '推薦一首', '推薦首'}, permission=get_bot().level)
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()

    return IntentCommand(90.0, 'music_recommend', current_arg=stripped_msg or '')
