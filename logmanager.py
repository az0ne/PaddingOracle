
import logging
import Colorer

logger = None
level = None

def getlogger():
    global logger, level
    if not logger:
        logger = logging.getLogger("")
        logger.setLevel(level)
        ch = logging.StreamHandler()
        ch.setLevel(level)
        logger.addHandler(ch)
    return logger

def set_level(_level):
    global level
    level = _level
set_level(logging.INFO)
