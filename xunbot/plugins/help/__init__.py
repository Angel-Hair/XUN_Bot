from nonebot import on_command, CommandSession, get_loaded_plugins

from xunbot import get_bot


__plugin_name__ = '使用帮助'
__plugin_usage__ = r"""
help [功能名称]
帮助 [功能名称]
使用帮助 [功能名称]
使用方法 [功能名称]
ps.无参数时，返回功能列表
eg.
help [无参数] #返回功能列表
help [功能名称]
""".strip()


@on_command('help', aliases=('help', '使用帮助', '帮助', '使用方法'), permission=get_bot().level)
async def help(session: CommandSession):
    plugins = list(filter(lambda p: p.name, get_loaded_plugins()))

    arg = session.current_arg_text.strip().lower()
    if not arg:
        await session.send('我现在支持的功能有：\n\n' + '\n'.join(p.name for p in plugins))
        return
    
    check = set(filter(lambda p: p.name.lower() == arg, plugins))
    if check:
        for p in check:
            await session.send(p.usage)
    else: await session.send("功能不存在:)")