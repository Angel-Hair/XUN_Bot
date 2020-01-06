from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
import thulac
import sys
from os import path   

from .data_source import get_song_of_music


def get_recommend(music_command: str):

    keywords = []
    user_words_path = path.join(path.dirname(__file__), "user_words.txt")
    user_words = []
    with open(user_words_path,'r', encoding='UTF-8') as f:
        for line in f:
            usr = str(line.strip('\n'))
            if usr.lower() in music_command.lower():
                keywords.append(usr.lower())
            user_words.append(usr)

    thu1 = thulac.thulac()
    words = thu1.cut(music_command)
    
    for word in words:
        if (word[0].lower() not in keywords) and ((word[1] in ['a', 't', 'np', 'id', 'i']) or (word[1] == 'v'  and (word[0] not in ['推荐', '来', '听', '着']))):
            keywords.append(word[0])

    inline = "+".join(keywords)

    return inline

@on_command('music_recommend', aliases=('推荐音乐', '音乐推荐', '推荐一首'))
async def music_recommend(session: CommandSession):
    music_command = session.get('command', prompt='你想听什么样的音乐呢？')
    keywords = get_recommend(music_command)
    music_report, infot = await get_song_of_music(keywords)
    if music_report:
        await session.send(music_report)
    await session.send(infot)

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

@on_natural_language(keywords={'音乐', '推荐', '推荐一首', '推荐首', '歌', '曲'})
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'music_recommend', current_arg=stripped_msg or '')
