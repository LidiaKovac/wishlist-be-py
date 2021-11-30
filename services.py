from fashionscraper.fashionscraper.spiders.clothes import ClothesSpider
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

class CrawlService():
    def spider_closing(self):
        print("Closing reactor")
        reactor.stop()
        pass
    
    def start_reactor(self):
        if not reactor.running:
            try:
                reactor.run()
            except:
                pass

    def stop_reactor(self):
        if reactor.running:
            reactor.stop()
    def crawl(self, query):
        
        # if you want to use CrawlerRunner, when you want to integrate Scrapy to existing Twisted Application
        runner = CrawlerRunner()
        d = runner.crawl(ClothesSpider, q=query)
        return d