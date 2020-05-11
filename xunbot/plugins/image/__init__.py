from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from .data_source import get_image_data
from ...xlog import xlogger
from xunbot import get_bot


__plugin_name__ = '识图'
__plugin_usage__ = r"""
以图识图

搜图 [图片]
识图 [图片]
image [图片]
[NLP模块] XXX搜图XXX图片XXX
""".strip()


@on_command('image', aliases=('image', '搜图', '识图', '搜圖', '識圖'), permission=get_bot().level)
async def image(session: CommandSession):
    image_data = session.get('image', prompt='图呢？GKD')
    image_data_report = await get_image_data(image_data, session.bot.config.SAUCENAO_KEY)
    
    if image_data_report:
        await session.send(image_data_report)
    else:
        xlogger.error("Not found imageInfo")
        await session.send("[ERROR]Not found imageInfo")


@image.args_parser
async def _(session: CommandSession):
    image_arg = session.current_arg_images

    if session.is_first_run:
        if image_arg:
            session.state['image'] = image_arg[0]
        return

    if not image_arg:
        session.pause('没图说个J*，GKD!')

    session.state[session.current_key] = image_arg


@on_natural_language(keywords={'image', '搜图', '识图', '搜圖', '識圖'}, permission=get_bot().level)
async def _(session: NLPSession):
    msg = session.msg
    return IntentCommand(90.0, 'image', current_arg=msg or '')