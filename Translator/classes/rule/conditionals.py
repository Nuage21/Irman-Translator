# ****************************************************************************
# contains: rule.is_conditional_el -> ret condition-mark + int-param if &model_el is conditional, False if not
#           rule.is_model_rest_conditional -> return True if all remaining model_els from &st(included) are conditional
# author: @Hakim-Beldjoudi (hbFree) NOV 2019
# ****************************************************************************


# return '' not conditional ex: $12 ?12 => conditional
def is_conditional_el(self, model_el, matched_buf_len):
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
    return False


# All remaining are conditional ?
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
