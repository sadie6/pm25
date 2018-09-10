# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from MySQLdb.cursors import DictCursor

from twisted.enterprise import adbapi
import logging
from pm25.items import Pm25Item
import pm25.settings as settings

class Pm25Pipeline(object):
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        dbargs = dict(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            passwd = settings.MYSQL_PASSWD,
            port = settings.MYSQL_PORT,
            charset = 'utf8',
            cursorclass = DictCursor,
            use_unicode = True,
            )   
        self.dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)


    def process_item(self, item, spider):
        if isinstance(item, Pm25Item):
            # print 'xxxxxxxxxxxxxxxxxxxxxx'
            query = self.dbpool.runInteraction(self._process_pm,item)
            query.addErrback(self._handle_error, item, spider)




        return item


    def _process_pm(self, tx, item):
        # print 'xxxxx'
        _sql = "insert into place_PM(aqi,pm2_5,co,pm10,so2,no2,o3,position_name,area,time_point) values (%s,%s,%s,%s,%s,%s,%s,'%s','%s','%s')"
        sql = _sql % (item['aqi'],item['pm2_5'],item['co'],item['pm10'],item['so2'],item['no2'],item['o3'],item['position_name'],item['area'],item['time_point'])
        # print sql
        try:
            tx.execute(sql)
            print sql
        except:
            print 'error----',sql








    def _handle_error(self, failue, item, spider):
        self.logger.error(failue)