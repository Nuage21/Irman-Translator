from .data import personal_p
from .data import iam
import re

def get_param_tab(self, param):
    if param == 'pp':
        return personal_p
    if param == 'im':
        return iam


def rm_suffixes(self, word):
    # ex: |pp|?12 -> |pp|
    i = len(word) - 1
    must_slice = False
    while i >= 0:
        if word[i] == '?' or word[i] == '$':
            must_slice = True
            break
        i = i - 1
    if must_slice:
        return word[0:i]
    return word


def tab_rm_suffixes(self, tab):
    # rm suffixes from a list
    for i in range(len(tab)):
        tab[i] = self.rm_suffixes(tab[i])
    return tab


def eval_param(self, param, matched_buf_size):
    # exemple for param = '3r' return third from last, for param = 2 return 2;
    real_param = param.strip()
    is_reverse = param.find('r')
    if is_reverse == 0:
        real_param = matched_buf_size - 1
    elif is_reverse > 0:
        real_param = matched_buf_size - 1 - int(param[0:is_reverse])
    real_param = int(real_param)
    return real_param

def adjust_text(txt):
    #  remove multiple spaces and strip
    txt = re.sub(' +', ' ', txt)
    return txt.strip()
