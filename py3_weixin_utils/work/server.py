#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from datetime import timedelta
from typing import Union

import diskcache
import httpx
import redis
from addict import Dict
from jsonschema.validators import Draft202012Validator
from py3_http_utils.response import HttpxResponseHandler


class Server(object):
    def __init__(self, agentid: Union[str, int] = "", corpid: str = "", corpsecret: str = "",
                 cache_instance: Union[diskcache.Cache, redis.Redis, redis.StrictRedis] = None):
        """
        服务端 API

        @see https://developer.work.weixin.qq.com/document/path/90664
        :param agentid: 应用id
        :param corpid: 企业id
        :param corpsecret: 应用的凭证密钥
        :param cache_instance: 缓存实例
        """
        self.gettoken_url_formatter = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
        self.gettoken_validate_json_schema = {
            "type": "object",
            "properties": {
                "access_token": {"type": "string", "minLength": 1},
            },
            "required": ["access_token"],
        }
        self.get_api_domain_ip_url_formatter = "https://qyapi.weixin.qq.com/cgi-bin/get_api_domain_ip?access_token={access_token}"
        self.get_api_domain_ip_validate_json_schema = {
            "type": "object",
            "properties": {
                "ip_list": {"type": "array", "minItems": 1},
            },
            "required": ["ip_list"],
        }
        self.message_send_url_formatter = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        self.message_send_validate_json_schema = {
            "type": "object",
            "properties": {
                "errcode": {
                    "oneOf": [
                        {"type": "integer", "const": 0},
                        {"type": "string", "const": "0"},
                    ]
                }
            },
            "required": ["errcode"],
        }
        self.media_upload_url_formatter = "https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type={f_type}"
        self.media_upload_validate_json_schema = {
            "type": "object",
            "properties": {
                "media_id": {"type": "string", "minLength": 1},
            },
            "required": ["media_id"],
        }
        self.media_uploadimg_url_formatter = "https://qyapi.weixin.qq.com/cgi-bin/media/uploadimg?access_token={access_token}"
        self.media_uploadimg_validate_json_schema = {
            "type": "object",
            "properties": {
                "url": {"type": "string", "minLength": 1},
            },
            "required": ["url"],
        }
        self.corpsecret = corpsecret
        self.corpid = corpid
        self.agentid = agentid if len(f"{agentid}") else self.corpid
        self.cache_instance = cache_instance
        self.access_token = ""

    def gettoken(self, **kwargs):
        """
        获取 access token

        @see https://developer.work.weixin.qq.com/document/path/91039
        :param kwargs: httpx.request(**kwargs)
        :return: state,access_token
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "GET")
        kwargs.setdefault("url", self.gettoken_url_formatter.format(corpid=self.corpid, corpsecret=self.corpsecret))
        response = httpx.request(**kwargs.to_dict())
        json_addict = HttpxResponseHandler.json_addict(response=response, condition=lambda x: x.is_success)
        if Draft202012Validator(self.gettoken_validate_json_schema).is_valid(json_addict):
            return True, json_addict.get("access_token", None), response
        return None, json_addict, response

    def get_api_domain_ip(self, **kwargs):
        """
        获取企业微信接口IP段

        @see https://developer.work.weixin.qq.com/document/path/92520
        :param kwargs: httpx.request(**kwargs)
        :return: state,ip_list or json
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "GET")
        kwargs.setdefault("url", self.get_api_domain_ip_url_formatter.format(access_token=self.access_token))
        response = httpx.request(**kwargs.to_dict())
        json_addict = HttpxResponseHandler.json_addict(response=response, condition=lambda x: x.is_success)
        if Draft202012Validator(self.get_api_domain_ip_validate_json_schema).is_valid(json_addict):
            return True, json_addict.get("ip_list", []), response
        return None, json_addict, response

    def message_send(self, **kwargs):
        """
        发送应用消息

        @see https://developer.work.weixin.qq.com/document/path/90236
        :param kwargs: httpx.request(**kwargs)
        :return: state,json
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", self.message_send_url_formatter.format(access_token=self.access_token))
        response = httpx.request(**kwargs.to_dict())
        json_addict = HttpxResponseHandler.json_addict(response=response, condition=lambda x: x.is_success)
        if Draft202012Validator(self.message_send_validate_json_schema).is_valid(json_addict):
            return True, json_addict, response
        return None, json_addict, response

    def media_upload(self, f_type="file", **kwargs):
        """
        上传临时素材

        @see https://developer.work.weixin.qq.com/document/path/90253
        :param f_type:
        :param kwargs: httpx.request(**kwargs)
        :return: state,media_id or json
        """
        f_type = f_type if isinstance(f_type, str) and f_type in ["image", "voice", "video", "file"] else "file"
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", self.media_upload_url_formatter.format(access_token=self.access_token, f_type=f_type))
        response = httpx.request(**kwargs.to_dict())
        json_addict = HttpxResponseHandler.json_addict(response=response, condition=lambda x: x.is_success)
        if Draft202012Validator(self.media_upload_validate_json_schema).is_valid(json_addict):
            return True, json_addict.get("media_id", None), response
        return None, json_addict, response

    def media_uploadimg(self, **kwargs):
        """
        上传图片

        @see https://developer.work.weixin.qq.com/document/path/90256
        :param kwargs: httpx.request(**kwargs)
        :return: state,url or json
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", self.media_uploadimg_url_formatter.format(access_token=self.access_token))
        response = httpx.request(**kwargs.to_dict())
        json_addict = HttpxResponseHandler.json_addict(response=response, condition=lambda x: x.is_success)
        if Draft202012Validator(self.media_uploadimg_validate_json_schema).is_valid(json_addict):
            return True, json_addict.get("url", None), response
        return None, json_addict, response

    def refresh_access_token(self, expire: Union[float, int, timedelta] = 7100):
        """
        刷新 access_token

        如果传递了cache_instance 则先取缓存中的 access_token 否则直接获取 access_token
        :param expire: 缓存过期时间
        :return: self
        """
        if not isinstance(self.cache_instance, (diskcache.Cache, redis.Redis, redis.StrictRedis)):
            state, access_token, _ = self.gettoken()
            if state and isinstance(access_token, str) and len(access_token):
                self.access_token = access_token
        else:
            cache_key = f"access_token_{self.agentid}"
            if isinstance(self.cache_instance, diskcache.Cache):
                self.access_token = self.cache_instance.get(cache_key, "")
                state, _, _ = self.get_api_domain_ip()
                if not state:
                    state, access_token, _ = self.gettoken()
                    if state and isinstance(access_token, str) and len(access_token):
                        self.access_token = access_token
                        self.cache_instance.set(key=cache_key, value=self.access_token,
                                                expire=expire or timedelta(seconds=7100).total_seconds())
            if isinstance(self.cache_instance, (redis.Redis, redis.StrictRedis)):
                self.access_token = self.cache_instance.get(cache_key)
                state, _, _ = self.get_api_domain_ip()
                if not state:
                    state, access_token, _ = self.gettoken()
                    if state and isinstance(access_token, str) and len(access_token):
                        self.access_token = access_token
                        self.cache_instance.set(name=cache_key, value=self.access_token,
                                                ex=expire or timedelta(seconds=7100))

        return self
