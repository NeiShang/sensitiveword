from transform import *
from main import Filter


class TestClass:
    def test_word_combination(self):
        word = '你好'
        ans = ['你好', '你hao', '你h', '你女子', 'ni好', 'nihao', 'nih', 'ni女子', 'n好', 'nhao', 'nh', 'n女子', '亻尔好',
               '亻尔hao', '亻尔h', '亻尔女子']
        result = word_combination(word)
        assert ans == result

    def test_filter(self):
        sensitive_words = ['操你妈', 'sb']
        text = ['cao妳媽的傻逼S12（b', '扌喿亻尔女马挥洒及我们把手机是你', 's  b就， 扫平今晚我操n嘛年四蛇女cnm']
        ans = 'total: 6\nLine1: <操你妈> cao妳媽\nLine1: <sb> S12（b\nLine2: <操你妈> 扌喿亻尔女马\nLine3: <sb> s  b\n' \
              'Line3: <操你妈> 操n嘛\nLine3: <操你妈> cnm\n'
        test = Filter()
        test.parse_sensitive_words(sensitive_words)
        result = test.sensitive_words_filter(text)
        assert ans == result
