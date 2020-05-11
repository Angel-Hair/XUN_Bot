import logging
import sys

xlogger = logging.getLogger('xunbot')
xun_handler = logging.StreamHandler(sys.stdout)
xun_handler.setFormatter(
    logging.Formatter('[%(asctime)s %(name)s] %(levelname)s: %(message)s \n[From: %(pathname)s]'))
xlogger.addHandler(xun_handler)