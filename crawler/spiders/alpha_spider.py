# encoding=utf-8
from __future__ import unicode_literals
import scrapy
import datetime
from mongoengine import connect
from urlparse import urljoin

from models import Institution, Info


class AlphaSpider(scrapy.Spider):
    name = "alpha_spider"

    def __init__(self):
        connect('alpha_flask')
        super(AlphaSpider, self).__init__()

    def start_requests(self):
        Institution.objects.update(last_crawled=0)
        for institution in Institution.objects.filter(crawl_latest=True):
            if institution.name == '深圳市发展和改革委员会': continue
            yield scrapy.Request(institution.url, meta={'institution': institution})
        for institution in Institution.objects.filter(crawl_all=True):
            if institution.name == '深圳市发展和改革委员会': continue
            for url in institution.url_list:
                yield scrapy.Request(url, meta={'institution': institution})

    def parse(self, response):
        institution = response.meta['institution']
        print 'crawling', institution, '...'
        for item in response.xpath(institution.item_xpath):
            title = item.xpath(institution.title_xpath).extract_first()
            if not title: continue
            title = title.strip()
            url = item.xpath(institution.url_xpath).extract_first()
            from scrapy.utils.response import get_base_url
            url = urljoin(get_base_url(response), url)
            pub_date = item.xpath(institution.pub_date_xpath).extract_first()
            if institution.name in ('深圳市科技创新委员会', '深圳市宝安区人民政府'):
                pub_date = pub_date.replace(u'年', '-').replace(u'月', '-').replace(u'日', '')
            elif institution.name in ('深圳市龙岗区发展和改革局', '深圳市龙岗区科技创新局',
                                      '深圳市前海深港服务业合作区管理局', '深圳市南山区政府', '深圳市福田区人民政府'):
                pub_date = pub_date[1:-1]
            elif institution.name.startswith('深圳市罗湖区'):
                pub_date = pub_date.split()[-1]
            elif institution.name == '深圳市盐田区人民政府':
                pub_date = pub_date.split()[-1][1:-1].replace('.', '-')
            data = {
                'title': title,
                'url': url,
                'pub_date': datetime.date(*[int(i) for i in pub_date.split('-')]),
                'institution': institution,
            }
            if institution.name == '深圳市光明新区管理委员会':
                yield scrapy.Request(url, self.parse_title01, meta={'data': data, 'institution': institution})
                continue
            try:
                print pub_date, title, url
                Info.objects.create(**data)
                institution.update(inc__last_crawled=1)
            except Exception, e:
                print e

    def parse_title01(self, response):
        data = response.meta['data']
        institution = response.meta['institution']
        data['title'] = response.xpath('//div[@class="titxixi"]/text()').extract_first().strip()
        try:
            Info.objects.create(**data)
            print data['pub_date'], data['title'], data['url']
            institution.update(inc__last_crawled=1)
        except Exception, e:
            print e

    def close(self, reason):
        Institution.objects.update(crawl_latest=False, crawl_all=False)
        pass
