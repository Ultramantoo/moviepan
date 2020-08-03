# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time
import csv


class MoviepanPipeline(object):
    # print('ok2222222222222222')

    @staticmethod
    def process_item(item, spider):
        list_item = [item['types'], item['link'], item['name'], item['link_pan'], item['pan_list'], item['pan_m'],
                     item['magnet_list']]
        date = str(time.strftime('%m%d', time.localtime(time.time())))
        # print('ok2222222222222222')
        with open("movie_pan" + date + '.csv', 'a+', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(list_item)
