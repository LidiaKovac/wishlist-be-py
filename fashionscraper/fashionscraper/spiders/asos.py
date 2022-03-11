import logging
from math import prod
import time
from cv2 import log
import scrapy
import random
from fashionscraper.fashionscraper.settings import LOG_LEVEL
from ..items import ClothesItem
from scrapy.utils.log import configure_logging


class AsosSpider(scrapy.Spider):
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    logging.basicConfig(
        filename='log.txt', format='%(levelname)s: %(message)s', level=logging.DEBUG)
    name = 'asos'
    allowed_domains = ['asos.com']
    start_urls = []

    def __init__(self, q='', p='', **kwargs):
        # urls = kwargs.pop('urls', [])
        # if urls:
        #     self.start_urls = urls.split(',')
        q = q
        p = p
        self.logger.info(self.start_urls)
        self.start_urls = [
            "https://www.asos.com/it/search/?q=" + q + "&page=" + p]

        super().__init__(**kwargs)

# note: * is the equivalent of js spread op
    def parse(self, response):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        # print(self.start_urls, 'bershka' in response.request.url )
        total = ''
        products = []
        if 'asos' in response.request.url:
            products = [*products, *
                        response.css("a._3TqU78D::attr(href)").getall()]
            next = response.css('.XmcWz6U::text').get()
            total = next.split('di ')[1].split(' prodotti')[0]
        for prd in products:
            times = [3, 5, 12, 35, 2, 1.5, 8, 1.3, 25.1, 23, 5, 8, 2, 30.4]
            time.sleep(times[random.randint(0, len(times) - 1)])
            yield scrapy.Request(url=prd, callback=self.parseitem, cb_kwargs={'total': total})
        # scrapy.Request(url=next, callback=self.parse)

    def parseitem(self, response, total):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        results = {'items': [], 'total': total}
        if 'asos' in response.request.url:
            result = ClothesItem()  # build item for the JSON file
            result['title'] = response.xpath("//h1/text()").get()
            result['images'] = response.xpath(
                "//img[starts-with(@src,'https://images.asos-media.com/products') and not(@class)]/@src").getall()
            result['url'] = response.url
            if response.url.split('prd/')[1].split('?clr')[0]:
                result['internal_id'] = 'ASOS' + \
                    response.url.split('prd/')[1].split('?clr')[0]
            else:
                result['internal_id'] = 'ASOS' + \
                    response.url.split('grp/')[1].split('?clr')[0]

            results['total'] = total
            results['items'].append(dict(result))

        return results  # return json file to be output
