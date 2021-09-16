import sys
from transform import *


class Filter:
    def __init__(self):
        self.sensitive_words = {}  # 敏感词树
        self.delimit = 'end'  # 结束符
        self.sensitive_words_dict = {}  # 敏感词字典，配合结束符判断敏感词类型

    def parse_sensitive_words(self, sensitive_words_list):  # 构建敏感词字典，并获得敏感词组合用于构建敏感词树
        count = 0
        for sensitive_word in sensitive_words_list:
            self.sensitive_words_dict[count] = ' <' + sensitive_word + '> '  # 增加敏感词字典
            combinations = word_combination(sensitive_word)  # 获得敏感词组合
            for word in combinations:
                self.add_sensitive_words(word, count)  # 构建敏感词树
            count += 1

    def add_sensitive_words(self, sensitive_word, count):  # 构建敏感词树
        chars = sensitive_word.lower()
        if not chars:
            return
        level = self.sensitive_words
        for i in range(len(chars)):
            if is_chinese(chars[i]):  # 判断是否是汉字，如果是汉字转换为拼音
                word_pinyin = ''.join(lazy_pinyin(chars[i]))
            else:
                word_pinyin = chars[i]
            if word_pinyin in level:
                level = level[word_pinyin]
            else:
                if not isinstance(level, dict):
                    break
                last_level, last_char = level, chars[i]
                for k in range(i, len(chars)):
                    if is_chinese(chars[k]):
                        word_pinyin = ''.join(lazy_pinyin(chars[k]))
                    else:
                        word_pinyin = chars[k]
                    level[word_pinyin] = {}
                    last_level, last_char = level, word_pinyin
                    level = level[word_pinyin]
                last_level[last_char] = {self.delimit: count}
                break
            if i == len(chars) - 1:
                level[self.delimit] = count

    def sensitive_words_filter(self, org_file):  # 敏感词检测
        current_row = 0
        total_count = 0
        content = ''
        for line in org_file:
            line_copy = line
            line = line.lower()
            current_row += 1
            start_flag = False  # start_flag 用来标记是否已经进入敏感词树
            start = 0
            while start < len(line):
                level = self.sensitive_words
                step = 0
                for char in line[start:]:
                    if not start_flag and is_other(char):
                        break
                    if start_flag and is_other(char):
                        step += 1
                        continue
                    char = ''.join(lazy_pinyin(char))  # 将汉字转换成拼音
                    if char in level:
                        start_flag = True
                        step += 1
                        if self.delimit not in level[char]:
                            level = level[char]
                        else:
                            keywords = line_copy[start:start + step]
                            start += step - 1
                            total_count += 1
                            content = "{}{}{}{}{}{}{}".format(content, 'Line', str(current_row), ':',
                                                              self.sensitive_words_dict[
                                                                  level[char][self.delimit]], keywords, '\n')
                            start_flag = False
                            break
                    else:
                        start_flag = False
                        break
                start += 1
        content = "{}{}".format('total: ' + str(total_count) + '\n', content)
        return content


if __name__ == '__main__':
    try:
        org, words, test = sys.argv[1:4]
    except Exception as e:
        print(e)
        exit(0)
    sensitive_filter = Filter()
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        text = f.read()
        sensitive_words = text.split('\n')
        sensitive_filter.parse_sensitive_words(sensitive_words)
    with open(sys.argv[2], 'r', encoding='utf-8') as input_file:
        text = input_file.read()
        input_content = text.split('\n')
        ans = sensitive_filter.sensitive_words_filter(input_content)
    with open(sys.argv[3], 'w+', encoding='utf-8') as output_file:
        output_file.write(ans)
