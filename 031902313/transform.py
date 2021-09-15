from pypinyin import lazy_pinyin, Style
from itertools import product
import json


def word_combination(sensitive_word):
    word_list = []
    combination = []
    # print(sensitive_word)
    for i in range(len(sensitive_word)):
        word_list.append([])
    with open('chai_zi.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    if is_chinese(sensitive_word):
        for i in range(len(sensitive_word)):
            word_list[i].append(sensitive_word[i])
            word_list[i].append(''.join(lazy_pinyin(sensitive_word[i])))
            word_list[i].append(''.join(lazy_pinyin(sensitive_word[i], style=Style.FIRST_LETTER)))
            if sensitive_word[i] in data.keys():
                word_list[i].append(data[sensitive_word[i]])
        loop_val = word_list
        for word in product(*loop_val):
            string = ''
            for i in range(len(word)):
                string += word[i]
            combination.append(string)
    else:
        combination.append(sensitive_word)
    return combination


def is_chinese(char):
    if '\u4e00' <= char <= '\u9fa5':
        return True
    else:
        return False


def is_number(char):
    if '\u0030' <= char <= '\u0039':
        return True
    else:
        return False


def is_alphabet(char):
    if ('\u0041' <= char <= '\u005a') or ('\u0061' <= char <= '\u007a'):
        return True
    else:
        return False


def is_other(char):
    if not(is_alphabet(char) or is_number(char) or is_chinese(char)):
        return True
    else:
        return False


if __name__ == '__main__':
    word_combination('法轮功')
