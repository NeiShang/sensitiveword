import sys
import time
from transform import *
time1 = time.time()


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
            self.sensitive_words_dict[count] = sensitive_words
            combinations = word_combination(sensitive_words)
            for word in combinations:
                self.add_sensitive_words(word, count)
            count += 1

    def add_sensitive_words(self, sensitive_word, count):
        sensitive_word = sensitive_word.lower()
        chars = sensitive_word.strip()
        if not chars:
            return
        level = self.sensitive_words
        for i in range(len(chars)):
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break
                last_level, last_char = level, chars[i]
                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: count}
                break
            if i == len(chars) - 1:
                level[self.delimit] = 0

    def sensitive_words_filter(self, path):
        file = open(path, 'r', encoding='utf-8')
        current_row = 0
        total_count = 0
        for line in file:
            line_copy = line
            line.lower()
            current_row += 1
            keywords = []
            start = 0
            while start < len(line):
                level = self.sensitive_words
                step = 0
                for char in line[start:]:
                    #  中文敏感词可能进行一些伪装，在敏感词中插入除字母、数字、换行的若干字符仍属于敏感词  符号
                    #  英文文本不区分大小写，在敏感词中插入若干空格、数字等其他符号(换行、字母除外)    数字+符号
                    if len(keywords) == 0 and is_other(char):
                        continue
                    if len(keywords) != 0 and is_other(char):
                        step += 1
                        continue
                    if char in level:
                        step += 1
                        keywords.append(char)
                        if self.delimit not in level[char]:
                            level = level[char]
                        else:
                            start += step - 1
                            # keywords.clear()
                            # for i in line_copy[start:start+step]:
                            #     keywords.append(i)
                            start += step - 1
                            total_count += 1
                            print('行数'+str(current_row)+':'+''.join(keywords)+' '
                                  + self.sensitive_words_dict[level[char][self.delimit]])
                            keywords.clear()
                            break
                    else:
                        keywords.clear()
                        break
                start += 1
        print(total_count)


if __name__ == '__main__':
    try:
        org, words, test = sys.argv[1:4]
    except Exception as e:
        print(sys.argv)
        print(e)
    sensitive_filter = Filter()
    sensitive_filter.parse_sensitive_words('words.txt')
    sensitive_filter.sensitive_words_filter('org.txt')
    j = json.dumps(sensitive_filter.sensitive_words, ensure_ascii=False)
    print(j)
    time2 = time.time()
    print('总共耗时:' + str(time2 - time1) + 's')



