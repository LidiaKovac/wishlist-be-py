import logging
from math import prod
import time
import scrapy
import random
from fashionscraper.fashionscraper.settings import LOG_LEVEL
from ..items import ClothesItem
from scrapy.utils.log import configure_logging


class AboutYouSpider(scrapy.Spider):
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    logging.basicConfig(
        filename='log.txt', format='%(levelname)s: %(message)s', level=logging.DEBUG)
    name = 'aboutyou'
    allowed_domains = ['aboutyou.it']
    start_urls = []

    def __init__(self, q='', p='', **kwargs):
        # urls = kwargs.pop('urls', [])
        # if urls:
        #     self.start_urls = urls.split(',')
        q = q
        p = p
        self.logger.info(self.start_urls)
        self.start_urls = ['https://www.aboutyou.it/c/' + q + '?page=' + p ]

        super().__init__(**kwargs)

# note: * is the equivalent of js spread op
    def parse(self, response):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        # print(self.start_urls, 'bershka' in response.request.url )
        total = ''
        products = []

        if 'aboutyou' in response.request.url:
            # products = []
            aboutyou = response.css(".sc-163x4qs-0::attr(href)").getall()
            urls = []
            for url in aboutyou:
                url = "https://www.aboutyou.it" + url
                urls.append(url)
            products = [*urls, *products]
            total = response.css('span.sc-2ppbeb-0::text').get()
        
        for prd in products:
            times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
            time.sleep(times[random.randint(0, len(times) - 1)])
            yield scrapy.Request(url=prd, callback=self.parseitem, cb_kwargs={'total' : total})
        # scrapy.Request(url=next, callback=self.parse)

    def parseitem(self, response, total):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        results = {'items': [], 'total': total}
        if 'aboutyou' in response.request.url:
            result = ClothesItem()  # build item for the JSON file
            # results = []
            result['title'] = response.xpath("//h1/text()").get()
            result['images'] = response.css(
                "button div[data-testid='productImage'] img[data-testid='productImageView']::attr(src)").getall()
            result['url'] = response.url
            result['id'] = 'ABOUTYOU' + response.url.split('-')[-1]

            results['total'] = total
            results['items'].append(dict(result))

        return results  # return json file to be output
