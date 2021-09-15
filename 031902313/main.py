import sys
from transform import *


class Filter:
    def __init__(self):
        self.sensitive_words = {}
        self.delimit = 'end'
        self.sensitive_words_dict = {}

    def parse_sensitive_words(self, path):
        file = open(path, 'r', encoding='utf-8')
        text = file.read()
        sensitive_words_list = text.split('\n')
        count = 0
        for sensitive_words in sensitive_words_list:
            self.sensitive_words_dict[count] = ' <'+sensitive_words+'> '
            combinations = word_combination(sensitive_words)
            for word in combinations:
                self.add_sensitive_words(word, count)
            count += 1

    def add_sensitive_words(self, sensitive_word, count):
        chars = sensitive_word.lower()
        if not chars:
            return
        level = self.sensitive_words
        for i in range(len(chars)):
            if is_chinese(chars[i]):
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

    def sensitive_words_filter(self, input_path, output_path):
        input_file = open(input_path, 'r', encoding='utf-8')
        output_file = open(output_path, 'w+', encoding='utf-8')
        current_row = 0
        total_count = 0
        for line in input_file:
            line_copy = line
            line = line.lower()
            current_row += 1
            start_flag = False
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
                    char = ''.join(lazy_pinyin(char))
                    if char in level:
                        start_flag = True
                        step += 1
                        if self.delimit not in level[char]:
                            level = level[char]
                        else:
                            keywords = line_copy[start:start+step]
                            start += step - 1
                            total_count += 1
                            output_file.write('Line'+str(current_row)+':'
                                              + self.sensitive_words_dict[level[char][self.delimit]] + keywords+'\n')
                            start_flag = False
                            break
                    else:
                        start_flag = False
                        break
                start += 1
        input_file.close()
        output_file.close()
        with open(output_path, "r+", encoding='utf-8') as f:
            old = f.read()
            f.seek(0)
            f.write('total: ' + str(total_count) + '\n')
            f.write(old)


if __name__ == '__main__':
    try:
        org, words, test = sys.argv[1:4]
    except Exception as e:
        print(sys.argv)
        print(e)
    sensitive_filter = Filter()
    sensitive_filter.parse_sensitive_words(sys.argv[1])
    sensitive_filter.sensitive_words_filter(sys.argv[2], sys.argv[3])

