import time
from os import path, getcwd

import pandas as pd

from ...xlog import xlogger


async def get_msg_from_board(num: int) -> str:
    try:
        all_msg = load_msg_board()
    except FileNotFoundError as e:
        return "暂时没有留言"

    line_list = ["{}\n——@{}({}) | {}".format(
        data['message'], data['nickname'], data['id'], 
        time.strftime("%Y-%m-%d", time.localtime(data['time']))) 
        for index, data in all_msg[-num:].iterrows()]

    return "\n\n".join(line_list)


def load_msg_board() -> pd.DataFrame:
    all_msg = pd.read_csv(getcwd() + "\\msg_board.csv").sort_values(by='time')
    xlogger.info("Message board data read successfully")
    return all_msg


def save_msg_board(sender: dict, msg: str, time: int):
    msg_board_f = open(getcwd() + '\\msg_board.csv', "a", encoding='utf-8')
    if not msg_board_f.tell():
        msg_board_f.write("nickname,id,time,message" + "\n")
    
    info = "{},{},{},{}".format(sender['nickname'], sender['user_id'], time, msg)
    msg_board_f.write(info + "\n")
    xlogger.debug("Message board is written {}".format(info))
    msg_board_f.close()
    xlogger.info("Message board saved successfully")