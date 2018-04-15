#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
该模块对页面内容特征化，并归一化后存入数据库

'''

import sys
import os

from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

out = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(out)
from db.db_process import MyProcess

reload(sys)
sys.setdefaultencoding('utf-8')


class WordFeature(MyProcess):
    # 继承了 数据库处理的类

    def __init__(self):
        super(WordFeature, self).__init__()
        # data格式为:["word1 word2 word3",
        #             "word4 word5 word6",
        #             "word7 word8 word9"
        #          ]

    # 结合cut_words方法将所有part进行整合以便tfidf算法可以直接接收
    def prepare_data(self):
        # data格式为:["word1 word2 word3",
        #             "word4 word5 word6",
        #             "word7 word8 word9"
        #          ]
        print '-----------We are preparing data from database-------------'
        train_data = self.get_phish_word() # 获取全部钓鱼词语
        data = map(lambda tup: tup[1], train_data)
        # filter_data = filter(lambda words: len(words.split(' '))>10, data)  # 除去词数小10的text
        print 'We finish preparing! \n'
        return data

    # 用tfidf将对每个part中的所有词进行特征化
    def tfidf_feature(self, data):
        # return [{'the':1, 'are':3, 'name':1}, {'the':0, 'are':1, 'name':5}, ...]
        print '----------We are trying to transform these data by tfidf now------------'
        dct_list = []  # 存储所有text中tfidf值
        vector = CountVectorizer(stop_words='english')  # 去除英文停用词
        transformer = TfidfTransformer()
        tfidf = transformer.fit_transform(vector.fit_transform(data))
        word = vector.get_feature_names()
        weight = tfidf.toarray()
        for i in range(len(weight)):
            dct = {}  # 每一个text的tfidf值
            # print '-----------------output ' + str(i) + ' text---------------------------'
            for j in range(len(word)):
                if weight[i][j] == 0.0:
                    # 去除分值为0的word和值
                    continue
                else:
                    dct[word[j]] = weight[i][j]
            dct_list.append(dct)
        print 'We finish the transform! \n'
        return dct_list

    # 对每个特征进行次数统计(暂时用不到)
    def counter_feature(self, data):
        # return [{'the':1, 'are':3, 'name':1}, {'the':0, 'are':1, 'name':5}, ...]
        print '----------We are trying to transform these data by counter now------------'
        dct_list = []  # 存储所有text中tfidf值
        vector = CountVectorizer()  # 去除英文停用词
        counter_matrix = vector.fit_transform(data)
        word_list = vector.get_feature_names()
        counter_ndarray = counter_matrix.toarray()
        # for i in range(len(counter_ndarray)):
        #     dct = {}  # 每一个text的tfidf值
        #     # print '-----------------output ' + str(i) + ' text---------------------------'
        #     for j in range(len(word)):
        #         if weight[i][j] == 0.0:
        #             # 去除分值为0的word和值
        #             continue
        #         else:
        #             dct[word[j]] = weight[i][j]
        #     dct_list.append(dct)
        print 'We finish the transform! \n'
        # return dct_list
        return word_list

    # 提取每个word_list的前几个word的前几个作为feature
    def every_head_feature(self, dct_list):
        # return set([u'this', u'and', u'second', u'third', u'first'])
        # feature_num [(u'second', 0.85322573614527841), (u'this', 0.27230146752334033), (u'first', 0.54197656972645725)...]
        print "------------We need to extract the front N feature-------------"
        feature_value = []
        num = 5  # 规定每个text前多少个词
        for dct in dct_list:
            lst = sorted(dct.items(), key=lambda tup: tup[1], reverse=True)
            text_i = lst[:num]
            feature_value.extend(text_i)
        feature_list = list(set(map(lambda tup: tup[0], feature_value)))
        print 'finish the extract! \n'
        return feature_list

    # 提取总体特征的前多少个词，(暂时用不到)
    # def total_head_feature(self, dct_text):
    #     num = 200  # 总体前多少个词
    #     words_name = dct_text['0'].keys()
    #     words_set = set(words_name)  # 去重
    #     words_dict = dict.fromkeys(words_set, 0)  # 创建一个特征词的字典
    #     for word in words_dict:
    #         for dct_i in dct_text:
    #             words_dict[word] += dct_text[dct_i][word]
    #     words_list = sorted(words_dict.items(), key=lambda tup: tup[1], reverse=True)
    #     feature_temp = map(lambda tup: tup[0], words_list[:num])
    #     # feature = filter(lambda feature_word: not re.search(r'\\\w+', feature_word), feature_temp)  # 对feature进行unicode的过滤
    #     return feature_temp

    def save_file(self, lst):
        print '-----------save the file-------------'
        with open('Feature_every.txt', 'w+') as f:
            for feature in lst:
                f.write(feature+'\n')
        print 'finish the save!'
        return

    def save_file_feature_word(self):
        # 将每个feature存储进Feature_every文件中
        data = self.prepare_data()
        lst = self.tfidf_feature(data)
        lst_1 = self.every_head_feature(lst)
        self.save_file(lst_1)
        return

    # 归一化的辅助函数辅佐于normalization_db
    def normalization_gen(self, data):
        # return 以生成器方式输出
        # param data 数据库读取的word数据 序列格式 ['english holle word', 'ok every day', ...]
        word_total_list = map(lambda tup: tup[1], data)  # 获取words_string然后组成list
        for word_string in word_total_list:
            yield self.normalization_gen(word_string)

    # 将输入的word_list特征化
    def normalization_feature(self, word_string):
        # # param word_string 数据库读取的word数据 序列格式 'english holle word ok every day'
        # return [1, 0, 0, 1,...]
        word_list = word_string.split(' ')  # 将每个words_string转换为words_list
        with open('Feature_every.txt', 'r+') as f:
            word_feature_temp = f.readlines()  # word_feature_temp phish特征读取后的列表，需要加工
        word_feature = map(lambda feature: feature.strip(), word_feature_temp)  # 加工，word_feature组成的list
        normalization_list = map(lambda x: 0, word_feature)  # 创建特征list [0,0,0,0,0,0...]
        for i, feature in enumerate(word_feature):
            if feature in word_list:
                normalization_list[i] = 1  # [1,0,0,0,0,...]
            else:
                continue
        return normalization_list

    # 归一化并存入数据库
    def normalization_save_db(self, flag):
        print '--------We are preparing to normalize feature and save db--------------'
        if flag == 'phish':
            data = self.get_phish_word()[:2000]
            for normalization_list in self.normalization_gen(data):
                normalization_list.append(1)  # phish_targer标注为1 [0,1,1,0,0,1,..,1]
                self.save_feature(str(normalization_list), 1)  # 将特征存储 1代表是钓鱼feature
        elif flag == 'normal':
            data = self.get_normal_word()[:2000]
            for normalization_list in self.normalization_gen(data):
                normalization_list.append(-1)  # normal_feature标注为-1 [0,0,0,0,0,1,..,-1]
                self.save_feature(str(normalization_list), 0)  # 将特征存储 0代表不是钓鱼feature
        else:
            raise SyntaxError
        print 'finish normalization and save \n'
        return


if __name__ == '__main__':
    # lst = read_csv('phish_data/verified_online4.csv')
    # d = count_brand(lst)
    # label_all = format_data(d)
    # load_file(label_all, 'phish_data/brands4.txt')
    # label_list = format_data(d)
    # pyplot.bar(range(0, len(label_list)), [tup[1] for tup in label_list], tick_label=[tup[0] for tup in label_list])
    # pyplot.show()
    # GetPhishSent().run(*lst)

    corpus = [
        'This is the first document.',
        'This is the second second document.',
        'And the third one.',
        'Is this the first document?',
        ]
    # vector = TfidfVectorizer(norm='l1', stop_words='english', ngram_range=(1,2))
    # weight = vector.fit_transform(corpus)
    # print type(weight)
    # print weight

    # vector = CountVectorizer()
    # transformer = TfidfTransformer()
    # tfidf = transformer.fit_transform(vector.fit_transform(corpus))
    # content = vector.fit_transform(corpus)
    # word = vector.get_feature_names()
    # print content
    # print word
    # print content.toarray()
    # weight = tfidf.toarray()
    # for i in xrange(len(weight)):
    #     print '--------text %d ---------' % i
    #     for j in xrange(len(word)):
    #         print '%s : %s' % (word[j], weight[i][j])


    # with open('Feature_every.txt', 'rb') as f:
    #     feature_temp = f.readlines()
    # feature_list = map(lambda feature_word: feature_word.strip(), feature_temp)
    # feature = map(lambda x: 0, feature_list)
    # word_string = "sign in to your account notice undefined index email in on line enter password password keep me signed in forgot my password sign in with different microsoft account microsoft terms of use privacy cookies"
    # word_list = word_string.split(' ')
    # # print feature_list
    # print word_list
    # for i, word in enumerate(word_list):
    #     if word in feature_list:
    #         feature[i] = 1
    #     else:
    #         continue
    # print feature











