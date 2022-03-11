import logging
import time
import random
from flask import jsonify
import scrapy
import requests
from fashionscraper.fashionscraper.settings import LOG_LEVEL
from ..items import ClothesItem
from scrapy.utils.log import configure_logging


class SheinSpider(scrapy.Spider):
    # configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    logging.basicConfig(
        filename='log.txt', format='%(levelname)s: %(message)s', level=logging.DEBUG)
    name = 'shein'
    allowed_domains = ['shein.com']
    start_urls = []

    def __init__(self, q='', p='', **kwargs):
        # urls = kwargs.pop('urls', [])
        # if urls:
        #     self.start_urls = urls.split(',')
        q = q
        p = p
        self.logger.info(self.start_urls)
        # https://it.shein.com/Clothing-c-2030.html
        self.start_urls = [
            "https://it.shein.com/Clothing-c-2030.html?ici=it_tab01navbar04&scici=navbar_WomenHomePage~~tab01navbar04~~4~~webLink~~~~0&srctype=category&userpath=category>ABBIGLIAMENTO" + "&page=" + p]

        super().__init__(**kwargs)

# note: * is the equivalent of js spread op
    def parse(self, response):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        # print(self.start_urls, 'bershka' in response.request.url )
        total = ''
        products = []
        products = [
            *products, *response.css("a.j-expose__product-item-img::attr(href)").getall()]
        next = response.css('.top-info__title-sum::text').get()
        total = next.split(' prodotti')[0]
        for prd in products:
            times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
            time.sleep(times[random.randint(0, len(times) - 1)])
            yield scrapy.Request(url='https://it.shein.com' + prd, callback=self.parseitem, cb_kwargs={'total': total})
        # scrapy.Request(url=next, callback=self.parse)

    def parseitem(self, response, total):
        times = [3, 5, 12, 65, 2, 1.5, 8, 1.3, 55, 23, 5, 8, 2, 90]
        time.sleep(times[random.randint(0, len(times) - 1)])
        results = {'items': [], 'total': total}
        result = ClothesItem()  # build item for the JSON file
        result['internal_id'] = 'SHEIN' + response.url.split('-p-')[1].split('-cat-')[0]

        raw = requests.get("https://it.shein.com/product-itemv2-" + response.url.split('-p-')[1].split('-cat-')[0] + ".html?_lang=it&_ver=1.1.8&template=1", headers={
            'cookies': 'language=it; cookieId=9D4DA675_EE8B_D7C4_D2E6_7E1AF2940C69; cate_channel_type=2; sessionID_shein=s%3ArPgD7tsJUbxifMX9nKnCG-ZK_gbvGoXx.NS%2F60nTkdE9mBBipxEkaPxIOiexglN1fCDs22oqp%2FXc; _ga=GA1.2.1580560195.1644402706; _gid=GA1.2.337386504.1644402706; sijssdk_2015_cross_new_user=1; sheindata2015jssdkcross=%7B%22distinct_id%22%3A%2217ede0a05e7b9e-03842dcac363854-44554e6d-2073600-17ede0a05e89c6%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217ede0a05e7b9e-03842dcac363854-44554e6d-2073600-17ede0a05e89c6%22%7D; country=IT; countryId=106; smidV2=2021071213374494caf693b13e27c2a1112ac64946daba00c0f932e7e337910; hideCoupon=1; hideCouponWithRequest=1; hideCouponId_time=15917_1; have_show=1; _abck=DEEC09276A2B064A9470AED40B83563D~0~YAAQ9BYQAnNYNrl+AQAAh18t4AdREyNrreelBSUCqy34oPaDMW5VGgFswvbs2zMpuCI+mW0GrJIqIyPS4wR7AZVFhML4tPEjh+Ej155QJbXJQGoelBna9Cyiv15CErPqqpuJUGiUcjwN+3hGbPXkmoXM5wtlCii7z61hxYM693Uc9unwqRHjjx49oGPGgA67pwkIn83FEmqCYZrJz3C+C4S3jM/6/zOfPjGbGnsMLsiAEZtNOcCHPgeO7UVs6hJYUt3IX2LZWSEEDezwqYMSr5CFv5h9LnFsJCwog4N28ASKe79ADiQ3e8SOPRcQjG5qxxIUIRmYBp2GzX+ltcAXU1PbI6L1HVjAQNeTwPlsrFDh+HgvS92Oz3luoStYABBhuW/YEVIYMg9/mrPGSzZCqavZdAk=~-1~-1~-1; bm_sz=3571A95AD022B204ADE87EE9C9F17256~YAAQ9BYQAnVYNrl+AQAAh18t4A7YjC031WP2CMsgZgOH4inc6gTWEljvNsdH86kMy9p+uxCFwVvkLlSYbiUJOkddV60Dz8ywgDH2xnINAtPQQbkS+akdHarqPGi92pOHZGFyGGKYCaGksRTT/JYDRFIW5pSd7nCDGPKhm0BdBDssp/M5l1eNC8XnLXA5fqZlNZlw2iQJfCtQ0VTM74G3J3PGDoDG7c/YP0Zh87el0skomc7GQlEBgfrTg73A3E9Nkwiub2LFMal2jwmuQcXgyhKea/DU+GPaV7uqO5cYQT2pKQ==~3290422~4338482; bi_session_id=bi_1644438577919_2468; default_currency_expire=1; ak_bmsc=9001CEBEEA68F08436D9B0F9758F8457~000000000000000000000000000000~YAAQ9BYQAoFYNrl+AQAAbmYt4A7O2BKoMrHWA5uctcntNZjixvoVdiD0eesSHl6Ys5SpONG4vyILXFW6S/jyl1IQmhcx+0wt2Q4V+Hfwn5b6Ps0QUX5189qVuBQOiK8U2xUFx9Dgtxa51k1pOXd3x9ooXUq4Amoqk0zqPDLOhJYd/h6RSH87Txafd1gr8yMoWB/w1OtYZF1SERgl/FcwyFG2qyl2em0CkTTLDcJgWtsffpOP2Hlg9ACF3aSg/rMS00yArR6jy0qmnwr016WEuiTI5xrLAeVuTzVhp/AVGXVR0ngfdE7K3bEtxXIjtLq5tAEdWp8oesl/OjDduanXTuyN3fefcCurasG2quml5px7CUyKwCYuPsOSg+0c/lSKfy4TrSm/AJynF62fR9oGu1kVq05BE0gRTAAKl6YP4jxZwnKwRZkokBJggSAZzq4R98zSIUYZpmiE91GJV1hbIXFC6MiFSzaPkgbbfiGvdgtB8MxeX2YUKQ==; ssrAbt=SellOutShow_type%3DB%23%23CccGoodsdetail_A%23%23SellingPoint_type%3Dsellingpoint; currency=EUR; OptanonAlertBoxClosed=2022-02-09T20:41:15.592Z; OptanonConsent=isIABGlobal=false&datestamp=Wed+Feb+09+2022+21%3A54%3A35+GMT%2B0100+(Ora+standard+dell%E2%80%99Europa+centrale)&version=6.13.0&hosts=&consentId=f95656ae-d1a8-4323-999b-94f1155433e7&interactionCount=2&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&iType=1&geolocation=IT%3B42; __atuvc=3%7C6; __atuvs=6204256daae3e9ab002; default_currency=EUR; bm_sv=D470D0E5B2B014B441C10F9B23DED365~89WSYamOKtP2zeoQ+/Q87T7TjH15DnVMJICOR2HZ/y+TXgy+VAaVEaGaAijEJRNxVX1A7OpN60h5EIfyw+9ZWKUgjyCPw97Kuvwy4Dv/1DTrkq53t/7Kz8f11vuM082Gd4LcduHRtGaTkUXLaEgMvLy0qbFCzQEGCJyYnDvL4yM='
        })
        html = raw.text
        script = html.split('window.goodsDetailv2SsrData = ')[
            1].split('var GB_S_SHIPPING_COST')[0]
        
        raw_imgs = [script.split('"origin_image":')[1].split(',')[0], script.split('"origin_image":')[2].split(',')[0], script.split(
            '"origin_image":')[3].split(',')[0], script.split('"origin_image":')[4].split(',')[0], script.split('"origin_image":')[5].split(',')[0]]

        images = []
        for img in raw_imgs:
            img = "https:" + img.replace('"', '')
            images.append(img)
        result['images'] = images

        # get name
        name = script.split('"goods_name":"')[1].split('"original_img"')[0].replace('"', '').replace(",", '')
        result['title'] = name
        result['url'] = response.url

        results['total'] = int(total.split(" Prodotti")[0])
        results['items'].append(dict(result))

        return results  # return json file to be output
