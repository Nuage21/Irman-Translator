# ****************************************************************************
# contains: rule.it_matches -> return -1/0/1 for no-match/match/conditional-match
#           rule.it_matches_or_list -> return match_status, what matched from an or splitted pattern element
#           rule.no_direct_match_after -> no direct match after i_included of phrase_ctx from j_included
# author: @Hakim-Beldjoudi (hbFree) NOV 2019
# ****************************************************************************

# IMPORTANT:
# multi-conditional gives -1 if no direct match
# if conditional but match directly then this last is prefered (returned)
#
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


# does word match any of model_list ? if yes
def it_matches_or_list(self, word, model_list):
    for model_el in model_list:
        m = self.it_matches(word, model_el)
        if m >= 0:
            return m, model_el
    return -1, 'none'


# explicit method name!
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
