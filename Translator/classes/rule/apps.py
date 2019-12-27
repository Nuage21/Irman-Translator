import re

# ****************************************************************************
# contains: rule.apply_single_clause (apply one clause only)
#           rule.apply_clause (apply rule)
#           rule.apply (call apply_clause when found a match* apply the rule over a string)
# author: @Hakim-Beldjoudi (hbFree) NOV 2019
# ****************************************************************************


# return the result of applying clause_el (an element of the rule application)
# goes recursive if found a clause_el inside
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

    ignore_classifier = False
    if bracket_modifier == 'nel':
        ignore_classifier = True
        bracket_modifier = 'el'

    if bracket_modifier == 'el':
        is_range = bracket_inside.find(':')
        if is_range > 0:
            min = int(bracket_inside[0:is_range])
            max = self.eval_param(bracket_inside[is_range + 1:], mlen)
            composed = ' '
            while min < max:
                to_add = matched_buf[min]
                if ignore_classifier:
                    to_add = rm_indicators(to_add)
                composed += self.rm_suffixes(to_add) + ' '
                min = min + 1
            return composed

        # if not range
        bracket_inside = self.eval_param(bracket_inside, mlen)

        to_add = matched_buf[int(bracket_inside)]
        if ignore_classifier:
            to_add = self.rm_indicators(to_add)
        return self.rm_suffixes(to_add)

    bracket_param = clause_el[bracket_underscore_index + 1:brck_open]  # ex: pp_2[] param = 2 (depends on 2d el)

    bracket_param = self.eval_param(bracket_param, mlen)  # eval: ex 2r -> mlen-3

    bracket_inside = self.split_inside_bracket(bracket_inside)
    bracket_param_tab = self.get_param_tab(bracket_modifier)  # ex: personal pronouns tab

    for i in range(len(bracket_inside)):
        if self.rm_indicators(matched_buf[bracket_param]) == bracket_param_tab[i]:  # what index stands for
            cur_bracket_el = bracket_inside[i]
            if cur_bracket_el == '0':
                return ''
            elif cur_bracket_el.find('[') < 0:
                return self.rm_suffixes(bracket_inside[i])
            else:
                return self.apply_single_clause_el(matched_buf, cur_bracket_el)
    return ''


# return the result of applying the &clause over the matched buffer
def apply_clause(self, matched_buf, clause):
    plus_index = clause.find('+')
    clen = len(clause)
    if plus_index < 0:
        return self.apply_single_clause_el(matched_buf, clause)
    first_clause_el = clause[0:plus_index]
    first_clause_applied = self.apply_single_clause_el(matched_buf, first_clause_el)
    return first_clause_applied + \
           self.apply_clause(matched_buf, clause[plus_index + 1:clen])


# seek for a match with the rule pattern
# call @apply_clause when found
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
                        parameter = int(is_conditional[1:])  # extract multi-match param ex: |00|?5 -> pa.. = 5
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
