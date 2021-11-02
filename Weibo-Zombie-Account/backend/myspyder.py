import codecs
import copy
import csv
import json
import math
import os
import random
import sys
import traceback
from collections import OrderedDict
from datetime import date, datetime, timedelta
from time import sleep

import requests
from lxml import etree
from requests.adapters import HTTPAdapter


class Myspyder(object):

    def __init__(self, id):
        self.got_count = 0
        self.weibo = []
        self.id = id
        self.alllike = 0
        self.allrepo = 0
        self.allcomm = 0
        self.retweets = 0
        self.original = 0

    def get_json(self, params):
        """获取网页中json数据"""
        url = 'https://m.weibo.cn/api/container/getIndex?'  # !这一句非常重要！
        print(params)
        r = requests.get(url, params=params)
        return r.json()

    def get_weibo_json(self, page):
        """获取网页中微博json数据"""
        params = {
            'containerid': '107603' + str(self.id),
            'page': page
        }
        js = self.get_json(params)
        return js

    def get_long_weibo(self, id):
        """获取长微博"""
        url = 'https://m.weibo.cn/detail/%s' % id
        html = requests.get(url).text
        html = html[html.find('"status":'):]
        html = html[:html.rfind('"hotScheme"')]
        html = html[:html.rfind(',')]
        html = '{' + html + '}'
        js = json.loads(html, strict=False)
        weibo_info = js.get('status')
        if weibo_info:
            weibo = self.parse_weibo(weibo_info)
            return weibo

    def get_location(self, selector):
        """获取微博发布位置"""
        location_icon = 'timeline_card_small_location_default.png'
        span_list = selector.xpath('//span')
        location = ''
        for i, span in enumerate(span_list):
            if span.xpath('img/@src'):
                if location_icon in span.xpath('img/@src')[0]:
                    location = span_list[i + 1].xpath('string(.)')
                    break
        return location

    def get_topics(self, selector):
        """获取参与的微博话题"""
        span_list = selector.xpath("//span[@class='surl-text']")
        topics = ''
        topic_list = []
        for span in span_list:
            text = span.xpath('string(.)')
            if len(text) > 2 and text[0] == '#' and text[-1] == '#':
                topic_list.append(text[1:-1])
        if topic_list:
            topics = ','.join(topic_list)
        return topics

    def get_at_users(self, selector):
        """获取@用户"""
        a_list = selector.xpath('//a')
        at_users = ''
        at_list = []
        for a in a_list:
            if '@' + a.xpath('@href')[0][3:] == a.xpath('string(.)'):
                at_list.append(a.xpath('string(.)')[1:])
        if at_list:
            at_users = ','.join(at_list)
        return at_users

    def string_to_int(self, string):
        """字符串转换为整数"""
        if isinstance(string, int):
            return string
        elif string.endswith(u'万+'):
            string = int(string[:-2] + '0000')
        elif string.endswith(u'万'):
            string = int(string[:-1] + '0000')
        return int(string)

    def standardize_date(self, created_at):
        """标准化微博发布时间"""
        if u"刚刚" in created_at:
            created_at = datetime.now().strftime("%Y-%m-%d")
        elif u"分钟" in created_at:
            minute = created_at[:created_at.find(u"分钟")]
            minute = timedelta(minutes=int(minute))
            created_at = (datetime.now() - minute).strftime("%Y-%m-%d")
        elif u"小时" in created_at:
            hour = created_at[:created_at.find(u"小时")]
            hour = timedelta(hours=int(hour))
            created_at = (datetime.now() - hour).strftime("%Y-%m-%d")
        elif u"昨天" in created_at:
            day = timedelta(days=1)
            created_at = (datetime.now() - day).strftime("%Y-%m-%d")
        elif created_at.count('-') == 1:
            year = datetime.now().strftime("%Y")
            created_at = year + "-" + created_at
        return created_at

    def standardize_info(self, weibo):
        """标准化信息，去除乱码"""
        for k, v in weibo.items():
            if 'bool' not in str(type(v)) and 'int' not in str(type(v)) and 'list' not in str(type(v)) and 'long' not in str(type(v)):
                weibo[k] = v.replace(u"\u200b", "").encode(
                    sys.stdout.encoding, "ignore").decode(sys.stdout.encoding)
        return weibo

    def parse_weibo(self, weibo_info):
        weibo = OrderedDict()
        if weibo_info['user']:
            weibo['user_id'] = weibo_info['user']['id']
            weibo['screen_name'] = weibo_info['user']['screen_name']
        else:
            weibo['user_id'] = ''
            weibo['screen_name'] = ''
        weibo['id'] = int(weibo_info['id'])
        weibo['bid'] = weibo_info['bid']
        text_body = weibo_info['text']
        selector = etree.HTML(text_body)
        weibo['text'] = etree.HTML(text_body).xpath('string(.)')
        weibo['location'] = self.get_location(selector)
        weibo['created_at'] = weibo_info['created_at']
        weibo['source'] = weibo_info['source']
        weibo['attitudes_count'] = self.string_to_int(
            weibo_info.get('attitudes_count', 0))
        weibo['comments_count'] = self.string_to_int(
            weibo_info.get('comments_count', 0))
        weibo['reposts_count'] = self.string_to_int(
            weibo_info.get('reposts_count', 0))
        weibo['topics'] = self.get_topics(selector)
        weibo['at_users'] = self.get_at_users(selector)
        return self.standardize_info(weibo)

    def get_page_count(self, user):
        """获取微博页数"""
        try:
            weibo_count = user['statuses_count']
            page_count = int(math.ceil(weibo_count / 10.0))
            return page_count
        except KeyError:
            sys.exit(u'程序出错，错误原因可能为以下两者：\n'
                     u'1.user_id不正确；\n'
                     u'2.此用户微博可能需要设置cookie才能爬取。\n'
                     u'解决方案：\n'
                     u'请参考\n'
                     u'https://github.com/dataabc/weibo-crawler#如何获取user_id\n'
                     u'获取正确的user_id；\n'
                     u'或者参考\n'
                     u'https://github.com/dataabc/weibo-crawler#3程序设置\n'
                     u'中的“设置cookie”部分设置cookie信息')

    def get_one_weibo(self, info):
        """获取一条微博的全部信息"""
        try:
            weibo_info = info['mblog']
            weibo_id = weibo_info['id']
            retweeted_status = weibo_info.get('retweeted_status')
            is_long = weibo_info.get('isLongText')
            if retweeted_status:  # 转发
                self.retweets += 1
                retweet_id = retweeted_status.get('id')
                is_long_retweet = retweeted_status.get('isLongText')
                if is_long:
                    weibo = self.get_long_weibo(weibo_id)
                    if not weibo:
                        weibo = self.parse_weibo(weibo_info)
                else:
                    weibo = self.parse_weibo(weibo_info)
                if is_long_retweet:
                    retweet = self.get_long_weibo(retweet_id)
                    if not retweet:
                        retweet = self.parse_weibo(retweeted_status)
                else:
                    retweet = self.parse_weibo(retweeted_status)
                retweet['created_at'] = self.standardize_date(
                    retweeted_status['created_at'])
                weibo['retweet'] = retweet
            else:  # 原创
                self.original += 1
                if is_long:
                    weibo = self.get_long_weibo(weibo_id)
                    if not weibo:
                        weibo = self.parse_weibo(weibo_info)
                else:
                    weibo = self.parse_weibo(weibo_info)
            weibo['created_at'] = self.standardize_date(
                weibo_info['created_at'])
            return weibo
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_one_page(self, page):
        """获取一页的全部微博"""
        try:
            print('正在爬取第'+str(page)+'页')
            js = self.get_weibo_json(page)
            if js['ok']:
                weibos = js['data']['cards']
                for w in weibos:
                    if w['card_type'] == 9:
                        wb = self.get_one_weibo(w)  # wb存储了所需信息
                        self.alllike += wb['attitudes_count']
                        self.allcomm += wb['comments_count']
                        self.allrepo += wb['reposts_count']
                        self.weibo.append(wb)
                        self.got_count += 1
        except Exception as e:
            print("Error: ", e)
            traceback.print_exc()

    def get_pages(self, user):
        """获取全部微博"""
        page_count = self.get_page_count(user)
        wrote_count = 0
        page1 = 0
        random_pages = random.randint(1, 5)
        start_date = datetime.now().strftime('%Y-%m-%d')
        for page in range(1, min(page_count + 1, 11)):
            is_end = self.get_one_page(page)  # page是一个整数
            if is_end:
                break
            if page % 5 == 0:
                sleep(random.randint(3, 6))
        print(u'微博爬取完成，共爬取%d条微博' % self.got_count)

    def start(self):
        params = {'containerid': '100505' +
                  str(self.id)}
        js = self.get_json(params)
        print(js)
        if js['ok']:
            info = js['data']['userInfo']
            user_info = {}
            user_info['id'] = self.id
            user_info['screen_name'] = info.get('screen_name', '')
            user_info['gender'] = info.get('gender', '')
            user_info['statuses_count'] = info.get('statuses_count', 0)
            user_info['followers_count'] = info.get('followers_count', 0)
            user_info['follow_count'] = info.get('follow_count', 0)
            user_info['description'] = info.get('description', '')
            user_info['profile_url'] = info.get('profile_url', '')
            user_info['profile_image_url'] = info.get('profile_image_url', '')
            user_info['avatar_hd'] = info.get('avatar_hd', '')
            user_info['urank'] = info.get('urank', 0)
            user_info['mbrank'] = info.get('mbrank', 0)
            user_info['verified'] = info.get('verified', False)
            user_info['verified_type'] = info.get('verified_type', 0)
            user_info['verified_reason'] = info.get('verified_reason', '')
            # print(user_info)  # 到此为止完成基本信息读取
            user = self.standardize_info(user_info)

            self.get_pages(user)

            self.userinfo = user
            self.userinfo['retweets'] = self.retweets
            self.userinfo['original'] = self.original
            self.userinfo['dalllike'] = self.alllike/self.got_count
            self.userinfo['dallrepo'] = self.allrepo/self.got_count
            self.userinfo['dallcomm'] = self.allcomm/self.got_count

        else:
            print('information failed')


def main():
    id = '1669879400'
    spy = Myspyder(id)
    spy.start()


if __name__ == '__main__':
    main()
