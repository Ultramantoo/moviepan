# -*- coding: utf-8 -*-
import scrapy
from moviepan.items import MoviepanItem
import re
import copy
# from cnblogSpider.items import CnblogspiderItem

# noinspection PyTypeChecker
class MoviepanSpider(scrapy.Spider):
    name = 'MoviePan'
    allowed_domains = ['n7f6.cn']
    start_urls = ['http://n7f6.cn/']

    def parse(self, response):
        # 获取分类
        type_all = response.xpath('//div[2]/div[2]/div[1]/ul[1]/li')
        print(len(type_all))
        for s in type_all[1:]:
            print('=' * 5)
            item = MoviepanItem()
            item['link'] = s.xpath('a/@href')[0].extract()
            item['types'] = str(s.xpath('a/span/text()').extract_first())
            print(item['types'])
            class_url = response.urljoin(item['link'])
            print(class_url)
            yield scrapy.Request(class_url, callback=self.parse_classify, meta={'key': copy.deepcopy(item)})
            # yield item

    def parse_classify(self, response):
        print('ok')
        # print(test)ra
        name_all = response.xpath('//div[1]/div[1]/div[1]/div[2]//div[1]/div[2]/div[1]')
        print(len(name_all))
        item = ''
        for s in name_all:
            # print(s)
            # item = MoviepanItem()
            item = response.meta['key']
            name = str(s.xpath('a/text()').extract_first().replace(' ', '').replace('\n', ''))
            print(name)
            print(type(name))
            # st = "处女心经오!수정(2000)"
            result = ''.join(re.findall(r'[\u4e00-\u9fa5_()!！：:/（）a-zA-Z0-9]', name))
            item['name'] = result
            print(item['name'])
            item['link_pan'] = s.xpath('a/@href')[0].extract()
            print(item['link_pan'])
            link_pan_url = response.urljoin(item['link_pan'])
            # yield item
            yield scrapy.Request(link_pan_url, callback=self.parse_pan, meta={'key2': copy.deepcopy(item)})

        url_p = item['link'][-2:]
        print(url_p)
        next_num = response.xpath("//span[@class='page-numbers current']/text()").extract_first()
        print(next_num)
        # 最大页数
        max_next = response.xpath("//a[@class='page-numbers']/text()").extract()[-1]
        print(max_next)
        if int(next_num) < int(max_next):
            next_num = int(next_num) + 1
            print(next_num)
            if next_num <= 1000: # 设置页数
                next_url = 'http://n7f6.cn/?paged={}&cat={}'.format(next_num,url_p)
                yield scrapy.Request(url=next_url,callback=self.parse_classify, meta={'key': copy.deepcopy(item)})

    def parse_pan(self, response):
        print('ok_2')
        # item = MoviepanItem()
        item = response.meta['key2']
        # 获取网盘地址
        content = response.xpath("//div[@class='post-content']")
        # print(content.text)
        # result =etree.tostring(content[0]).decode('utf-8')
        result = content.extract()[0]
        # print(result)
        pan_list = re.findall(r"(https://pan.baidu.com.+?)\"", result)
        print(pan_list)
        item['pan_list'] = pan_list
        pan_m = re.findall("(提取码: |提取码：|密码：|密码:)(.+?)<", result)
        pan_m = [i[1] for i in pan_m]
        print(pan_m)
        item['pan_m'] = pan_m
        # 获取 链接下载地址
        magnet_list = re.findall(r"((ed2k|magnet).+?)\"", result)
        magnet_list = [i[0] for i in magnet_list]
        if len(magnet_list) > 0: print(magnet_list)
        item['magnet_list'] = magnet_list
        yield item
