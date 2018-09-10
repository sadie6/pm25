# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import scrapy
import json
import time, datetime
from scrapy.http import Request
import re
from pm25.items import Pm25Item


citys = []
_url = 'http://www.pm25.com/city%s'
with open('/home/liusai/Desktop/city2.txt','r') as f:
        for line in f:
            citys.append(_url %line.replace('\n',''))
# print citys
class PmSpider(scrapy.Spider):
    name = 'pm'
    allowed_domains = ['www.pm25.com']
    start_urls = citys
    kinds = ['aqi','pm2_5','pm10','so2','no2','co','o3']
    shuju = {}

    

    def parse(self, response):
        if response.url == 'http://www.pm25.com/beijing.html':
            pass
        else:
            print response.url
            # print response.body
            poi = response.xpath('//div[@class="pj_area_data"]/ul[1]/li/a[1]/@href').extract()
            # print len(poi),poi[0]    #poi[0] = '/city/mon/aqi/厦门/溪东.html'
            for p in poi:
                url = 'http://www.pm25.com' + p.replace('aqi','%s')
                for kind in self.kinds[:]:
                    _url = url %kind
                    yield Request(_url,callback=self.mon, errback=self.parse_err,meta={'a_type':kind,'sign': url %'sign'})



    def mon(self, response):
        # print response.body
        a = response.xpath('//script').extract()
        # print len(a),a[-1]
        d = re.findall(r'data:\[(.*?)\] ',a[-1])
        # print d
        # print response.meta['a_type'],response.meta['sign']
        if len(d) == 4:
            # print d[1]
            v = d[1].split(',')[-1]
            # print v
        else:
            v = d[0].split(',')[-1]
        time_point = re.findall(r'<span>更新时间：(.*?)</span>',response.body)[0]
        if response.meta['sign'] not in self.shuju.keys():
            self.shuju[response.meta['sign']] = {}
        self.shuju[response.meta['sign']][response.meta['a_type']] =  int(v)
        # print self.shuju[response.meta['sign']]
        if len(self.shuju[response.meta['sign']].keys()) == 7:
            # print response.meta['sign'],self.shuju[response.meta['sign']]
            signs = response.meta['sign'].split('/')
            area = signs[-2]
            position_name = signs[-1].strip('.html')
            # print area,position_name
            aqi=self.shuju[response.meta['sign']]['aqi']
            pm2_5=self.shuju[response.meta['sign']]['pm2_5']
            co = self.shuju[response.meta['sign']]['co']
            pm10 = self.shuju[response.meta['sign']]['pm10']
            so2 = self.shuju[response.meta['sign']]['so2']
            no2 = self.shuju[response.meta['sign']]['no2']
            o3 = self.shuju[response.meta['sign']]['o3']
            pm_item = Pm25Item( position_name = position_name, area = area, time_point = time_point, aqi = aqi, pm2_5 = pm2_5, co = co, pm10 = pm10, so2 = so2, no2 = no2, o3 = o3 )
            yield pm_item







    
    def parse_err(self, response):
        self.logger.error('crawl %s fail'%response.url)