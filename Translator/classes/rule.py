import re

personal_p = [
    'nekki',
    'kečči',
    'kemmi',
    'netta',
    'nettat',
    'nekni',
    'nukentti',
    'kenwi',
    'kuntti',
    'nutni',
    'nutentti',
]
iam = [
    'aqli',
    'aqlik',
    'aqlikem',
    'atan',
    'attan',
    'aqlaɣ',
    'aqlaɣ',
    'aqlikun',
    'aqlikunt',
    'ahnad',
    'ahnttad',
]
dico = {
    'i': ['nekki','pp'],
    'u': ['kečči', 'pp'],
    'you': ['kečči', 'pp'],
    'you_f': ['kemmi', 'pp'],
    'he': ['netta', 'pp'],
    'she': ['nettat', 'pp'],
    'it': ['netta', 'pp'],
    'you_p': ['kenwi', 'pp'],
    'you_pf': ['kuntti', 'pp'],
    'we': ['nekni', 'pp'],
    'we_f': ['nukentti', 'pp'],
    'they': ['nutni', 'pp'],
    'they_f': ['nutentti', 'pp'],
    'still': ['mazal', '0v'],
    'but': ['maca', 'oa'],
    'why': ['ayɣer', 'qs'],
    'love': ['ḥemel', '0v'],
    'drink': ['sw', '0v'],
    'banana': ['banan', '0n'],
    'kill': ['nɣ', '0v'],
    'cry': ['ttru', '0v'],
    'hit': ['wet', '0v'],
    'to': ['akken', 'to'],
    'suicide': ['swisid', '0v'],
    'hate': ['kerh', '0v'],
    'a': ['d-', '0p'],
    'so': ['bezzaf', '0b'],
    'much': ['mliḥ', '0b'],
    'hard': ['yu3er', '0b'],
    'too': ['bezzaf', '0b'],
    'this': ['wagi', '0d'],
    'become': ['ql', '0v'],
    'is': ['d', '0v'],
    'donkey': ['aɣyul', '0n'],
    'will': ['ad', '0f'],
    'myself': ['iman-iw', 'dp'],
    'yourself': ['iman-ik', 'pp'],
    'himself': ['iman-is', 'pp'],
    'themseves': ['iman-nsen', 'pp'],
    'ourselves': ['iman-neɣ', 'pp'],
    'crying': ['tettru', '0v'],
    'going': ['deg-webrid', '0c'],
    'won\'t': ['g-ttili-ara', '0s'],
    'be': ['til', '0v'],
    'walking': ['tedduɣ', '0v'],
    'eating': ['tečče', '0v'],
    'want': ['bɣ', '0v'],
    'i\'m': ['aqli', 'cv'],
    'you\'are': ['aqlik', 'cv'],
    'he\'s': ['atan', 'cv'],
    'she\'s': ['attan', 'cv'],
    'we\'are': ['aqlaɣ', 'cv'],
    'they\'are': ['ahnad', 'cv'],
}

def translate_word(word):
    for w in dico:
        w = dico.get(word.lower())
        if w:
            return '|'+w[1]+'|'+w[0]
        return word
def translate_stage0(text):
    splitted = re.split(r"[^a-zA-Z0-9'.,]", text)
    result = ''
    for word in splitted:
        result = result + ' ' + translate_word(word)
    return result

class rule:
    pattern = ''

    def __init__(self, rmdl):
        self.pattern = rmdl

    def split_inside_bracket(self, inside):
        #  comma split inside bracket params without taking params
        #  that are inside a param's bracket as to_split elements

        splitted = []
        el = ''
        inside_bracket = 0
        for letter in inside:
            if letter == '[':
                inside_bracket = inside_bracket + 1
            if letter == ']':
                inside_bracket = inside_bracket - 1
            if letter == ',' and inside_bracket == 0:
                splitted.append(el)
                el = ''
            else:
                el = el + letter
        return splitted
    def get_param_tab(self, param):
        if param == 'pp':
            return personal_p
        if param == 'cv':
            return iam

    def it_matches(self, word, model_el):
        if not model_el:
            return True
        if (len(word) < 5):
            return False
        if model_el[0] == '|':  # condition model
            return word[0:4] == model_el
        return word == model_el  # word matches model

    def apply_single_clause_el(self, matched_buf, clause_el):
        brck_open = clause_el.find('[')
        brck_close = clause_el.find(']')

        clen = len(clause_el)

        if brck_open < 0 and brck_close < 0:  # no bracket
            return clause_el
        if brck_close < brck_open or brck_open < 2:
            return '[exception: invalid model clause non closes bracket]'
        bracket_modifier = clause_el[0:2]  # get what inside the []

        if bracket_modifier == 'el':
            bracket_inside = clause_el[3:clen - 1]
            return matched_buf[int(bracket_inside)]

        bracket_inside = clause_el[5:clen - 1]  # get what inside the []
        bracket_param = int(clause_el[3:4])  # ex: pp_2[] param = 2 (depends on 2d el)

        bracket_inside = self.split_inside_bracket(bracket_inside)
        bracket_param_tab = self.get_param_tab(bracket_modifier)  # ex: personal pronouns tab

        for i in range(len(bracket_inside)):
            if matched_buf[bracket_param] == bracket_param_tab[i]:  # what index stands for
                cur_bracket_el = bracket_inside[i]
                if cur_bracket_el == '0':
                    return ''
                elif cur_bracket_el.find('[') < 0:
                    return bracket_inside[i]
                else:
                    return self.apply_single_clause_el(matched_buf, cur_bracket_el)
        return ''

    def apply_clause(self, matched_buf, clause):
        plus_index = clause.find('+')
        clen = len(clause)
        if plus_index < 0:
            return self.apply_single_clause_el(matched_buf, clause)
        first_clause_el = clause[0:plus_index]
        first_clause_applied = self.apply_single_clause_el(matched_buf, first_clause_el)
        return first_clause_applied +\
               self.apply_clause(matched_buf, clause[plus_index+1:clen])

    def apply(self, text):

        invalid_pattern_except = 'invalid pattern'
        empty_pat_model_except = 'pattern model is empty'
        no_app_except = 'rule application clause is empty'
        two_point_missing_except = '\':\' missing after model clause'
        exct = 'exception: '

        plen = len(self.pattern)

        if (not text) or (not self.pattern):
            return 'exception: null pattern or text'
        pth1 = self.pattern.find('(', 0)
        if pth1 == -1:
            return exct + invalid_pattern_except
        pth2 = self.pattern.find(')', pth1)
        if pth2 < pth1:
            return exct + invalid_pattern_except
        if pth2 == pth1 + 1:
            return exct + empty_pat_model_except
        if pth2 == plen - 1:
            return exct + no_app_except
        if self.pattern[pth2 + 1] != ':':
            return exct + two_point_missing_except
        # get model context
        pmodel_ctx = self.pattern[pth1 + 1:pth2].split('>')
        text_ctx = re.split(r"[^a-zA-z0-9ɣ'ḥč.$|,-]+", text)

        i = 0
        matched_buf = []
        result = ''


        for word in text_ctx:
            if self.it_matches(word, pmodel_ctx[i]):
                matched_buf.append(word)
                i = i + 1
            else:
                result = result + ' '.join(matched_buf) + ' ' + word
                matched_buf.clear()
                i = 0
            if i == len(pmodel_ctx):
                for j in range(len(matched_buf)):
                    matched_buf[j] = (matched_buf[j])[4:]
                # apply to match
                st = pth2 + 2  # skip ):
                model_clause = self.pattern[st:plen]
                applied = self.apply_clause(matched_buf, model_clause)
                result = result + ' ' + applied
                i = 0
                matched_buf.clear()

        result = result + ' ' + ' '.join(matched_buf)
        return result

rule0 = rule('if(|pp|>|0v|>|pp|):'
                'pp_0[0,t-,t-,i,t,n-,n-,t-,t-,0,0]'
                '+el[1]'
                '+pp_0[eɣ,ed,ed,0,0,0,0,em,emt,en,ent]'
                '+pp_0['
                'pp_2[-imaniw,-k,-kem,-t,-t, nekni, nukentti,ken,kentt,ten,tent],'
                'pp_2[-iyi, imanik,0,-t,-t,-aɣ,-aɣ, wigi, tigi,-ten,-tent],'
                'pp_2[-iyi, wagi, imanim,-t,-t,-aɣ,-aɣ, wigi, tigi,-ten,-tent],'
                'pp_2[-iyi,-ik,-ikem,-t,-t,-aɣ,-aɣ,-iken,-ikent,-iten,-itent],'
                'pp_2[-iyi,-ik,-ikem,-t,-t,-aɣ,-aɣ,-iken,-ikent,-iten,-itent],'
                'pp_2[-iyi,-ik,-ikem,-t,-t,-aɣ,-aɣ,-iken,-ikent,-iten,-itent],'
                'pp_2[-iyi,-ik,-ikem,-t,-t,-aɣ,-aɣ,-iken,-ikent,-iten,-itent],'
                'pp_2[-iyi, wagi, tagi,-t,-t,-aɣ,-aɣ, imanwen, tigi,-ten,tent],'
                'pp_2[-iyi, wagi, tagi,0,0,-aɣ,-aɣ, wigi, imanwent,-ten,tent],'
                'pp_2[-iyi,-k,-kem,-t,-t,-aɣ,-aɣ,kun,kunt, iman-nsen,tent],'
                ']')

rule1 = rule('if(|pp|>|0v|):'
                'pp_0[0,t-,t-,i,t,n-,n-,t-,t-,0,0]'
                '+el[1]'
                '+pp_0[eɣ,ed,ed,0,0,0,0,em,emt,en,ent]')

rule2 = rule('if(|cv|>|0v|):'
                'el[0]+ +'
                'cv_0[0,t-,t-,i,t,n-,n-,t-,t-,0,0]'
                '+el[1]'
                '+cv_0[eɣ,ed,ed,0,0,0,0,em,emt,en,ent]')

def translate_stage1(text0):
    #  apply rules
    result = rule0.apply(text0)
    result = rule1.apply(result)
    return result

def rm_indicators(text):
    bar_ind0 = -1
    i = 0
    result = ''
    after_bar = ''
    for letter in text:
        if letter == '|':
            if bar_ind0 < 0:
                bar_ind0 = i
            else:
                if i - bar_ind0 != 3:
                    result = result + after_bar
                bar_ind0 = -1
                after_bar = ''
        else:
            if bar_ind0 >= 0:
                after_bar = after_bar + letter
            else:
                result = result + letter
        i = i + 1
    return result


