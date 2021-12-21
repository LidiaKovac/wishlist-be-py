import os
import crochet
crochet.setup()
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from fashionscraper.fashionscraper.spiders.clothes import ClothesSpider
from flask import Flask,send_from_directory, render_template, jsonify

import time 


app = Flask(__name__)

OUTPUT = []
crawl_runner = CrawlerRunner()
@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsof.icon')
@app.route('/<string:query>')
def scrape(query:str):
    
    scrape_with_crochet(q=query) # Passing that URL to our Scraping Function

    time.sleep(15) # Pause the function while the scrapy spider is running

    return jsonify({"q":query, "r":OUTPUT}),200 # Returns the scraped data after being running for 12 seconds.
  
  
@crochet.run_in_reactor
def scrape_with_crochet(q):
    try:
    # This will connect to the dispatcher that will kind of loop the code between these two functions.
        dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    # This will connect to the ReviewspiderSpider function in our scrapy file and after each yield will pass to the crawler_result function.
        crawl_runner.crawl(ClothesSpider, q = q)
        #return eventual
    except: 
        return "Error!", 500

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    # print(response.request.url)
    OUTPUT.append(dict(item))

