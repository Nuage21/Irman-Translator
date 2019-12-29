import re
from .rule import loader
from .rule.util import adjust_text

def translate_word(word0):
    word = word0.lower()

    w = loader.dico.get(word)

    word_translation = ''
    word_classifier = ''

    if w:
        word_translation = w[0]
        word_classifier = w[1]

    else:
        # treat plural nouns
        if word[-1] == 's':  # ex: houses -> (not found) -> seek house
            word = word[:-1]
            w = loader.dico.get(word)
            if w:
                word_tr = w[0]
                if w[1] == 'nms':
                    word_translation = 'i' + word_tr[1:] + 'en'
                    word_classifier = 'nmp'
                elif w[1] == 'nfs':
                    word_translation = 'ti' + word_tr[1:] + 'in'
                    word_classifier = 'nfp'
    if w:
        return '|' + word_classifier + '|' + word_translation

    return '|99|' + word0


def map_phrase(phrase):  # map a phrase with corespondents
    splitted = re.split(r"[^a-zA-Z0-9'.,]", phrase)
    result = ''
    for word in splitted:
        result = result + ' ' + translate_word(word)
    return result

def app_rules(text0):
    #  apply rules
    text0 = adjust_text(text0)
    result = text0

    rule_app_left = True
    while rule_app_left:
        rule_app_left = False # suppose nothing wd change
        for r in loader.rule_list:
            result, status = r.apply(result)
            if status == 0:  # if smth has changed (rule match found & applied)
                rule_app_left = True

    result = adjust_text(result)
    return result