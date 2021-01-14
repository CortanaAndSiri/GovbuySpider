# -*- coding: utf-8 -*-
import hashlib
from dateutil.parser import parse
import time
import http.client
import hashlib
import json
import urllib
import random



class DealBidTools(object):
    baidu = [

        {'appid':'20181227000252503','secretKey':'aLpAFDSv3Wd0tjalytLp'},
        {'appid':'20181227000252505','secretKey':'LVIPhAOCX9tz3sJa07Hu'}
    ]
    @classmethod
    def compare_time(cls, date_time):
        """
        比较时间，如果传入的当前时间大于当前时间，返回
        :param date_time:
        :return:
        """
        data_time = parse(date_time).timestamp()
        today_time = int(time.time()) - int(time.time())%86400 + time.timezone
        if data_time >= today_time:
            return True
        else:
            return False

    @classmethod
    def deal_time(cls, strtime, timesTmp=False):
        """
        处理时间
        :param strtime: 任意格式的时间
        :param timesTmp: 默认为False,返回%Y-%m-%d日期，如果设置为True,返回时间戳
        :return:
        """
        if timesTmp:
            time = parse(strtime).timestamp()
            return int(time)
        else:
            time = parse(strtime).date()
            return str(time)

    @classmethod
    def extract_cookies(cls, cookie):
        """
        从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies
        """
        cookies = dict([l.split("=", 1) for l in cookie.split("; ")])
        return cookies

    @classmethod
    def md5(cls, url):
        """
        将url通过hashlib编码
        """
        hash = hashlib.md5()
        hash.update(url.encode('utf-8'))
        return hash.hexdigest()

    @classmethod
    def bd_trans(cls, content):
        i = random.randint(0, (len(cls.baidu)-1))
        appid = cls.baidu[i]['appid']
        secretKey = cls.baidu[i]['secretKey']
        httpClient = None
        myurl = '/api/trans/vip/translate'
        q = content
        fromLang = 'en'  # 源语言
        toLang = 'zh'  # 翻译后的语言
        salt = random.randint(32768, 65536)
        sign = appid + q + str(salt) + secretKey
        sign = hashlib.md5(sign.encode()).hexdigest()
        myurl = myurl + '?appid=' + appid + '&q=' + urllib.parse.quote(
            q) + '&from=' + fromLang + '&to=' + toLang + '&salt=' + str(
            salt) + '&sign=' + sign

        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            # response是HTTPResponse对象
            response = httpClient.getresponse()
            jsonResponse = response.read().decode("utf-8")  # 获得返回的结果，结果为json格式
            js = json.loads(jsonResponse)  # 将json格式的结果转换字典结构
            dst = str(js["trans_result"][0]["dst"])  # 取得翻译后的文本结果
            return dst # 打印结果
        except Exception as e:
            print(e)
        finally:
            if httpClient:
                httpClient.close()