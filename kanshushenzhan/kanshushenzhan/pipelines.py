# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import string


class KanshushenzhanPipeline(object):
    def process_item(self, item, spider):
        name = item['titles']  # 小说名称字典
        for n in name.values():
            path = os.path.join(r'E:\novel', n)
            try:
                os.makedirs(path)
            except:
                pass
        chap = item['chaptername']  # 章节名称字典
        contents = item['chaptercontent']  # 章节内容字典
        k = list(contents.keys())  # 键值列表
        ls = k[0].split("/")[-1]
        ks = k[0].rstrip(ls)
        m = name[ks]
        path = os.path.join(r'E:\novel', m)  # 文件夹
        try:
            os.chdir(path)
        except:
            print(path + ' 不存在！')
        title = ''.join(chap[k[0]].split())  # split():split方法中不带参数时，表示分割所有换行符、制表符、空格
        temp = []
        for c in title:
            if c not in string.punctuation:
                temp.append(c)
        titles = ''.join(temp)
        titles = titles.replace('？', '')
        l = titles + str('.txt')
        path1 = os.path.join(path, l)  # path小说文件夹路径
        try:
            with open(path1, 'w', encoding='gbk') as F:
                for c in contents[k[0]]:
                    F.write(c + '\n')
        except:
            print(k[0] + " " + chap[k[0]] + ' 下载失败！')
        return item
