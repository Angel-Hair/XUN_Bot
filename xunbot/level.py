from .xlog import xlogger

def get_permission_level(level: "int = 1") -> int:
    if not(0 < level < 11):
        xlogger.error("[ERROR] level set incorrectly, now XUN Security Level is 1 !!!")
        return 0xF000

    PRIVATE_FRIEND = 0x0001
    PRIVATE_GROUP = 0x0002
    PRIVATE_DISCUSS = 0x0004
    PRIVATE_OTHER = 0x0008
    PRIVATE = 0x000F
    DISCUSS = 0x00F0
    GROUP_MEMBER = 0x0100
    GROUP_ADMIN = 0x0200
    GROUP_OWNER = 0x0400
    GROUP = 0x0F00
    SUPERUSER = 0xF000
    EVERYBODY = 0xFFFF

    level_permission = 0
    if level >= 1:
        level_permission |= SUPERUSER
    if level >= 2:
        level_permission |= PRIVATE_FRIEND
    if level >= 3:
        level_permission |= GROUP_OWNER
    if level >= 4:
        level_permission |= GROUP_ADMIN
    if level >= 5:
        level_permission |= GROUP_MEMBER
    if level >= 6:
        level_permission |= GROUP
        level_permission |= PRIVATE_GROUP
    if level >= 7:
        level_permission |= DISCUSS
    if level >= 8:
        level_permission |= PRIVATE_DISCUSS
    if level >= 9:
        level_permission |= PRIVATE_OTHER
    if level >= 10:
        level_permission |= PRIVATE
        level_permission |= EVERYBODY

    return level_permission