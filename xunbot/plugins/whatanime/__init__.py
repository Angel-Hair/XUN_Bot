from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from .data_source import get_anime
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '识番'
__plugin_usage__ = r"""
以图识番

识番 [图片]
whatanime [图片]
[NLP模块] XXX识番XXX图片XXX
""".strip()


@on_command('whatanime', aliases=('whatanime', '识番', '識番'), permission=get_bot().level)
async def whatanime(session: CommandSession):
    anime_data = session.get('whatanime', prompt='图呢？GKD')
    anime_data_report = await get_anime(anime_data)
    if anime_data_report:
        await session.send(anime_data_report)
    else:
        xlogger.error("Not found Anime")
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

@on_natural_language(keywords={'whatanime', '识番', '識番'}, permission=get_bot().level)
async def _(session: NLPSession):
    msg = session.msg
    return IntentCommand(90.0, 'whatanime', current_arg=msg or '')