# -*- coding: utf-8 -*-

from hashlib import md5
from flask_restful import reqparse
from util.log import LogHandler
import base64
import re
from lxml import etree
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr

import zlib
import json
import bson.binary


make_md5 = lambda string: md5(string.encode()).hexdigest()
log = LogHandler(__name__)


class GetDictParam:
    """
        这是一个解析dict 参数的类
        可以用于多参数的指定key 、 指定key集合解析key
    """
    @classmethod
    def get_value(cls, my_dict: dict, key: str):
        """
            这是一个递归函数
        """
        if isinstance(my_dict, dict):
            if my_dict.get(key) or my_dict.get(key) == 0 or my_dict.get(key) == ''\
                    and my_dict.get(key) is False or my_dict.get(key) == []:
                return my_dict.get(key)

            for my_dict_key in my_dict:
                if cls.get_value(my_dict.get(my_dict_key), key) or \
                                cls.get_value(my_dict.get(my_dict_key), key) is False:
                    return cls.get_value(my_dict.get(my_dict_key), key)

        if isinstance(my_dict, list):
            for my_dict_arr in my_dict:
                if cls.get_value(my_dict_arr, key) \
                        or cls.get_value(my_dict_arr, key) is False:
                    return cls.get_value(my_dict_arr, key)

    @classmethod
    def list_for_key_to_dict(cls, *args: tuple, my_dict: dict) -> dict:
        """
            接收需要解析的dict和 需要包含需要解析my_dict的keys的list
        :param my_dict: 需要解析的字典
        :param args: 包含需要解析的key的多个字符串
            # list_for_key_to_dict("code", "pageNo", "goodsId", my_dict=dict)
        :return: 一个解析后重新拼装的dict
        """
        result = {}
        if len(args) > 0:
            for key in args:
                result.update({key: cls.get_value(my_dict, key)})
        return result


class ParseRequestParameters(GetDictParam):
    def __init__(self, params: reqparse.RequestParser):
        self.args = params.parse_args()

    def check(self, check_body):
        check_body = self.list_for_key_to_dict(*check_body, my_dict=self.args)
        make_md5_params = ""
        for key, value in check_body.items():
            if isinstance(value, type(None)):
                value = ""
            make_md5_params += value
        md5 = make_md5(make_md5_params)
        return md5 == self.args["sign"]


class ShortenURL:
    _alphabet = '0123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNOPQRSTUVWXYZ-_'
    _base = len(_alphabet)

    def encode(self, number):
        string = ''
        while number > 0:
            string = self._alphabet[number % self._base] + string
            number //= self._base
        return string

    def decode(self, string):
        number = 0
        for char in string:
            number = number * self._base + self._alphabet.index(char)
        return number

def compress(info):
    return str(base64.b64encode(info.encode("utf-8")), "utf-8")


def cleantags(info):
    return re.sub(r'\n+|\s+|\t+|(\r\n)+','',info)


def get_text(info):
    try:
        text = etree.HTML(cleantags(info)).xpath('string(.)')
        if text:
            return text
        else:
            log.error('[text=null]')
    except ValueError as err:
        log.error('[error={} text={}]'.format(err,text))
        return False
    return False


def send_mail(sender, sender_pwd, sender_name, receivers, host, subject, body, format):
    msg = MIMEText(body,format, _charset='utf-8')
    format_from = formataddr([sender_name,sender])
    msg['Subject'] = subject
    msg['From'] = format_from
    msg['To'] = ",".join(receivers) if type(receivers) is list else receivers
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    try:
        s = smtplib.SMTP()
        s.connect(host)
        s.ehlo()
        s.esmtp_features['auth'] = 'LOGIN DIGEST-MD5 PLAIN'
        s.login(sender, sender_pwd)
        s.sendmail(sender, receivers, msg.as_string())
        s.close()
    except Exception as e:
        log.exception(e)
        return False
    return True


def zcompress(info):
    try:
        return bson.binary.Binary(zlib.compress(info.encode()))
    except Exception as e:
        log.exception('[zcompress error %s]',e)
    return ''

def zdecompress(info):
    detail = info.get('detail','')
    if detail and isinstance(detail, bytes):
        info['detail'] = zlib.decompress(detail).decode()
        return info
    return info


mapkv={'dy_163_com':'163news','百家号':'baijiahao','大风号':'dafenghao','腾讯新闻':'qiehao','搜狐新闻':'souhuxinwen','今日头条':'toutiaohao'}


def insert_middle_table(uri, publish_info, middle, url, uid):
    log.info('[uri={},publish_info={},url={},uid={}]'.format(uri,publish_info,url,uid))
    try:
        if uri == 'dy_163_com':
            #log.info({'_id':mapkv[uri]+':'+url,'type':mapkv[uri]})
            middle.save({'_id':mapkv[uri]+':'+url,'type':mapkv[uri]})
        elif publish_info == "百家号":
            if 'appId' in uid:
                uid = uid.split('appId:')[1].split(';')[0]
            #log.info({'_id':mapkv[publish_info]+':'+uid,'type':mapkv[publish_info]})
            middle.save({'_id':mapkv[publish_info]+':'+uid,'type':mapkv[publish_info]})
        else:
            if mapkv.get(publish_info):
                #log.info({'_id':mapkv[publish_info]+':'+uid,'type':mapkv[publish_info]})
                middle.save({'_id':mapkv[publish_info]+':'+uid,'type':mapkv[publish_info]})
    except Exception as e:
        log.exception('[insert_middle_table %s]',e)
