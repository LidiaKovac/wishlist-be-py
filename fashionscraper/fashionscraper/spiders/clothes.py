import scrapy
from ..items import ClothesItem

class ClothesSpider(scrapy.Spider):
    name = 'clothes'
    allowed_domains = ['asos.com', 'aboutyou.it']
    start_urls = []
    def __init__(self, q='', **kwargs):
        # urls = kwargs.pop('urls', []) 
        # if urls:
        #     self.start_urls = urls.split(',')
        # self.logger.info(self.start_urls)
        print(q)
        self.start_urls.append("https://www.asos.com/it/search/?q=" + q)
        self.start_urls.append("https://www.aboutyou.it/ricerca?term=" + q)
        print(self.start_urls)
        super().__init__(**kwargs)
        

    def parse(self, response):
        for url in self.start_urls:
            if 'asos' in response.request.url: 
                products = []
                products = [*response.css("a._3TqU78D::attr(href)").getall()]
                # products.append(**)  #get all the links in the page
                for prd in products: 
                    yield scrapy.Request(url = prd, callback = self.parseasos) #exec a request for each link in the page
            elif 'aboutyou' in response.request.url:
                print(response.request.url)
                products = []
                products = [*response.css(".sc-163x4qs-0::attr(href)").getall()]
                # products.append(**response.css(".sc-163x4qs-0::attr(href)").getall()) 
                print(products)
                for prd in products:
                    prd = "https://www.aboutyou.it" + prd
                    print(prd)
                    yield scrapy.Request(url = prd, callback=self.parseabout)
        

    def parseasos(self,response): 
        result = ClothesItem() #build item for the JSON file
        result['title'] = response.xpath("//h1/text()").get()
        result['images'] = response.xpath("//img[starts-with(@src,'https://images.asos-media.com/products') and not(@class)]/@src").getall()
        result['url'] = response.url
        results = []
        results.append(result)
        return results #return json file to be output

    def parseabout(self,response): 
        result = ClothesItem() #build item for the JSON file
        results = []
        result['title'] = response.xpath("//h1/text()").get()
        result['images'] = response.css("button div[data-testid='productImage'] img[data-testid='productImageView']::attr(src)").getall()
        result['url'] = response.url
        
        results.append(result)
        return results #return json file to be output