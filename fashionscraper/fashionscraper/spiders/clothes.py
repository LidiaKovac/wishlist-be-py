import logging
from math import prod
import time
import scrapy
import random
from fashionscraper.fashionscraper.settings import LOG_LEVEL
from ..items import ClothesItem
from scrapy.utils.log import configure_logging


class ClothesSpider(scrapy.Spider):
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    logging.basicConfig(
        filename='log.txt', format='%(levelname)s: %(message)s', level=logging.DEBUG)
    name = 'clothes'
    allowed_domains = ['asos.com', 'aboutyou.it', 'hm.com']
    start_urls = []

    def __init__(self, q='', **kwargs):
        # urls = kwargs.pop('urls', [])
        # if urls:
        #     self.start_urls = urls.split(',')
        q = q
        self.logger.info(self.start_urls)
        self.start_urls = ["https://www.asos.com/it/search/?q=" + q,
                           'https://www2.hm.com/it_it/search-results.html?q=' + q, 'https://www.aboutyou.it/ricerca?term=' + q]

        super().__init__(**kwargs)

# note: * is the equivalent of js spread op
    def parse(self, response):
        # print(self.start_urls, 'bershka' in response.request.url )
        products = []
        if 'asos' in response.request.url:
            products = [*products, *
                        response.css("a._3TqU78D::attr(href)").getall()]
            # products.append(**)  #get all the links in the page
            # for prd in products:
            #     yield scrapy.Request(url = prd, callback = self.parseasos) #exec a request for each link in the page
        if 'aboutyou' in response.request.url:
            # products = []
            aboutyou = response.css(".sc-163x4qs-0::attr(href)").getall()
            urls = []
            for url in aboutyou:
                url = "https://www.aboutyou.it" + url
                urls.append(url)
            products = [*urls, *products]
        if 'hm.com' in response.request.url:
            hm = response.css("a.item-link::attr(href)").getall()
            urls = []
            for url in hm:
                url = "https://www2.hm.com" + url
                urls.append(url)
            products = [*products, *urls]
        random.shuffle(products)
        for prd in products:
            yield scrapy.Request(url=prd, callback=self.parseitem)

    def parseitem(self, response):
        results = []
        if 'asos' in response.request.url:
            result = ClothesItem()  # build item for the JSON file
            result['title'] = response.xpath("//h1/text()").get()
            result['images'] = response.xpath(
                "//img[starts-with(@src,'https://images.asos-media.com/products') and not(@class)]/@src").getall()
            result['url'] = response.url
            results.append(result)
        if 'aboutyou' in response.request.url:
            result = ClothesItem()  # build item for the JSON file
            # results = []
            result['title'] = response.xpath("//h1/text()").get()
            result['images'] = response.css(
                "button div[data-testid='productImage'] img[data-testid='productImageView']::attr(src)").getall()
            result['url'] = response.url
            results.append(result)
        if 'hm.com' in response.request.url:
            result = ClothesItem()  # build item for the JSON file
            
            result['title'] = response.xpath("//h1/text()").get()
            images = [*response.css("div.product-detail-main-image-container img::attr(src)").getall(
            ), *response.css("img.product-detail-thumbnail-image::attr(src)").getall()]
            urls = []
            for img in images:
                newimg = "https:" + img
                urls.append(newimg)
                
            result['images'] = urls
            result['url'] = response.url
            results.append(result)

        return results  # return json file to be output
