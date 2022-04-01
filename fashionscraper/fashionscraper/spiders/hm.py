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


class HMSpider(scrapy.Spider):
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
        self.start_urls = ['https://www2.hm.com/it_it/donna/acquista-per-prodotto/view-all.html?page-size=' +
                           str(int(p)*36) + "offset=" + str(int(p-1)*36)]

        super().__init__(**kwargs)

# note: * is the equivalent of js spread op
    def parse(self, response):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        # print(self.start_urls, 'bershka' in response.request.url )
        total = ''
        products = []
        products = [
            *products, *response.css("a.item-link::attr(href)").getall()]
        next = response.css('.filter-pagination::text').get()
        total = next.split(' articoli')[0]
        for prd in products:
            times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
            time.sleep(times[random.randint(0, len(times) - 1)])
            yield scrapy.Request(url='https://www2.hm.com' + prd, callback=self.parseitem, cb_kwargs={'total': total})
        # scrapy.Request(url=next, callback=self.parse)

    def parseitem(self, response, total):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        results = {'items': [], 'total': total}
        result = ClothesItem()  # build item for the JSON file
        result['internal_id'] = 'HM' + \
            response.url.split('productpage.')[1].split('.html')[0]

        raw_imgs = response.xpath(
            "//img[starts-with(@src,'//lp2.hm.com/hmgoepprod?') and not(@class)]/@src").getall()
        # raw_imgs = [*response.css('img::attr(src)').getall()]
        images = []
        for img in raw_imgs:
            img = "https:" + \
                img.replace('"', '').replace(
                    "=url[file:/product/miniature]", "=url[file:/product/main]")
            images.append(img)

        print(images)
        result['images'] = images

        # get name
        result['title'] = response.css('h1::text').get().replace(
            '\t', '').replace('\n', '').replace("  ", "")
        result['url'] = response.url

        results['total'] = int(total)
        results['items'].append(dict(result))

        return results  # return json file to be output
