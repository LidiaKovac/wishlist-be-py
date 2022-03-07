import logging
import json
import time
from unittest import result
from urllib import request
from flask import jsonify
import scrapy
import random
from fashionscraper.fashionscraper.settings import LOG_LEVEL
from ..items import ClothesItem
from scrapy.utils.log import configure_logging


class OvsSpider(scrapy.Spider):
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    logging.basicConfig(
        filename='log.txt', format='%(levelname)s: %(message)s', level=logging.DEBUG)
    name = 'ovs'
    allowed_domains = ['ovs.it']
    start_urls = []

    def __init__(self, q='', p='', **kwargs):
        # urls = kwargs.pop('urls', [])
        # if urls:
        #     self.start_urls = urls.split(',')
        q = q
        p = p
        self.logger.info(self.start_urls)
        self.start_urls = ["https://www.ovs.it/search?q=donna&search-button=&lang=it_IT&sz=100" + "&start=" + str((int(p) - 1) * 100)]

        super().__init__(**kwargs)

# note: * is the equivalent of js spread op
    
    def parse(self, response):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        total = ''
        products = []
        products = [
            *products, *response.css("a.product-tile-link::attr(href)").getall()]
        next = response.css('.search-result-count::text').get()
        total = next.split(' risultati')[0].replace("\n", '').replace(".", '')
        for prd in products:
            times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
            time.sleep(times[random.randint(0, len(times) - 1)])
            yield scrapy.Request(url='https://www.ovs.it' + prd, callback=self.parseitem, cb_kwargs={'total': total})
        # scrapy.Request(url=next, callback=self.parse)

    def parseitem(self, response, total):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        results = {'items': [], 'total': total}
        result = ClothesItem()  # build item for the JSON file
        result['id'] = 'OVS' + response.url.split('/')[4].split('.html')[0]

        result['images'] = [*response.css(".thumbnail-images-container div.thumbnail-image-wrapper img::attr(src)").getall()]
         
        # get name
        
        result['title'] = response.css("h1::text").get()
        result['url'] = response.url

        results['total'] = int(total)
        results['items'].append(dict(result))

        return results  # return json file to be output
