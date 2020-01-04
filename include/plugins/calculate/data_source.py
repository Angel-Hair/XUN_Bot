import io
import tokenize

def check_unsafe_attributes(string):
    """https://mozillazg.com/2016/05/python-some-security-problems-about-use-exec-function.rst.html"""
    error_str = ["import os", "open("]
    for estr in error_str:
        if estr in string:
            msg = "code '{}' is unsafe.".format(estr)
            raise SyntaxError(msg)
    g = tokenize.tokenize(io.BytesIO(string.encode('utf-8')).readline)
    pre_op = ''
    for toktype, tokval, _, _, _ in g:
        if toktype == tokenize.NAME and pre_op == '.' and tokval.startswith('_'):
            attr = tokval
            msg = "access to attribute '{0}' is unsafe.".format(attr)
            raise AttributeError(msg)
        elif toktype == tokenize.OP:
            pre_op = tokval

def remove_l(l: dict):
    pl = l
    del_l = []
    for key in pl:
        if "module '" in str(pl[key]):
            del_l.append(key)
    if del_l:
        for key in del_l:
            del pl[key]
    
    return pl

async def get_end_calculate(conde_str: str) -> str:
    repass = ''
    try:
        check_unsafe_attributes(conde_str)
        g = {}
        l = {}
        exec(conde_str, g, l)
        l = remove_l(l)
        repass = "{}".format(l)
    except Exception as e:
        repass = "[Error] {}".format(e)
    
    return repass