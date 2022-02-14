import time
from flask import Flask, send_from_directory, render_template, jsonify
from fashionscraper.fashionscraper.spiders.aboutyou import AboutYouSpider
from fashionscraper.fashionscraper.spiders.asos import AsosSpider
from fashionscraper.fashionscraper.spiders.hm import HMSpider
from fashionscraper.fashionscraper.spiders.shein import SheinSpider

from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerRunner
from scrapy import signals
import os
import crochet

from fashionscraper.fashionscraper.spiders.subdued import SubduedSpider
crochet.setup()


app = Flask(__name__)

OUTPUT = {
    'results': [],
    'total': 0
}
crawl_runner = CrawlerRunner()


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsof.icon')


@app.route('/<string:store>/<string:query>/<string:page>')
def scrape(store: str, query: str, page: str):  # store must be 'asos' or 'aboutyou'

    # Passing that URL to our Scraping Function
    scrape_with_crochet(q=query, p=page, store=store)

    time.sleep(600)  # Pause the function while the scrapy spider is running
    # print(OUTPUT)
    # Returns the scraped data after being running for 12 seconds.
    return jsonify(OUTPUT), 200


@crochet.run_in_reactor
def scrape_with_crochet(q, p, store):
    try:
        # This will connect to the dispatcher that will kind of loop the code between these two functions.
        dispatcher.connect(_crawler_result, signal=signals.item_scraped)
    # This will connect to the spider function in our scrapy file and after each yield will pass to the crawler_result function
        if store == 'asos':
            crawl_runner.crawl(AsosSpider, q=q, p=p)
        elif store == 'aboutyou':
            crawl_runner.crawl(AboutYouSpider, q=q, p=p)
        elif store == 'shein':
            crawl_runner.crawl(SheinSpider, q=q, p=p)
        elif store == 'hm':
            crawl_runner.crawl(HMSpider, q = q, p=p)
        elif store == 'subdued':
            crawl_runner.crawl(SubduedSpider, q = q, p=p)
    except:
        return "Error!", 500


# This will append the data to the output data list.
def _crawler_result(item, response, spider):
    OUTPUT['results'].append(item['items'][0])
    OUTPUT['total'] = str(item['total'])
