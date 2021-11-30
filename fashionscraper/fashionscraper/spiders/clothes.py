import scrapy
from twisted.internet import reactor
from ..items import ClothesItem

class ClothesSpider(scrapy.Spider):
    name = 'clothes'
    allowed_domains = ['asos.com']
    start_urls = []
    def __init__(self, q='', **kwargs):
        # urls = kwargs.pop('urls', []) 
        # if urls:
        #     self.start_urls = urls.split(',')
        # self.logger.info(self.start_urls)
        print(q)
        self.start_urls.append("https://www.asos.com/it/search/?q=" + q)
        super().__init__(**kwargs)
        

    def parse(self, response):
        
        products = response.css("a._3TqU78D::attr(href)").getall() #get all the links in the page
        for prd in products: #for loop
            yield scrapy.Request(url = prd, callback = self.parseitem) #exec a request for each link in the page
        

    def parseitem(self,response): 
        result = ClothesItem() #build item for the JSON file
        result['title'] = response.xpath("//h1/text()").get()
        result['images'] = response.xpath("//img[starts-with(@src,'https://images.asos-media.com/products') and not(@class)]/@src").getall()
        result['url'] = response.url
        results = []
        results.append(result)
        return results #return json file to be output