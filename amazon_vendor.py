from datetime import datetime
from bs4 import BeautifulSoup as bs
import requests
import scraperwiki
import itertools
import json


def scrape_asins(base_url, vendor):
    # for vendor in vendors:
       # asin_num = []
        for page in itertools.count():
            data = {'seller': '{}'.format(vendor), 'currentPage': '{}'.format(page + 1), 'useMYI': '1'}
            pages = requests.post(base_url, data=data)
            soup_asin = json.loads(pages.text)
            if not soup_asin:
                break
            for asin in soup_asin:
                try:
                    prices = requests.get('http://www.amazon.com/gp/aag/ajax/asinRenderToJson.html?id={0}&useMYI=0&numCellsInResultsSet=2400&isExplicitSearch=0&merchantID={1}&shovelerName=AAGProductWidget&maxCellsPerPage=1'.format(asin, vendor))
                except:
                    pass
                if not prices:
                    continue
                li = json.loads(prices.text)
                sp = bs(li[0]['content'])
                try:
                    price = sp.find('li', 'AAG_ProductPrice aagItemDetLI').text
                except: pass
                todays_date = str(datetime.now())
                scraperwiki.sqlite.save(unique_keys=['Date'], data={"Seller ID": vendor, "ASIN": asin.strip(), "Price": price.strip(), "Date": todays_date})
                print asin


def scrape(vendor):
    base_url = 'http://www.amazon.com/gp/aag/ajax/searchResultsJson.html'
    scrape_asins(base_url, vendor)


if __name__ == '__main__':
    vendors = ['A1QPMQFTF8M71I', 'AR16HDX0T86D3', 'A2E18I18Q0JAFG', 'A2ZX3UCEGAR8GY',
    'A1PN9DPDDLPAD7', 'A1EOQ6DK5T5X45', 'A1E3Q3IXSLVMLQ', 'A21E5ULQPFWHNB', 'A2UQP4A626F3RZ',
    'A7Y9B0BV6QPNF', 'A35PDZRZE9DDA3', 'AWLS96Q1FYGFY']
    for vendor in vendors:
        scrape(vendor)
