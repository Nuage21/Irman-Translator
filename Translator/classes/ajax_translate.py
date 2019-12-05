from django.http import JsonResponse
from .rule import *


def translate(req):
    msg = req.GET['msg']
    msg = str(msg)

    msg2 = ''  # current result

    if msg:
        msg0 = translate_stage0(msg)
        msg1 = translate_stage1(msg0)
        msg2 = rm_indicators(msg1)

    data = {
        'tmsg': msg2
    }
    return JsonResponse(data)
