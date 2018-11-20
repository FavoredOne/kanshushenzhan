# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import os
import re
import requests
from kanshushenzhan.items import KanshushenzhanItem


class WanjieSpider(scrapy.Spider):
    name = 'wanjie'
    allowed_domains = ['kanshushenzhan.com']
    start_urls = ['https://www.kanshushenzhan.com/all/0_lastupdate_0_0_0_0_2_0_1.html']

    def parse(self, response):
        # print(response.url)
        # print(response.xpath("//div[@class='listRightBottom']/ul/li/h2/a/text()").extract())
        titles = response.xpath("//div[@class='listRightBottom']/ul/li/h2/a/text()").extract()  # 书名
        novelurllist = response.xpath("//div[@class='listRightBottom']/ul/li/h2/a/@href").extract()  # 书的网址
        titlesdict = dict(zip(novelurllist, titles))
        for no in novelurllist:
            # print(no)
            yield Request(url=no, callback=self.parse_novel, meta={"ID1": titlesdict})
        page = response.xpath('//div[@class="page"]/strong/text()').extract_first()
        i = int(page) + 1
        page_urls = 'https://www.kanshushenzhan.com/all/0_lastupdate_0_0_0_0_2_0_%s.html' % i  # 下一页网址
        yield Request(page_urls, callback=self.parse)
        # self.logger.debug(response.text)
        pass

    def parse_novel(self, response):
        chapterurllist = []
        chapterurl = response.xpath('//div[@class="chapterCon"]/ul/li/a/@href').extract()  # 书名章节网址
        chapternames = response.xpath('//div[@class="chapterCon"]/ul/li/a/text()').extract()  # 章节名称
        for ch in range(len(chapterurl)):
            chapterurlreal = 'https://www.kanshushenzhan.com' + chapterurl[ch]
            chapterurllist.append(chapterurlreal)
        chapterdict = dict(zip(chapterurllist, chapternames))
        for cm in chapterurllist:
            yield Request(url=cm, callback=self.parse_chaptercontent, meta={"ID1": response.meta["ID1"], "ID2": chapterdict})
            # print(chaptername[ch] + ': ' + chapterurlreal)

    def parse_chaptercontent(self, response):
        item = KanshushenzhanItem()
        chapterdetail = []
        # print(response.text)
        item['titles'] = response.meta["ID1"]
        item['chaptername'] = response.meta["ID2"]
        contenturl = response.url
        content = response.xpath('//*[@id="yellow"]/div[1]/div[2]/div[2]/p/text()').extract()  # 章节内容
        for c in content:
            if c != '\r\n':
                chapterdetail.append(c.strip('\r\n\xa0\xa0\xa0\xa0'))
                # print(c.strip('\r\n\xa0\xa0\xa0\xa0'))
        contentdict = {contenturl: chapterdetail}
        # contentdict = dict(zip(contenturl, chapterdetail))  # 这种方法如果第一个参数为字符串就会把每个字母隔开成为对应数列
        item['chaptercontent'] = contentdict
        yield item

