from os import path

from level import get_permission_level

import nonebot

import config

if __name__ == '__main__':
    level = get_permission_level(config.PERMISSION_LEVEL)
    nonebot.NoneBot.level = level
    
    nonebot.init(config)
    nonebot.load_builtin_plugins()
    nonebot.load_plugins(
        path.join(path.dirname(__file__), 'include', 'plugins'),
        'include.plugins'
    )
    nonebot.run()
