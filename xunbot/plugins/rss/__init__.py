from datetime import timedelta

from nonebot import on_command, scheduler, permission, CommandSession
# from apscheduler.triggers.interval import IntervalTrigger

from ...xlog import xlogger
from .data_source import RSS_reader, RSS
from xunbot import get_bot

MAX_RSS_P = get_bot().config.MAX_RSS_P
MAX_RSS_G = get_bot().config.MAX_RSS_G
MAX_RSS_D = get_bot().config.MAX_RSS_D
RSSINTERVAL = get_bot().config.RSSINTERVAL
xlogger.debug("time interval: {}".format(RSSINTERVAL))


__plugin_name__ = 'RSSHub订阅'
__plugin_usage__ = r"""
配合RSSHub实现RSS订阅
-当前订阅检索的时间间隔为: {}

rss [RSSHub 路由]
订阅 [RSSHub 路由]

unrss [RSSHub 路由]
取消订阅 [RSSHub 路由]

无参数时返回当前的订阅表：
rss #返回订阅表

-[RSSHub 路由]请参考：https://docs.rsshub.app/social-media.html

以下是一些简单说明：
-比如要订阅A站用户id为934542的投稿，则应该发送：
订阅 /acfun/user/video/934542
-如果要订阅B站用户id为2949989的投稿，则发送：
订阅 /bilibili/user/video/2949989
-而要订阅SteamDB周末免费游戏，则发送：
订阅 /steamdb/free/weekend

另外群订阅只能由管理员、群主或者群管理员通过群聊添加和修改，
讨论组订阅只能由管理员订阅，而个人订阅只需要私聊即可。
""".format(str(timedelta(**RSSINTERVAL))).strip()

xlogger.info("Loading RSS reader……")
reader = RSS_reader()

# async def _start(self):
#     delta = timedelta(hours=RSSINTERVAL)
#     trigger = IntervalTrigger(
#         run_date=datetime.now() + delta
#     )
#     scheduler.add_job(
#         func=await reader.send_msg,
#         trigger=trigger,
#         args=(),
#         misfire_grace_time=60,
#     )

@scheduler.scheduled_job('interval', **RSSINTERVAL)
async def _():
    await reader.send_msg()


@on_command('rss', aliases=('rss', '订阅'), permission=get_bot().level)
async def rss(session: CommandSession):
    xlogger.debug("rss command wake up")
    type = session.event['message_type']
    check, id = await check_msg_permission(session, type)

    if check and id :
        route = session.current_arg_text.strip().lower()

        if route:
            if check_suber_limit(reader, type, id):
                await session.send("请等待测试……")
                rss_test = RSS(route)
                if await rss_test.test_feed():
                    if reader.add_rss(route, type=type, id=id, title=rss_test.title, lasttitle=rss_test.lasttitle):
                        await session.send("订阅成功:)")
                    else:
                        await session.send("订阅失败:(")
                else:
                    await session.send("订阅源测试失败，请检查订阅源是否正确")
                    await session.send("如果需要帮助，请发送: help rss")
                    await session.send("另外，如果多次测试失败，请联系管理员")
            else:
                await session.send("订阅数已达到限制，可以尝试删掉不必要的订阅_(:3 」∠)_")
        else:
            routes_msg = "\n".join(reader.get_routes(type, id))
            info = '空' if not routes_msg else '\n'+routes_msg
            await session.send("当前的订阅列表为" + info)
    else:
        await session.send("权限错误")


@on_command('unrss', aliases=('unrss', '取消订阅'), permission=get_bot().level)
async def unrss(session: CommandSession):
    xlogger.debug("unrss command wake up")
    type = session.event['message_type']
    check, id = await check_msg_permission(session, type)

    if check and id :
        route = session.current_arg_text.strip().lower()

        if route in reader.get_routes(type, id):
            if reader.remove_subscriber(route, type, id):
                await session.send("取消订阅成功:)")
            else:
                await session.send("取消订阅失败:(")
        else:
            await session.send("没有订阅该路由")
    else:
        await session.send("权限错误")


def check_suber_limit(reader: RSS_reader, type: str, id: int) -> bool:
    subscriptions = len(reader.get_routes(type, id)) + 1

    return (type == "private" and subscriptions <= MAX_RSS_P) or  \
            (type == "group" and subscriptions <= MAX_RSS_G) or  \
            (type == "discuss" and subscriptions <= MAX_RSS_D)


async def check_msg_permission(session: CommandSession, type: str) -> (bool, int):
    check = False
    id = 0

    if type == "group":
        id = session.event['group_id']
        xlogger.info("check the group permission: {}".format(id))
        check = await permission.check_permission(session.bot, session.event, 0xF600)
    elif type == "private":
        id = session.event['user_id']
        check = True
    elif type == "discuss":
        id = session.event['discuss_id']
        xlogger.info("check the discuss permission: {}".format(id))
        check = await permission.check_permission(session.bot, session.event, 0xF000)

    return check, id


# @rss.args_parser
# async def _(session: CommandSession):
#     stripped_arg = session.current_arg_text.strip()

#     if session.is_first_run:
#         if stripped_arg:
#             session.state['route'] = stripped_arg
#         return

#     if not stripped_arg:
#         session.pause('还搁这儿虚空订阅呢，快给我一个订阅源')

#     session.state[session.current_key] = stripped_arg