from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from .data_source import get_anime


@on_command('whatanime', aliases=('whatanime', '搜番', '识番'))
async def whatanime(session: CommandSession):
    anime_data = session.get('whatanime', prompt='图呢？GKD')
    anime_data_report = await get_anime(anime_data)
    if anime_data_report:
        await session.send(anime_data_report)
    else:
        await session.send("[ERROR]Not found Anime")


@whatanime.args_parser
async def _(session: CommandSession):
    image_arg = session.current_arg_images

    if session.is_first_run:
        if image_arg:
            session.state['whatanime'] = image_arg[0]
        return

    if not image_arg:
        session.pause('没图说个J*，GKD!')

    session.state[session.current_key] = image_arg

@on_natural_language(keywords={'whatanime', '搜番', '识番'})
async def _(session: NLPSession):
    msg = session.msg

    # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
    return IntentCommand(90.0, 'whatanime', current_arg=msg or '')