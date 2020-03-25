import io
import tokenize
import sys
from copy import deepcopy

sys.path.append('../../../')
from config import MORE_COMPLEX, CALCULATE_LIST

def check_unsafe_attributes(string) -> (dict, dict):
    """This code is modified from:
    https://mozillazg.com/2016/05/python-some-security-problems-about-use-exec-function.rst.html
    """
    g = {}
    l = {}
    model_del_list = ['__import__','open','quit','exit','requests','help','license','exec','eval','copyright','credits']

    if MORE_COMPLEX:
        for fn in CALCULATE_LIST.keys():
            sn = CALCULATE_LIST[fn]
            if sn:
                exec("import {} as {}".format(fn, sn), g, l)
            else:
                exec("import {}".format(fn), g, l)
    g_c = deepcopy(g)

    for md in model_del_list:
        if md in g_c['__builtins__'].keys():
            g_c['__builtins__'].pop(md)
        else: print("[Error] {} not in global['__builtins__'] !".format(md))

    go = tokenize.tokenize(io.BytesIO(string.encode('utf-8')).readline)
    pre_op = ''
    for toktype, tokval, _, _, _ in go:
        if toktype == tokenize.NAME and pre_op == '.' and tokval.startswith('_'):
            attr = tokval
            msg = "access to attribute '{0}' is unsafe.".format(attr)
            raise AttributeError(msg)
        elif toktype == tokenize.OP:
            pre_op = tokval

    return g_c, l

def remove_l(loacl_dict: dict):
    pl = loacl_dict
    del_l = []
    for key in pl:
        if "module '" in str(pl[key]):
            del_l.append(key)
    if del_l:
        for key in del_l:
            del pl[key]
    
    return pl

def check(loacl_dict: dict):
    repass_list = []
    pl = loacl_dict

    key_list = list(pl.keys())
    if "END" in key_list:
        return str(pl["END"])

    for key in pl.keys():
        repass_list.append("{}: {}".format(key, pl[key]))
        
    return "\n".join(repass_list)

async def get_end_calculate(conde_str: str) -> str:
    if 'import ' in conde_str:
        return("[Warning] For program security reasons, the Import module will be removed after version 7.0-beta. more information: https://github.com/Angel-Hair/XUN_Bot") # This code will be removed in a future release.

    repass = ''
    try:
        g, l = check_unsafe_attributes(conde_str)
        exec(conde_str, g, l)
        l = remove_l(l)
        repass = check(l)
    except Exception as e:
        repass = "[Error] {}".format(e)

    return repass