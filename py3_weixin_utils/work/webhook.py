#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from typing import Union

import httpx
from addict import Dict
from jsonschema.validators import Draft202012Validator
from py3_http_utils.response import HttpxResponseHandler


class Webhook(object):
    def __init__(self, key: str = "", mentioned_list: Union[tuple, list] = [],
                 mentioned_mobile_list: Union[tuple, list] = []):
        """
        webhook class

        @see https://developer.work.weixin.qq.com/document/path/99110
        :param key: webhook key
        :param mentioned_list: mentioned list
        :param mentioned_mobile_list: mentioned mobile list
        """
        self.send_url_formatter = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}"
        self.upload_media_url_formatter = "https://qyapi.weixin.qq.com/cgi-bin/webhook/upload_media?key={key}&type={f_type}"
        self.send_validate_json_schema = {
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
        self.key = key
        self.mentioned_list = mentioned_list
        self.mentioned_mobile_list = mentioned_mobile_list

    def send_text_formatter(
            self,
            content: str = "",
            mentioned_list: Union[tuple, list] = [],
            mentioned_mobile_list: Union[tuple, list] = []
    ):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E6%9C%AC%E7%B1%BB%E5%9E%8B
        :param content:
        :param mentioned_list:
        :param mentioned_mobile_list:
        :return:
        """
        return Dict({
            "msgtype": "text",
            "text": {
                "content": f"{content}",
                "mentioned_list": self.mentioned_list + mentioned_list,
                "mentioned_mobile_list": self.mentioned_mobile_list + mentioned_mobile_list
            }
        })

    def send_markdown_formatter(self, content: str = ""):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#markdown%E7%B1%BB%E5%9E%8B
        :param content:
        :return:
        """
        return Dict({
            "msgtype": "markdown",
            "markdown": {
                "content": f"{content}"
            }
        })

    def send_image_formatter(self, image_base64: str = ""):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E5%9B%BE%E7%89%87%E7%B1%BB%E5%9E%8B
        :param image_base64:
        :return:
        """
        return Dict({
            "msgtype": "image",
            "image": {
                "base64": f"{image_base64}",
                "md5": "MD5"
            }
        })

    def send_news_formatter(self, articles: Union[tuple, list] = []):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E5%9B%BE%E6%96%87%E7%B1%BB%E5%9E%8B
        :param articles:
        :return:
        """
        return Dict({
            "msgtype": "news",
            "news": {
                "articles": articles
            }
        })

    def send_template_card_formatter(self, template_card: dict = {}):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%A8%A1%E7%89%88%E5%8D%A1%E7%89%87%E7%B1%BB%E5%9E%8B
        :param template_card:
        :return:
        """
        return Dict({
            "msgtype": "template_card",
            "template_card": template_card
        })

    def send_file_formatter(self, media_id: str = ""):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E6%96%87%E4%BB%B6%E7%B1%BB%E5%9E%8B
        :param media_id:
        :return:
        """
        return Dict({
            "msgtype": "file",
            "file": {
                "media_id": media_id
            }
        })

    def send_voice_formatter(self, media_id: str = ""):
        """
        @see https://developer.work.weixin.qq.com/document/path/91770#%E8%AF%AD%E9%9F%B3%E7%B1%BB%E5%9E%8B
        :param media_id:
        :return:
        """
        return Dict({
            "msgtype": "voice",
            "voice": {
                "media_id": media_id
            }
        })

    def send(self, **kwargs):
        """
        send
        @see https://developer.work.weixin.qq.com/document/path/99110
        :param kwargs: httpx.request(**kwargs)
        :return: bool,json
        """
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", self.send_url_formatter.format(key=self.key))
        response = httpx.request(**kwargs.to_dict())
        json_addict = HttpxResponseHandler.json_addict(response=response, condition=lambda x: x.is_success)
        if Draft202012Validator(self.send_validate_json_schema).is_valid(json_addict):
            return True, json_addict, response
        return None, json_addict, response

    def upload_media(self, f_type: str = "file", **kwargs):
        """
        upload media

        @see https://developer.work.weixin.qq.com/document/path/99110
        :param f_type: file type one of ["voice", "file"]
        :param kwargs: httpx.request(**kwargs)
        :return: state, media_id or json
        """
        f_type = "file" if f_type not in ["voice", "file"] else f_type
        kwargs = Dict(kwargs)
        kwargs.setdefault("method", "POST")
        kwargs.setdefault("url", self.upload_media_url_formatter.format(key=self.key, f_type=f_type))
        response = httpx.request(**kwargs.to_dict())
        json_addict = HttpxResponseHandler.json_addict(response=response, condition=lambda x: x.is_success)
        if Draft202012Validator(self.send_validate_json_schema).is_valid(json_addict):
            return True, json_addict.get("media_id", None), response
        return None, json_addict, response
