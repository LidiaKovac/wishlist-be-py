import scrapy
import crochet
crochet.setup()
from services import CrawlService
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from twisted.internet import reactor
from fashionscraper.fashionscraper.spiders.clothes import ClothesSpider
from flask import Flask, json
from flask import jsonify, request
from threading import Thread
import time 


app = Flask(__name__)

OUTPUT = []
crawl_runner = CrawlerRunner()

@app.route('/<string:query>')
def scrape(query:str):

    scrape_with_crochet(q=query) # Passing that URL to our Scraping Function

    time.sleep(12) # Pause the function while the scrapy spider is running
    
    return jsonify({"q":query, "r":OUTPUT}) # Returns the scraped data after being running for 20 seconds.
  
  
@crochet.run_in_reactor
def scrape_with_crochet(q):
    try:
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
        dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
        eventual = crawl_runner.crawl(ClothesSpider, q = q)
        print("Heyyyy", eventual)
        #return eventual
    except: 
        return "Error!", 500

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    OUTPUT.append(dict(item))
# def get_clothes(query:str):
#     run_scraper(query = query)
#     time.sleep(20)
#         # process = CrawlerRunner()
#         # runner = process.crawl(ClothesSpider, q=query)
#         # runner.addBoth(lambda _: reactor.stop())
#         # reactor.run(installSignalHandlers=False) # the script will block here until the crawling is finished
#         # process.start()
#    


# @crochet.run_in_reactor
# def run_scraper(query):
#     # This will connect to the dispatcher that will kind of loop the code between these two functions.
#     dispatcher.connect(get_res, signal=signals.item_scraped)
    
#     # This will connect to the ClothesSpider function in our scrapy file and after each yield will pass to the crawler_result function.
#     result = CrawlerRunner().crawl(ClothesSpider, q=query)
#     return result

# def get_res(item, response, spider): 
#     print(item)
#     OUTPUT.append(dict(item))
