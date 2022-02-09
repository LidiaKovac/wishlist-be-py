import os
import crochet
crochet.setup()
from scrapy import signals
from scrapy.crawler import CrawlerRunner
from scrapy.signalmanager import dispatcher
from fashionscraper.fashionscraper.spiders.asos import AsosSpider
from fashionscraper.fashionscraper.spiders.aboutyou import AboutYouSpider
from flask import Flask,send_from_directory, render_template, jsonify

import time 


app = Flask(__name__)

OUTPUT = {
    'results': [],
    'total': 0
}
crawl_runner = CrawlerRunner()
@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico',mimetype='image/vnd.microsof.icon')
@app.route('/<string:store>/<string:query>/<string:page>')
def scrape(store:str, query:str, page:str): #store must be 'asos' or 'aboutyou'

    scrape_with_crochet(q=query, p=page, store=store) # Passing that URL to our Scraping Function

    time.sleep(60) # Pause the function while the scrapy spider is running
    # print(OUTPUT)
    return jsonify(OUTPUT),200 # Returns the scraped data after being running for 12 seconds.

  
@crochet.run_in_reactor
def scrape_with_crochet(q, p, store):
    if store == 'asos':
        try:
        # This will connect to the dispatcher that will kind of loop the code between these two functions.
            dispatcher.connect(_crawler_result, signal=signals.item_scraped)
        # This will connect to the spider function in our scrapy file and after each yield will pass to the crawler_result function.
            crawl_runner.crawl(AsosSpider, q = q, p=p)
            #return eventual
        except: 
            return "Error!", 500
    elif store == 'aboutyou':
        try:
        # This will connect to the dispatcher that will kind of loop the code between these two functions.
            dispatcher.connect(_crawler_result, signal=signals.item_scraped)
        # This will connect to the spider function in our scrapy file and after each yield will pass to the crawler_result function.
            crawl_runner.crawl(AboutYouSpider, q = q, p=p)
            #return eventual
        except: 
            return "Error!", 500

#This will append the data to the output data list.
def _crawler_result(item, response, spider):
    OUTPUT['results'].append(item['items'][0])
    OUTPUT['total'] = str(item['total'])
