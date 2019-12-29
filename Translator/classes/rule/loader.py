from xml.dom import minidom
import re
from . import rule

# ****************************************************************************
# contains: load_dico -> load dico from text file dico.txt
#           xml_load_rule_list -> load rules into a list from xml holder
# author: @Hakim-Beldjoudi (hbFree) NOV 2019
# ****************************************************************************

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


def xml_load_rule_list():
    rules_list = []
    root = minidom.parse('Translator/static/Translator/translation_data/en_tz/rules.xml')
    for rule_node in root.getElementsByTagName('rule'):
        rule_core = str(rule_node.firstChild.data).rstrip()
        adjusted_rule_core = ''
        in_comment = False  # reading inside a comment ?
        un_permitted = ['\n', '\r', '\t']
        for letter in rule_core:
            if letter in un_permitted:
                continue
            else:
                if letter == '#':
                    in_comment = not in_comment
                elif not in_comment:
                    adjusted_rule_core += letter
        rules_list.append(rule(adjusted_rule_core))
    return rules_list


# load dico & rules
dico = load_dico()
rule_list = xml_load_rule_list()
