import re
from xml.dom import minidom

# contains rule class declaration
# rule class is a powerful tool to apply grammar/vocab... rules to any string
# rule class works similarly as a regex
# author: @Hakim-Beldjoudi (hbFree) NOV 2019
#
class rule:

    def __init__(self, rmdl):
        self.pattern = rmdl

    # import methods

    # @util.py
    from .util import get_param_tab
    from .util import rm_suffixes
    from .util import tab_rm_suffixes
    from .util import eval_param

    # @split
    from .split import split_inside_bracket
    from .split import or_split

    # @conditional.py
    from .conditionals import is_conditional_el
    from .conditionals import is_model_rest_conditional

    # @match.py
    from .match import it_matches
    from .match import it_matches_or_list
    from .match import no_direct_match_after

    # @apps.py
    from .apps import apply_single_clause_el
    from .apps import apply_clause
    from .apps import apply

    @staticmethod
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


