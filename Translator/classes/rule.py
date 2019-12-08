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


def load_dico():
    dico_file = open("Translator/static/Translator/translation_data/en_tz/dico.txt", encoding='utf-8')
    dico = {}

    for line in dico_file:
        line = str(line)
        splited_line = line.split(':')
        key = splited_line[0]
        indicators_tab = []
        indicators = re.split(r'[^a-zA-Z0-9čǧḥɛṛṭɣẓṣ-]', splited_line[1])
        for i in indicators:
            if i:
                indicators_tab.append(i)
        dico[key] = indicators_tab

    dico_file.close()
    return dico


dico = load_dico()


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
        if param == 'im':
            return iam

    def it_matches(self, word, model_el):
        if not model_el:
            return 0
        if model_el[0] == '|':  # condition model
            if word[0:4] == model_el[0:4]:
                return 0
        if word == model_el:  # word matches model
            return 0
        if model_el[-1] == '?':
            return 1  # matches with conditional existence
        return -1

    def is_conditional_el(self, model_el):
        # return '' not conditional else ex: $12 ?12 => conditional
        cndmark_found = False
        number = 0
        reversed_model_el = model_el[::-1]
        mark = '?'
        for letter in reversed_model_el:
            if letter.isdigit():
                number = 10 * number + int(letter)
            elif letter == '?' or letter == '$':
                mark = letter
                cndmark_found = True
                break
            else:
                break
        number = mark + str(number)[::-1]  # ex: 123 -> 321
        if cndmark_found:
            return number
        return ''

    def is_model_rest_conditional(self, model, st):  # ex: ['|pp|', |pp|?, |gg|?] -> true from 1
        if st >= len(model):
            return False
        is_cnd = True
        while st < len(model):
            if not self.is_conditional_el(model[st]):
                is_cnd = False
            st = st + 1
        return is_cnd

    def rm_suffixes(self, word):
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

    def apply_single_clause_el(self, matched_buf, clause_el):
        brck_open = clause_el.find('[')
        brck_close = clause_el.find(']')

        clen = len(clause_el)

        conditional_matche = self.is_conditional_el(clause_el)

        if conditional_matche:
            condition_mark = conditional_matche[0]
            condition_param = int(conditional_matche[1:])

            target_pattern_el = matched_buf[condition_param]

            if condition_mark == '?' and target_pattern_el[-1] == '$':
                return ''
            if condition_mark == '$':
                if target_pattern_el[-1] != '$':
                    return ''


        #  now either not conditional or ?conditional&exist or
        if brck_open < 0 and brck_close < 0:  # no bracket
            return self.rm_suffixes(clause_el)

        if brck_close < brck_open or brck_open < 2:
            return '[exception: invalid model clause non closed bracket]'
        bracket_modifier = clause_el[0:2]  # get what inside the []

        if bracket_modifier == 'el':
            bracket_inside = clause_el[3:clause_el.find(']')]  # ex el[32] -> 32
            return self.rm_suffixes(matched_buf[int(bracket_inside)])

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
                    return self.rm_suffixes(bracket_inside[i])
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
        return first_clause_applied + \
               self.apply_clause(matched_buf, clause[plus_index + 1:clen])

    def apply(self, text):
        invalid_pattern_except = 'invalid pattern'
        empty_pat_model_except = 'pattern model is empty'
        no_app_except = 'rule application clause is empty'
        two_point_missing_except = '\':\' missing after model clause'
        exct = 'exception: '

        plen = len(self.pattern)

        if not self.pattern:
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
        text_ctx = re.split(r"[^a-zA-z0-9ɣ'č.$ḥ|?,-]+", text)

        i = 0
        matched_buf = []
        result = ''
        for word in text_ctx:
            matches = self.it_matches(word, pmodel_ctx[i])

            if matches == 0:
                matched_buf.append(word)
                i = i + 1
            elif matches == 1:
                matched_buf.append(word + '$')  # $ for conditional matching
                i = i + 1
            else:
                result = result + ' '.join(matched_buf) + ' ' + word
                matched_buf.clear()
                i = 0

            conditional_app = ((i == len(text_ctx)) and self.is_model_rest_conditional(pmodel_ctx, i))
            if conditional_app:
                for j in range(len(pmodel_ctx) - i):
                    matched_buf.append('|$$|$')

            if i == len(pmodel_ctx) or conditional_app:
                # remove indicators
                for j in range(len(matched_buf)):
                    matched_buf[j] = (matched_buf[j])[4:]
                # apply to match
                st = pth2 + 2  # skip ):
                model_clause = self.pattern[st:plen]
                applied = self.apply_clause(matched_buf, model_clause)
                result = result + ' ' + applied
                i = 0
                matched_buf.clear()

        result = (result + ' ' + ' '.join(matched_buf)).strip()
        return result  # remove sides spaces


rule0 = rule('if(|pp|>|0v|>|pp|?):'
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
             'pp_2[-iyi,-k,-kem,-t,-t,-aɣ,-aɣ,kun,kunt, iman-nsen,tent]'
             ']?2+ +el[2]$2')

rule1 = rule('if(|im|>|cv|):'
             'el[0]+ +'
             'im_0[0,t-,t-,i,t,n-,n-,t-,t-,0,0]'
             '+el[1]'
             '+im_0[eɣ,ed,ed,0,0,0,0,em,emt,en,ent]')

def translate_word(word):
    for w in dico:
        w = dico.get(word.lower())
        if w:
            return '|' + w[1] + '|' + w[0]
        return '|99|' + word


def translate_stage0(phrase):
    splitted = re.split(r"[^a-zA-Z0-9'.,]", phrase)
    result = ''
    for word in splitted:
        result = result + ' ' + translate_word(word)
    return result


def adjust_text(txt):
    #  remove multiple spaces and strip
    txt = re.sub(' +', ' ', txt)
    return txt.strip()


def translate_stage1(text0):
    #  apply rules
    text0 = text0.strip()
    result = rule0.apply(text0)
    result = rule1.apply(result)

    result = adjust_text(result)
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
