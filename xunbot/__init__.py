from os import path
import logging
from typing import Any, Optional
# from shutil import copyfile

from nonebot import *
from nonebot import logger

from .level import get_permission_level
from .xlog import xlogger


class Xun(NoneBot):
    def __init__(self, config_object: Optional[Any] = None):
        super().__init__(config_object)
        self.level = int(get_permission_level(self.config.PERMISSION_LEVEL))
        logger.info("Permission Level: LV.{}".format(self.config.PERMISSION_LEVEL))


_bot: Optional[Xun] = None


def run(config, host: Optional[str] = None, port: Optional[int] = None,
        *args, **kwargs) -> None:
    xinit(config)
    if config.BUILTIN_PLUGINS:
        load_builtin_plugins()
    load_plugins(
        path.join(path.dirname(__file__), 'plugins'),
        'xunbot.plugins'
    )
    get_bot().run(host=host, port=port, *args, **kwargs)


def xinit(config_object: Optional[Any] = None) -> None:
    global _bot
    _bot = Xun(config_object)

    if _bot.config.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if _bot.config.XDEBUG:
        xlogger.setLevel(logging.DEBUG)
    else:
        xlogger.setLevel(logging.INFO)

    _bot.server_app.before_serving(_start_scheduler)
    

def get_bot() -> Xun:
    if _bot is None:
        raise ValueError('XunBot instance has not been initialized')
    return _bot


async def _start_scheduler():
    if scheduler and not scheduler.running:
        scheduler.configure(_bot.config.APSCHEDULER_CONFIG)
        scheduler.start()
        logger.info('Scheduler started')


# def set_config():
#     dirname, _ = path.split(path.abspath(__file__))
#     copyfile(path.join(dirname, "simple_config.py"), path.join(getcwd(), "config.py"))