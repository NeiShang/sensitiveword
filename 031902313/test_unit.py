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
        sensitive_words = ['你好', 'hello']
        text = ['亻尔女子hE’；0llo', '好睡觉哦i你手机n女子，是孔金瓯省亻尔h暑假', '妳；】‘、。好你ha睡觉哦i啊']
        ans = 'total: 6\nLine1: <你好> 亻尔女子\nLine1: <hello> hE’；0llo\nLine2: <你好> n女子\n' \
              'Line2: <你好> 亻尔h\nLine3: <你好> 妳；】‘、。好\nLine3: <你好> 你h\n'
        test = Filter()
        test.parse_sensitive_words(sensitive_words)
        result = test.sensitive_words_filter(text)
        assert ans == result
