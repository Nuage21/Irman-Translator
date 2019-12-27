
# ****************************************************************************
# contains: rule.split_inside_bracke -> see ^method-description
#           rule.or_split -> split an or separated pattern elements
# author: @Hakim-Beldjoudi (hbFree) NOV 2019
# ****************************************************************************


#  comma split inside bracket params without taking params
#  that are inside a param's bracket as to_split_elements
#  ex: inside= "im_0[0, ab, ...], pp_1[a, b, c, ...], ..." -> ['im_0[0, ab, ...]', 'pp_1[a, b, c, ...]', ...]
#  !would generate unwanted split if we do inside.split(',')
def split_inside_bracket(self, inside):
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


# exemple: |pp|or|v0| -> ['pp', 'v0']
def or_split(self, model_el):
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
