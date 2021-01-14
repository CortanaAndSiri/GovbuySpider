# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import random,json

from scrapy.pipelines.files import FilesPipeline, FileException
from scrapy.utils.request import referer_str
import re
import os
from scrapy.utils.misc import md5sum
from scrapy.utils.python import to_bytes
from urllib import parse as urlparse
import pymysql
import scrapy
from twisted.enterprise import adbapi
import time
import hashlib
from scrapy.exceptions import DropItem
import redis
import logging
from utils.tools import DealBidTools
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

logger = logging.getLogger(__name__)


class GovbuySpiderPipeline(object):
    """
    数据加工
    """
    def __init__(self, con_redis):
        self.con_redis = con_redis

    @classmethod
    def from_settings(cls, settings):
        con_redis = redis.StrictRedis(
            host=settings['REDIS_HOST'],
            port=settings['REDIS_PORT'],
            db=settings['REDIS_DB'],
            password=settings['REDIS_PWD']
        )
        return cls(con_redis)

    def process_item(self, item, spider):
        print(item)
        if self._deal_repeat_down(item["redis_value"] if item.get("redis_value") else item["bid_url"]):
            # if 'service' in item['title'].lower():
            #     item['catid'] = '8'
            category = {"1": "0001:", "2": "0002:", "3": "0003:", "4": "0004:", "5": "0005:", "6": "0006:", "7": "0007:", "8": "0008:", "9": "0009:", "10": "0010:", "11": "0011:", "12": "0012:", "13": "0013:", "14": "0014:",  "15": "0015:", "16": "0016:", "17": "0017:", "18": "0018:", "19": "0019:", "20": "0020:", "21": "0021:", "22": "0022:", "23": "0023:", "976": "0976:", "977": "0977:", "978": "0978:", "979": "0979:"}
            if item['catid'] in category:
                item["catpath"] = category[str(item['catid'])]
            else:
                item["catpath"] = '0'

            item["secure"], item["status"] = 0, 0
            item["uptime"] = int(time.time())
            item["expire"] = DealBidTools.deal_time(item['expiredate'])
            item["dtime"] = DealBidTools.deal_time(item['issuedate'], timesTmp=True) if item['issuedate'] else int(time.time())
            item['links'] = str(item['links']).replace("'",'"') if item.get('links') else ''

            return item
        else:

            print('*'*50)
            print("有重复")
            print('*'*50)

            raise DropItem(item)



    def _deal_repeat_down(self, redis_value):
        """
        处理没有详情页面url，通过redis_value进行增量去重
        :param redis_value:
        :return: 没有重复，返回True，否则，返回False
        """
        url = DealBidTools.md5(redis_value)
        return not self.con_redis.exists('url:%s' % url)


class DownloadFilesPipeline(FilesPipeline):
    """
    自定义下载组件
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    user_agents = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
        "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"]

    def get_media_requests(self, item, info):
        if item.get("formdata"):
            for data in item["formdata"]:
                yield scrapy.FormRequest(url=item["post_url"], formdata=data, headers={"user-agent": random.choice(self.user_agents)}, meta={"data": data})
        elif item.get("file_urls"):
            if item.get("cookies"):
                for url in item['file_urls']:
                    yield scrapy.Request(url, headers={"user-agent": random.choice(self.user_agents)}, cookies=item["cookies"])
            else:
                for url in item['file_urls']:
                    yield scrapy.Request(url, headers={"user-agent": random.choice(self.user_agents)},)
        else:
            print('*'*50)
            print('下载失败')
            print('*'*50)
            return item

    def media_downloaded(self, response, request, info):
        """
        从content-dispositon中取文件名
        :param response:
        :param request:
        :param info:
        :return:
        """
        referer = referer_str(request)
        if response.status != 200:
            logger.warning(
                'File (code: %(status)s): Error downloading file from '
                '%(request)s referred in <%(referer)s>',
                {'status': response.status,
                 'request': request, 'referer': referer},
                extra={'spider': info.spider}
            )
            raise FileException('download-error')
        if not response.body:
            logger.warning(
                'File (empty-content): Empty file from %(request)s referred '
                'in <%(referer)s>: no-content',
                {'request': request, 'referer': referer},
                extra={'spider': info.spider}
            )
            raise FileException('empty-content')
        status = 'cached' if 'cached' in response.flags else 'downloaded'
        logger.debug(
            'File (%(status)s): Downloaded file from %(request)s referred in '
            '<%(referer)s>',
            {'status': status, 'request': request, 'referer': referer},
            extra={'spider': info.spider}
        )
        self.inc_stats(info.spider, status)

        try:
            containFileName = response.headers.get('Content-Disposition') or response.headers.get('content-disposition')
            if containFileName is not None:
                pattern_marks = re.compile(r'filename="(.*)"')
                pattern_no_marks = re.compile(r'filename=(.*)')
                try:
                    file_name = pattern_marks.search(containFileName.decode('utf-8')) or pattern_no_marks.search(containFileName.decode('utf-8'))
                except:
                    file_name = pattern_marks.search(str(containFileName).split("'")[1]) or pattern_no_marks.search(str(containFileName).split("'")[1])
                if file_name is not None:
                    file_name = urlparse.unquote(file_name.group(1).strip())
                else:
                    file_name = urlparse.unquote(os.path.basename(urlparse.unquote(response.request.url)))
            else:
                file_name = urlparse.unquote(os.path.basename(urlparse.unquote(response.request.url)))
            media_ext = os.path.splitext(file_name)[1]
            if "." not in media_ext or "\\" in media_ext or "/" in media_ext or ":" in media_ext or "*" in media_ext or "?" in media_ext or '"' in media_ext or "<" in media_ext or ">" in media_ext or "|" in media_ext or ";" in media_ext:
                content_type = response.headers.get('Content-Type') or response.headers.get('content-type')
                file_type = "." + content_type.decode('utf-8').split("/")[-1]
                file_name = str(int(time.time())) + file_type
                media_ext = file_type
            if response.meta.get("data"):
                url = request.url + urlparse.urlencode(response.meta["data"])
            else:
                url = request.url
            media_guid = hashlib.sha1(to_bytes(url)).hexdigest()
            path = 'full/%s%s' % (media_guid, media_ext)
            checksum = self.file_downloaded(response, request, info, path)
        except FileException as exc:
            logger.warning(
                'File (error): Error processing file from %(request)s '
                'referred in <%(referer)s>: %(errormsg)s',
                {'request': request, 'referer': referer, 'errormsg': str(exc)},
                extra={'spider': info.spider}, exc_info=True
            )
            raise
        except Exception as exc:
            logger.error(
                'File (unknown-error): Error processing file from %(request)s '
                'referred in <%(referer)s>',
                {'request': request, 'referer': referer},
                exc_info=True, extra={'spider': info.spider}
            )
            raise FileException(str(exc))

        return {'url': urlparse.unquote(url), 'path': path, 'checksum': checksum, "name": file_name}

    def file_downloaded(self, response, request, info, path):
        """
        重定义文件下载
        """
        buf = BytesIO(response.body)
        checksum = md5sum(buf)
        buf.seek(0)
        self.store.persist_file(path, buf, info)

        return checksum


class InsertDBPipeline(object):
    """
    将数据录入数据库
    """
    insert_govbuy_con = '''insert into govbuy_con(con_menuid, cat_id, cat_path, con_title, con_area, con_body, con_name, con_phone, con_email, con_dtime, con_uptime, con_extime, web_url, con_url, con_auth, region_id, secure, status, con_ex1, con_ex2) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
    update_govbuy_cat = '''update govbuy_cat set cat_nums = cat_nums + 1 where cat_id= %s'''
    update_govbuy_region = '''update govbuy_cat set cat_nums = cat_nums + 1 where cat_id= %s'''
    insert_govbuy_pdf = '''insert into govbuy_pdf(pdf_gid, pdf_path, pdf_name) values(%s, %s, %s)'''


    def __init__(self, dbpool, con_redis):
        self.dbpool = dbpool
        self.con_redis = con_redis

    @classmethod
    def from_settings(cls, settings):
        # 将pymysql当作mysqldb来用
        pymysql.install_as_MySQLdb()
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        con_redis = redis.StrictRedis(
            host=settings['REDIS_HOST'],
            port=settings['REDIS_PORT'],
            db=settings['REDIS_DB'],
            password=settings['REDIS_PWD']
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbargs)
        return cls(dbpool, con_redis)

    def process_item(self, item, spider):

        if item.get('file_urls') or item.get('formdata'):
            if item.get("formdata"):
                if len(item["formdata"]) == len(item["files"]):
                    query = self.dbpool.runInteraction(self._insert_govbuy_con, item, spider, files=True)
                    query.addErrback(self._handle_error, item, spider)
                    url = DealBidTools.md5(item["redis_value"] if item.get("redis_value") else item["bid_url"])
                    self.con_redis.set('url:%s' % url, 1)
                    return item
            else:
                if len(item["file_urls"]) == len(item["files"]):
                    query = self.dbpool.runInteraction(self._insert_govbuy_con, item, spider, files=True)
                    print(query)
                    query.addErrback(self._handle_error, item, spider)
                    url = DealBidTools.md5(item["redis_value"] if item.get("redis_value") else item["bid_url"])
                    self.con_redis.set('url:%s' % url, 1)
                    return item
        else:
            query = self.dbpool.runInteraction(self._insert_govbuy_con, item, spider)
            query.addErrback(self._handle_error, item, spider)
            url = DealBidTools.md5(item["redis_value"] if item.get("redis_value") else item["bid_url"])
            self.con_redis.set('url:%s' % url, 1)
            return item
        return item

    def _insert_govbuy_con(self, conn, item, spider, files=False):
        if item['region_id'] != '27':
            item['trans'] = DealBidTools.bd_trans(item['title'])
        if not item['trans']:
            item['trans'] = item['title']
        params = (item['menuid'], item['catid'], item['catpath'], item['title'], item['memo'], item['body'], item['contact'],  item['phone'], item['email'],  item['dtime'], item['uptime'], item['expire'], item['web_url'], item['bid_url'], spider.name, item['region_id'], item['secure'], item['status'], item['trans'], item['links'])
        conn_row = conn.execute(self.insert_govbuy_con, params)



        # conn.commit()
        if conn_row == 1:
            item['gid'] = conn.lastrowid
            self._update_govbuy_cat(conn, item['catid'], item['region_id'])
            if files:
                self._insert_govbuy_pdf(conn, item)
        else:
            print('*'*50)
            print("插入govbuy_con表失败")
            print('*'*50)

    def _update_govbuy_cat(self, conn, cat_id, region_id):
        """
        更新栏目内容数量统计
        :param:int:catid:栏目ID
        """
        print('*'*50)
        if region_id != '27':
            conn_row = conn.execute(self.update_govbuy_cat, (str(cat_id)))

            if conn_row != 1:
                print("栏目数量更新失败")
        conn_row = conn.execute(self.update_govbuy_region, (str(region_id)))
        if conn_row != 1:
            print("栏目数量更新失败")

    def _insert_govbuy_pdf(self, conn, item):
        for file in item['files']:
            conn_row = conn.execute(self.insert_govbuy_pdf, (item['gid'], file['path'], file['name']))
            if conn_row != 1:
                print("插入govbuy_pdf表失败")

    def _handle_error(self, failue, item, spider):
        print(failue)
        print(spider.name)
        raise DropItem(item)









class Ceshi(object):
    def open_spider(self,spider):
        print('*' * 50)
        self.file = open('ceshi.json','w',encoding='utf-8')
    def process_item(self, item, spider):


        print('*'*50)
        json_str = json.dumps(dict(item),ensure_ascii=False)
        self.file.write(json_str+'\n')
        return item

    def close_spider(self,spider):
        self.file.close()



































































# # -*- coding: utf-8 -*-

# # Define your item pipelines here
# #
# # Don't forget to add your pipeline to the ITEM_PIPELINES setting
# # See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import random

# from scrapy.pipelines.files import FilesPipeline, FileException
# from scrapy.utils.request import referer_str
# import re
# import os
# from scrapy.utils.misc import md5sum
# from scrapy.utils.python import to_bytes
# from urllib import parse as urlparse
# import pymysql
# import scrapy
# from twisted.enterprise import adbapi
# import time
# import hashlib
# from scrapy.exceptions import DropItem
# import redis
# import logging
# from utils.tools import DealBidTools
# try:
#     from cStringIO import StringIO as BytesIO
# except ImportError:
#     from io import BytesIO

# logger = logging.getLogger(__name__)


# class GovbuySpiderPipeline(object):
#     """
#     数据加工
#     """
#     def __init__(self, con_redis):
#         self.con_redis = con_redis

#     @classmethod
#     def from_settings(cls, settings):
#         con_redis = redis.StrictRedis(
#             host=settings['REDIS_HOST'],
#             port=settings['REDIS_PORT'],
#             db=settings['REDIS_DB'],
#             # password = settings['REDIS_PWD']
#         )
#         return cls(con_redis)

#     def process_item(self, item, spider):
#         if self._deal_repeat_down(item["redis_value"] if item.get("redis_value") else item["bid_url"]):
#             category = {"1": "0001:", "2": "0002:", "3": "0003:", "4": "0004:", "5": "0005:", "6": "0006:", "7": "0007:", "8": "0008:", "9": "0009:", "10": "0010:", "11": "0011:", "12": "0012:", "13": "0013:", "14": "0014:",  "15": "0015:", "16": "0016:", "17": "0017:", "18": "0018:", "19": "0019:", "20": "0020:", "21": "0021:", "22": "0022:", "23": "0023:", "976": "0976:", "977": "0977:", "978": "0978:", "979": "0979:"}
#             item["catpath"] = category[str(item['catid'])]
#             item["secure"], item["status"] = 0, 0
#             item["uptime"] = int(time.time())
#             item["expire"] = DealBidTools.deal_time(item['expiredate'])
#             item["dtime"] = DealBidTools.deal_time(item['issuedate'], timesTmp=True) if item['issuedate'] else int(time.time())
#             return item
#         else:
#             raise DropItem(item)

#     def _deal_repeat_down(self, redis_value):
#         """
#         处理没有详情页面url，通过redis_value进行增量去重
#         :param redis_value:
#         :return: 没有重复，返回True，否则，返回False
#         """
#         url = DealBidTools.md5(redis_value)
#         return not self.con_redis.exists('url:%s' % url)


# class DownloadFilesPipeline(FilesPipeline):
#     """
#     自定义下载组件
#     """
#     headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
#     user_agents = [
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
#         "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
#         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
#         "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
#         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
#         "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#         "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
#         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
#         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#         "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#         "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
#         "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
#         "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
#         "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
#         "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
#         "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
#         "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
#         "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
#         "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
#         "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
#         "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
#         "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
#         "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
#         "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
#         "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
#         "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"]

#     def get_media_requests(self, item, info):
#         if item.get("formdata"):
#             # print ('------------pipeline-formdata-------',item["formdata"],'------------pipeline-formdata-------',len(item["formdata"]),type(item["formdata"]))
#             # time.sleep(5)
#             for data in item["formdata"]:
#                 yield scrapy.FormRequest(url=item["post_url"], formdata=data, headers={"user-agent": random.choice(self.user_agents)}, meta={"data": data})
#         elif item.get("file_urls"):
#             if item.get("cookies"):
#                 for url in item['file_urls']:
#                     yield scrapy.Request(url, headers={"user-agent": random.choice(self.user_agents)}, cookies=item["cookies"])
#             else:
#                 for url in item['file_urls']:
#                     yield scrapy.Request(url, headers={"user-agent": random.choice(self.user_agents)},)
#         else:
#             return item

#     def media_downloaded(self, response, request, info):
#         """
#         从content-dispositon中取文件名
#         :param response:
#         :param request:
#         :param info:
#         :return:
#         """
#         referer = referer_str(request)
#         if response.status != 200:
#             logger.warning(
#                 'File (code: %(status)s): Error downloading file from '
#                 '%(request)s referred in <%(referer)s>',
#                 {'status': response.status,
#                  'request': request, 'referer': referer},
#                 extra={'spider': info.spider}
#             )
#             raise FileException('download-error')
#         if not response.body:
#             logger.warning(
#                 'File (empty-content): Empty file from %(request)s referred '
#                 'in <%(referer)s>: no-content',
#                 {'request': request, 'referer': referer},
#                 extra={'spider': info.spider}
#             )
#             raise FileException('empty-content')
#         status = 'cached' if 'cached' in response.flags else 'downloaded'
#         logger.debug(
#             'File (%(status)s): Downloaded file from %(request)s referred in '
#             '<%(referer)s>',
#             {'status': status, 'request': request, 'referer': referer},
#             extra={'spider': info.spider}
#         )
#         self.inc_stats(info.spider, status)

#         try:
#             containFileName = response.headers.get('Content-Disposition') or response.headers.get('content-disposition')
#             if containFileName is not None:
#                 pattern_marks = re.compile(r'filename="(.*)"')
#                 pattern_no_marks = re.compile(r'filename=(.*)')
#                 try:
#                     file_name = pattern_marks.search(containFileName.decode('utf-8')) or pattern_no_marks.search(containFileName.decode('utf-8'))
#                 except:
#                     file_name = pattern_marks.search(str(containFileName).split("'")[1]) or pattern_no_marks.search(str(containFileName).split("'")[1])
#                 if file_name is not None:
#                     file_name = urlparse.unquote(file_name.group(1).strip())
#                 else:
#                     file_name = urlparse.unquote(os.path.basename(urlparse.unquote(response.request.url)))
#             else:
#                 file_name = urlparse.unquote(os.path.basename(urlparse.unquote(response.request.url)))
#             media_ext = os.path.splitext(file_name)[1]
#             if "." not in media_ext or "\\" in media_ext or "/" in media_ext or ":" in media_ext or "*" in media_ext or "?" in media_ext or '"' in media_ext or "<" in media_ext or ">" in media_ext or "|" in media_ext:
#                 content_type = response.headers.get('Content-Type') or response.headers.get('content-type')
#                 file_type = "." + content_type.decode('utf-8').split("/")[-1]
#                 file_name = str(int(time.time())) + file_type
#                 media_ext = file_type
#             if response.meta.get("data"):
#                 url = request.url + urlparse.urlencode(response.meta["data"])
#             else:
#                 url = request.url
#             media_guid = hashlib.sha1(to_bytes(url)).hexdigest()
#             path = 'full/%s%s' % (media_guid, media_ext)
#             checksum = self.file_downloaded(response, request, info, path)
#         except FileException as exc:
#             logger.warning(
#                 'File (error): Error processing file from %(request)s '
#                 'referred in <%(referer)s>: %(errormsg)s',
#                 {'request': request, 'referer': referer, 'errormsg': str(exc)},
#                 extra={'spider': info.spider}, exc_info=True
#             )
#             raise
#         except Exception as exc:
#             logger.error(
#                 'File (unknown-error): Error processing file from %(request)s '
#                 'referred in <%(referer)s>',
#                 {'request': request, 'referer': referer},
#                 exc_info=True, extra={'spider': info.spider}
#             )
#             raise FileException(str(exc))

#         return {'url': urlparse.unquote(url), 'path': path, 'checksum': checksum, "name": file_name}

#     def file_downloaded(self, response, request, info, path):
#         """
#         重定义文件下载
#         """
#         buf = BytesIO(response.body)
#         checksum = md5sum(buf)
#         buf.seek(0)
#         self.store.persist_file(path, buf, info)
#         return checksum


# class InsertDBPipeline(object):
#     """
#     将数据录入数据库
#     """
#     insert_govbuy_con = '''insert into govbuy_con(con_menuid, cat_id, cat_path, con_title, con_area, con_body, con_name, con_phone, con_email, con_dtime, con_uptime, con_extime, web_url, con_url, con_auth, region_id, secure, status, con_ex1) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
#     update_govbuy_cat = '''update govbuy_cat set cat_nums = cat_nums + 1 where cat_id= %s'''
#     update_govbuy_region = '''update govbuy_cat set cat_nums = cat_nums + 1 where cat_id= %s'''
#     insert_govbuy_pdf = '''insert into govbuy_pdf(pdf_gid, pdf_path, pdf_name) values(%s, %s, %s)'''


#     def __init__(self, dbpool, con_redis):
#         self.dbpool = dbpool
#         self.con_redis = con_redis

#     @classmethod
#     def from_settings(cls, settings):
#         # 将pymysql当作mysqldb来用
#         pymysql.install_as_MySQLdb()
#         dbargs = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset='utf8',
#             cursorclass=pymysql.cursors.DictCursor,
#             use_unicode=True
#         )
#         con_redis = redis.StrictRedis(
#             host=settings['REDIS_HOST'],
#             port=settings['REDIS_PORT'],
#             db=settings['REDIS_DB'],
#             # password = settings['REDIS_PWD']
#         )
#         dbpool = adbapi.ConnectionPool("MySQLdb", **dbargs)
#         return cls(dbpool, con_redis)

#     def process_item(self, item, spider):
#         if item.get('file_urls') or item.get('formdata'):
#             if item.get("formdata"):
#                 if len(item["formdata"]) == len(item["files"]):
#                     query = self.dbpool.runInteraction(self._insert_govbuy_con, item, spider, files=True)
#                     query.addErrback(self._handle_error, item, spider)
#                     url = DealBidTools.md5(item["redis_value"] if item.get("redis_value") else item["bid_url"])
#                     self.con_redis.set('url:%s' % url, 1)
#                     return item
#             else:
#                 if len(item["file_urls"]) == len(item["files"]):
#                     query = self.dbpool.runInteraction(self._insert_govbuy_con, item, spider, files=True)
#                     print(query)
#                     query.addErrback(self._handle_error, item, spider)
#                     url = DealBidTools.md5(item["redis_value"] if item.get("redis_value") else item["bid_url"])
#                     self.con_redis.set('url:%s' % url, 1)
#                     return item
#         else:
#             query = self.dbpool.runInteraction(self._insert_govbuy_con, item, spider)
#             query.addErrback(self._handle_error, item, spider)
#             url = DealBidTools.md5(item["redis_value"] if item.get("redis_value") else item["bid_url"])
#             self.con_redis.set('url:%s' % url, 1)
#             return item
#         return item

#     def _insert_govbuy_con(self, conn, item, spider, files=False):
#         item['trans'] = item['title']
#         if item['region_id'] != '27':
#             item['trans'] = DealBidTools.bd_trans(item['title'])
#         params = (item['menuid'], item['catid'], item['catpath'], item['title'], item['memo'], item['body'], item['contact'],  item['phone'], item['email'],  item['dtime'], item['uptime'], item['expire'], item['web_url'], item['bid_url'], spider.name, item['region_id'], item['secure'], item['status'], item['trans'])
#         conn_row = conn.execute(self.insert_govbuy_con, params)
#         # conn.commit()
#         if conn_row == 1:
#             item['gid'] = conn.lastrowid
#             self._update_govbuy_cat(conn, item['catid'], item['region_id'])
#             if files:
#                 self._insert_govbuy_pdf(conn, item)
#         else:
#             print("插入govbuy_con表失败")


#     def _update_govbuy_cat(self, conn, cat_id, region_id):
#         """
#         更新栏目内容数量统计
#         :param:int:catid:栏目ID
#         """
#         if region_id != '27':
#             conn_row = conn.execute(self.update_govbuy_cat, (str(cat_id)))
#             if conn_row != 1:
#                 print("栏目数量更新失败")
#         conn_row = conn.execute(self.update_govbuy_region, (str(region_id)))
#         if conn_row != 1:
#             print("栏目数量更新失败")

#     def _insert_govbuy_pdf(self, conn, item):
#         for file in item['files']:
#             conn_row = conn.execute(self.insert_govbuy_pdf, (item['gid'], file['path'], file['name']))
#             if conn_row != 1:
#                 print("插入govbuy_pdf表失败")

#     def _handle_error(self, failue, item, spider):
#         print(failue)
#         print(spider.name)
#         raise DropItem(item)


