from django.http import JsonResponse
from . import en_tz_translate as tr
from .rule import rule
from .rule.util import adjust_text


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
                ph = tr.adjust_text(ph)
                ph0 = tr.map_phrase(ph)
                ph1 = tr.app_rules(ph0)
                ph2 = rule.rm_indicators(ph1)
                if res:
                    res = res + ', '
                res = res + ph2

    data = {
        'tmsg': res
    }

    return JsonResponse(data)
