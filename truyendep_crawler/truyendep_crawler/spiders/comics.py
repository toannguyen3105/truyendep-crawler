# -*- coding: utf-8 -*-
import csv
import glob
import os.path
from openpyxl import Workbook

from scrapy.spiders import Spider
from scrapy.http import Request


class ComicsSpider(Spider):
    name = 'comics'
    allowed_domains = ['truyendep.com']
    start_urls = ['https://truyendep.com/']

    def __init__(self, category=None):
        self.category = category

    def parse(self, response):
        if self.category:
            absolute_comic_url = response.xpath(
                '//a[contains(strong/text(), "' + self.category + '") or contains(text(), "' + self.category + '")]/@href').extract_first()
            yield Request(absolute_comic_url, callback=self.parse_category)
        else:
            categories = response.xpath('//table[@class="theloai"]//a/@href').extract()
            for absolute_category in categories:
                yield Request(absolute_category, callback=self.parse_category)

    def parse_category(self, response):
        category_name = response.xpath('//li[@property="itemListElement"]/span/text()').extract_first()

        comics = response.xpath('//*[contains(@class, "update_item")]')
        for comic in comics:
            comic_name = comic.xpath('.//h3/a/text()').extract_first()
            absolute_comic_url = comic.xpath('.//h3/a/@href').extract_first()

            yield Request(absolute_comic_url,
                          meta={
                              'category_name': category_name,
                              'comic_name': comic_name,
                              'comic_url': absolute_comic_url
                          },
                          callback=self.parse_comic)

        absolute_next_page = response.xpath('//a[@rel="next"]/@href').extract_first()
        if absolute_next_page:
            yield Request(absolute_next_page, callback=self.parse_category)

    def parse_comic(self, response):
        category_name = response.meta['category_name']
        comic_name = response.meta['comic_name']
        comic_url = response.meta['comic_url']
        comic_author = response.xpath('//*[@class="truyen_info_right"]/li[2]/a/text()').extract_first()
        comic_type = response.xpath('//*[@class="truyen_info_right"]/li[3]/a/text()').extract()
        comic_description = response.xpath('//*[@class="entry-content"]/p//text()').extract()
        comic_chapter_title = response.xpath('//*[@class="chapter-list"]/div/span[1]/a/text()').extract()
        comic_chapter_link = response.xpath('//*[@class="chapter-list"]/div/span[1]/a/@href').extract()

        yield {
            'category_name': category_name,
            'comic_name': comic_name,
            'comic_url': comic_url,
            'comic_author': comic_author,
            'comic_type': comic_type,
            'comic_description': comic_description,
            'comic_chapter_title': comic_chapter_title,
            'comic_chapter_link': comic_chapter_link,
        }

    def close(spider, reason):
        csv_file = max(glob.iglob('*.csv'), key=os.path.getctime)

        wb = Workbook()
        ws = wb.active

        with open(csv_file, 'r', encoding="utf8") as f:
            for row in csv.reader(f):
                ws.append(row)

        wb.save(csv_file.replace('.csv', '') + '.xlsx')
