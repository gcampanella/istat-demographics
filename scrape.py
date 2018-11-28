#!/usr/bin/env

import csv
from itertools import product
from urllib.parse import urljoin

import scrapy
from bs4 import BeautifulSoup


class IstatScraper(scrapy.Spider):
    name = 'Istat'
    allowed_domains = ['demo.istat.it']
    start_urls = {
        'http://demo.istat.it/bilmens2004/left02.htm': 2004,
        'http://demo.istat.it/bilmens2005/left02.htm': 2005,
        'http://demo.istat.it/bilmens2006/left02.htm': 2006,
        'http://demo.istat.it/bilmens2007gen/left02.htm': 2007,
        'http://demo.istat.it/bilmens2008gen/left02.php': 2008,
        'http://demo.istat.it/bilmens2009gen/left02.php': 2009,
        'http://demo.istat.it/bilmens2010gen/left02.php': 2010,
        'http://demo.istat.it/bilmens20111008/left02.php': 2011,
        'http://demo.istat.it/bilmens20111009/left02.php': 2011,
        'http://demo.istat.it/bilmens2012gen/left02.php': 2012,
        'http://demo.istat.it/bilmens2013gen/left02.php': 2013,
        'http://demo.istat.it/bilmens2014gen/left02.php': 2014,
        'http://demo.istat.it/bilmens2015gen/left02.php': 2015,
        'http://demo.istat.it/bilmens2016gen/left02.php': 2016,
        'http://demo.istat.it/bilmens2017gen/left02.php': 2017,
        'http://demo.istat.it/bilmens2018gen/left02.php': 2018,
    }

    def start_requests(self):
        for url, year in self.start_urls.items():
            yield scrapy.Request(
                url,
                callback=self.parse_provinces_and_months,
                meta={
                    'year': year,
                }
            )

    def parse_provinces_and_months(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        provinces_select = soup.find('select', attrs={'name': 'Pro'})
        provinces = [int(x['value'])
                     for x in provinces_select.find_all('option')]
        months_select = soup.find('select', attrs={'name': 'periodo'})
        months = [int(x['value'])
                  for x in months_select.find_all('option')]
        for province, month in product(provinces, months):
            url = urljoin(
                response.url,
                'bild7b1.php?allrp=4&Pro={}&periodo={}'.format(province, month)
            )
            yield scrapy.Request(
                url,
                callback=self.process_csv,
                meta={
                    'province': province,
                    'year': response.meta['year'],
                    'month': month,
                }
            )

    def process_csv(self, response):
        lines = response.text.splitlines()
        men_start = lines.index(',Maschi') + 1
        men_end = next(men_start + i for i, x in enumerate(lines[men_start:])
                       if x.startswith('Codice'))
        for entry in self.parse_csv(lines[men_start:men_end]):
            yield dict(entry, **{
                'province': response.meta['province'],
                'year': response.meta['year'],
                'month': response.meta['month'],
                'sex': 'M',
            })
        women_start = lines.index(',Femmine') + 1
        for entry in self.parse_csv(lines[women_start:]):
            yield dict(entry, **{
                'province': response.meta['province'],
                'year': response.meta['year'],
                'month': response.meta['month'],
                'sex': 'F',
            })

    def parse_csv(self, lines):
        reader = csv.reader(lines)
        entries = []
        for row in reader:
            if len(row) != 11:
                break
            entries.append({
                'municipality': int(row[0]),
                'births': int(row[3]),
                'deaths': int(row[4]),
                'net_migration': int(row[8]),
            })
        return entries
