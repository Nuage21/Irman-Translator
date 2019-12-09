from django.http import JsonResponse
from .rule import *


def translate(req):
    msg = req.GET['msg']
    msg = str(msg)

    res = ''  # current result

    if msg:
        sentences = msg.split('.')
        for sent in sentences:
            if res:
                res = res + '. '
            phrases = sent.split(',')
            for ph in phrases:
                ph = adjust_text(ph)
                ph0 = translate_stage0(ph)
                ph1 = translate_stage1(ph0)
                ph2 = rm_indicators(ph1)
                if res:
                    res = res + ', '
                res = res + ph2

    data = {
        'tmsg': res
    }

    return JsonResponse(data)
