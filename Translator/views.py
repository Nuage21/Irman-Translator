from django.shortcuts import render
from django.template.defaulttags import register
from xml.dom import minidom

class LanguagesXml:
    root = minidom.parse('Translator/static/Translator/lng.xml')

    def get(self, lng, attr):
        cur = self.root.getElementsByTagName(lng)
        attfound = True
        if cur:
            att = cur[0].getElementsByTagName(attr)
            if att:
                return att[0].firstChild.data
            else:
                attfound = False
        else:
            att = self.root.getElementsByTagName('en')[0].getElementsByTagName(attr)
            if att:
                return att[0].firstChild.data
            else:
                attfound = False

        if not attfound:
            return 'error: 0x01 ntf!'


LNG = LanguagesXml()


@register.simple_tag
def get_item(obj, lng, attr):
    return obj.get(lng, attr)


def index(req):
    context = {
        'GET_LIST': req.GET,
        'LNG': LNG,
    }
    lg = 'en'
    if req.GET:
        if 'lng' in req.GET:
            lg = req.GET['lng']
    context['cur_lng'] = lg
    return render(req, 'Translator/index.html', context)
