import re
from xml.dom import minidom

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
        indicators = re.split(r'[^_a-zA-Z0-9čǧḥḍɛṛṭɣẓṣ-]', splited_line[1])
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

    def or_split(self, model_el):
        # exemple: |pp|or|v0| -> ['pp', 'v0']
        accum = ''
        reslt = []
        i = 0
        while i < len(model_el) - 1:
            if model_el[i:i + 2] == 'or':
                accum = accum.strip()
                reslt.append(accum)
                accum = ''
                i = i + 1
            else:
                accum = accum + model_el[i]
            i = i + 1
        accum = accum + model_el[-1]
        reslt.append(accum)
        return reslt

    def it_matches_or_list(self, word, model_list):
        for model_el in model_list:
            m = self.it_matches(word, model_el)
            if m >= 0:
                return m, model_el
        return -1, 'none'

    def it_matches(self, word, model_el):
        if not model_el:
            return 0

        or_index = model_el.find('or')
        if or_index > 0:
            or_splitted = self.or_split(model_el)
            status, matched_model = self.it_matches_or_list(word, or_splitted)
            return status

        if model_el[0] == '|':  # classification match
            word_closed_classifier = word.rfind('|')
            model_closed_classifier = model_el.rfind('|')

            for i in range(max(word_closed_classifier, model_closed_classifier)):
                if i >= model_closed_classifier:
                    return -1
                elif i >= word_closed_classifier:
                    is_rest_model_conditional = True
                    j = i
                    # (is the rest all conditional ? ex: abc[XXXXX] )
                    while j < model_closed_classifier:
                        if model_el[j] != 'X':
                            is_rest_model_conditional = False
                        j = j + 1
                    if is_rest_model_conditional:
                        return 0
                    else:
                        if model_el[-1] == '?':
                            return 1  # even if no match but conditional
                        return -1
                if model_el[i] != 'X' and model_el[i] != word[i]:  # X matches anything
                    if model_el[-1] == '?':
                        return 1  # even if no match but conditional
                    return -1
            return 0
        # direct match evaluating (omit classification)
        if word[0] == '|':
            if word[word.rfind('|') + 1:] == model_el:  # word matches model
                return 0

        elif word == model_el:  # word matches model
            return 0

        # simple conditional (always match regardless of everything)
        # rem: direct match is prefered over conditional, so that is tested last
        if model_el[-1] == '?':
            return 1  # matches with conditional existence
        return -1

    def is_conditional_el(self, model_el, matched_buf_len):
        # return '' not conditional ex: $12 ?12 => conditional
        if not model_el:
            return False

        cndmark_found = False
        number = 0
        reversed_model_el = model_el[::-1]
        st = 0
        if reversed_model_el[0] == 'r' and (
                reversed_model_el[1].isdigit() or reversed_model_el[1] == '$' or reversed_model_el[1] == '?'):
            st = 1
        mark = '?'
        for letter in reversed_model_el[st:]:
            if letter.isdigit():
                number = 10 * number + int(letter)
            elif letter == '?' or letter == '$':
                mark = letter
                cndmark_found = True
                break
            else:
                break
        if st == 1:
            number = mark + str(matched_buf_len - 1 - number)[::-1]  # ex: 123 -> 321
        else:
            number = mark + str(number)[::-1]  # ex: 123 -> 321
        if cndmark_found:
            return number
        return ''

    def is_model_rest_conditional(self, model, st):  # ex: ['|pp|', |pp|?, |gg|?] -> true from 1
        if st >= len(model):
            return False
        is_cnd = True
        while st < len(model):
            # 5 is optional, just to run the method, since we only interested in True or False
            if not self.is_conditional_el(model[st], 5):
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

    def tab_rm_suffixes(self, tab):
        for i in range(len(tab)):
            tab[i] = self.rm_suffixes(tab[i])
        return tab

    def eval_param(self, param, matched_buf_size):
        # exemple for param = '3r' return third from last, for param = 2 return 2;
        real_param = param
        is_reverse = param.find('r')
        if is_reverse == 0:
            real_param = matched_buf_size - 1
        elif is_reverse > 0:
            real_param = matched_buf_size - 1 - int(param[0:is_reverse])
        real_param = int(real_param)
        return real_param

    def apply_single_clause_el(self, matched_buf, clause_el):
        brck_open = clause_el.find('[')
        brck_close = clause_el.find(']')

        clen = len(clause_el)
        mlen = len(matched_buf)

        conditional_matche = self.is_conditional_el(clause_el, mlen)

        if conditional_matche:
            condition_mark = conditional_matche[0]
            condition_param = int(conditional_matche[1:])

            if condition_param >= len(matched_buf):
                return ''
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

        bracket_underscore_index = clause_el.find('_')
        bracket_modifier_delimiter = brck_open
        if bracket_underscore_index > 0:
            bracket_modifier_delimiter = bracket_underscore_index

        bracket_modifier = clause_el[0:bracket_modifier_delimiter]  # get what inside the []

        bracket_inside = clause_el[brck_open + 1:clause_el.rfind(']')]  # ex el[32] -> 32

        if bracket_modifier == 'el':
            is_range = bracket_inside.find(':')
            if is_range > 0:
                min = int(bracket_inside[0:is_range])
                max = self.eval_param(bracket_inside[is_range + 1:], mlen)
                composed = ' '
                while min < max:
                    composed += self.rm_suffixes(matched_buf[min]) + ' '
                    min = min + 1
                return composed

            # if not range
            bracket_inside = self.eval_param(bracket_inside, mlen)
            return self.rm_suffixes(matched_buf[int(bracket_inside)])

        bracket_param = clause_el[bracket_underscore_index + 1:brck_open]  # ex: pp_2[] param = 2 (depends on 2d el)

        bracket_param = self.eval_param(bracket_param, mlen)  # eval: ex 2r -> mlen-3

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

    def no_direct_match_after(self, model, i, phrase_ctx, j):
        no_match = True
        mlen = len(model)
        plen = len(phrase_ctx)
        tmpi = i
        while j < plen:
            while i < mlen:
                if self.it_matches(phrase_ctx[j], model[i]) == 0:
                    return False
                i = i + 1
            i = tmpi
            j = j + 1
        return no_match

    def apply(self, text):
        err_invalid_pattern = 'invalid pattern'
        err_empty_pat_model = 'pattern model is empty'
        err_no_app = 'rule application clause is empty'
        err_null_patter_or_text = 'rule application clause is empty'
        err_two_point_missing = '\':\' missing after model clause'

        status = -1  # =0 => smth has been applied
        # =-1 => nothing has been applied (same text returned)
        # =1 => an error has occured
        # nothing applied by default

        plen = len(self.pattern)

        if not self.pattern:
            return err_null_patter_or_text, status
        pth1 = self.pattern.find('(', 0)
        if pth1 == -1:
            return err_invalid_pattern, 1  # if clause no parethesed
        pth2 = self.pattern.find(')', pth1)
        if pth2 < pth1:
            return err_invalid_pattern, 1  # if clause unclosed parenthese
        if pth2 == pth1 + 1:
            return err_empty_pat_model, 1  # nothing inside if clause
        if pth2 == plen - 1:
            return err_no_app, 1  # no if clause application
        if self.pattern[pth2 + 1] != ':':
            return err_two_point_missing, 1  # : missing

        # ERRORS_TREATED

        def correct_matched_buf(buf):
            # no match at all (not direct, not conditional)
            buf = self.tab_rm_suffixes(buf)

            # remove conditionally loaded into matched_buf
            for k in range(len(buf)):
                if buf[k] == '|$$|':
                    buf[k] = ''
            return buf

        # get model context
        pmodel_ctx = self.pattern[pth1 + 1:pth2].split('>')
        text_ctx = re.split(r"[^a-zA-z0-9ɣ'čǧḥḍɛṛṭɣẓṣ$ḥ|?,-]+", text)
        multiple_matches_recorder = 0
        i = 0  # iterates over model_els
        j = 0  # to keep text_ctx current pos
        matched_buf = []
        result = ''

        match_st = -1
        def set_match_st():
            nonlocal match_st
            if match_st < 0:
                match_st = j

        while j < len(text_ctx):
            word = text_ctx[j]

            if multiple_matches_recorder == 1:  # max conditionals reached
                i = i + 1
                multiple_matches_recorder = 0

            matches = self.it_matches(word, pmodel_ctx[i])

            if matches == 0:
                matched_buf.append(word)
                i = i + 1
                set_match_st()

            elif matches == 1:
                cd = '$'
                if i + 1 < len(pmodel_ctx):
                    if self.it_matches(word, pmodel_ctx[i + 1]) == 0:
                        matched_buf.append('|$$|$')  # $ for single conditional matching
                        cd = ''
                        i = i + 1
                matched_buf.append(word + cd)  # $ for single conditional matching
                i = i + 1
                set_match_st()

            else:
                is_conditional = self.is_conditional_el(pmodel_ctx[i], 5)  # 5 is optional
                if is_conditional:  # multi-conditional
                    set_match_st()
                    if self.it_matches(word, pmodel_ctx[i + 1]) == 0:
                        # two conditions to stop evaluating multiple conditionals
                        # 1. we reach the max of multiples
                        # 2. next pattern_el typo matches with current word
                        i = i + 2
                        multiple_matches_recorder = 0
                        matched_buf.append(word)
                    else:
                        if multiple_matches_recorder > 1:
                            matched_buf.append(word + '$')
                            multiple_matches_recorder = multiple_matches_recorder - 1
                        else:
                            parameter = int(is_conditional[1:]) # extract multi-match param ex: |00|?5 -> pa.. = 5
                            matched_buf.append(word + '$')
                            multiple_matches_recorder = parameter  # already affected one

                else:
                    j = j + 1

                    if match_st >= 0:
                        matched_buf = [matched_buf[0], ]
                        j = match_st + 1
                        word = ''  # don't add word

                    matched_buf = correct_matched_buf(matched_buf)
                    result = result + ' ' + ' '.join(matched_buf) + ' ' + word + ' '
                    matched_buf.clear()
                    match_st = -1
                    i = 0
                    continue

            conditional_app = self.is_model_rest_conditional(pmodel_ctx, i) and self.no_direct_match_after(pmodel_ctx,
                                                                                                           i, text_ctx,
                                                                                                           j)
            j = j + 1  # word pos at text_ctx goes next

            if conditional_app:
                for k in range(len(pmodel_ctx) - i):
                    matched_buf.append('|$$|$')

            if i == len(pmodel_ctx) or conditional_app:
                status = 0  # smth has changed

                # remove indicators
                for k in range(len(matched_buf)):
                    matched_buf[k] = rm_indicators(matched_buf[k])

                # apply to match
                st = pth2 + 2  # skip ):
                model_clause = self.pattern[st:plen]
                applied = self.apply_clause(matched_buf, model_clause)
                result = result + ' ' + applied + ' '
                i = 0
                match_st = -1
                matched_buf.clear()

        matched_buf = correct_matched_buf(matched_buf)
        result = (result + ' ' + ' '.join(matched_buf)).strip()
        return result, status  # remove sides spaces

def xml_load_rule_list():
    rules_list = []
    root = minidom.parse('Translator/static/Translator/translation_data/en_tz/rules.xml')
    for rule_node in root.getElementsByTagName('rule'):
        rule_core = str(rule_node.firstChild.data).rstrip()
        rules_list.append(rule(rule_core))
    return rules_list


rule_list = xml_load_rule_list()


def translate_word(word0):
    word = word0.lower()

    w = dico.get(word)

    word_translation = ''
    word_classifier = ''

    if w:
        word_translation = w[0]
        word_classifier = w[1]

    else:
        # treat plural nouns
        if word[-1] == 's':  # ex: houses -> (not found) -> seek house
            word = word[:-1]
            w = dico.get(word)
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


def translate_stage0(phrase):  # map a phrase with corespondents
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
    text0 = adjust_text(text0)
    result = text0

    rule_app_left = True
    while rule_app_left:
        rule_app_left = False # suppose nothing wd change
        for r in rule_list:
            result, status = r.apply(result)
            if status == 0:  # if smth has changed (rule match found & applied)
                rule_app_left = True

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
                bar_ind0 = -1
                after_bar = ''
        else:
            if bar_ind0 >= 0:
                after_bar = after_bar + letter
            else:
                result = result + letter
        i = i + 1
    return result
