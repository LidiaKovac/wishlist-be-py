# https://www.subdued.com/it_it/collezione?p=1&product_list_limit=36

import logging
import json
import time
from urllib import request
from flask import jsonify
import scrapy
import random
from fashionscraper.fashionscraper.settings import LOG_LEVEL
from ..items import ClothesItem
from scrapy.utils.log import configure_logging


products = []

class SubduedSpider(scrapy.Spider):
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    logging.basicConfig(
        filename='log.txt', format='%(levelname)s: %(message)s', level=logging.DEBUG)
    name = 'hm'
    allowed_domains = ['hm.com']
    start_urls = []

    def __init__(self, q='', p='', **kwargs):
        # urls = kwargs.pop('urls', [])
        # if urls:
        #     self.start_urls = urls.split(',')
        q = q
        p = p
        self.logger.info(self.start_urls)
        self.start_urls = [
            'https://www.subdued.com/it_it/collezione?p=' + p + '&product_list_limit=36']

        super().__init__(**kwargs)

# note: * is the equivalent of js spread op
    def parse(self, response):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        # print(self.start_urls, 'bershka' in response.request.url )
        total = 0
        urls = response.css("a.product-item-photo::attr(href)").getall()
        # print(urls)
        for url in urls:
            products.append(url)

        next = response.css('a.page::attr(href)').getall()[-1]
        nextBtn = response.css('a.next').get()
        if nextBtn:
            total += 36
            
            yield scrapy.Request(url=next, callback=self.parse, dont_filter=True)
            print(len(products))
        for prd in products:
            times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
            time.sleep(times[random.randint(0, len(times) - 1)])
            yield scrapy.Request(url=prd, callback=self.parseitem, cb_kwargs={'total': total}, dont_filter=True)
        # scrapy.Request(url=next, callback=self.parse)

    def parseitem(self, response, total):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        print(total, response.url)
        results = {'items': [], 'total': total}
        result = ClothesItem()  # build item for the JSON file
        result['id'] = 'SUBDUED' + response.css("div.sku div::text").get()

        raw_imgs = response.xpath(
            "//img[starts-with(@src,'https://www.subdued.com/media/catalog/product/') and not(@class)]/@src").getall()
        # raw_imgs = [*response.css('img::attr(src)').getall()]
        images = []
        for img in raw_imgs:
            img = img.replace('"', '').replace(
                "=url[file:/product/miniature]", "=url[file:/product/main]")
            images.append(img)
        result['images'] = images

        # get name
        result['title'] = response.css('h1 span::text').get().replace(
            '\t', '').replace('\n', '').replace("  ", "")
        result['url'] = response.url

        results['total'] = int(total)
        results['items'].append(dict(result))

        return results  # return json file to be output
