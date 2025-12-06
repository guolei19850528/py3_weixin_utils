import os
import unittest

import diskcache
import httpx
import requests

from py3_weixin_utils.work import webhook, server

diskcache_default_instance = diskcache.Cache(
    directory=os.path.join(os.getcwd(), "runtime", "cache", "diskcache", "default"))


class MyTestCase(unittest.TestCase):
    def test_work_webhook(self):
        webhook_instance = webhook.Webhook(
            key="366095be-225c-4c92-9369-c9d9bc5cc1c5"
        )
        state, _ = webhook_instance.send(json=webhook_instance.send_text_formatter(content="test"))
        if state:
            print("send text success")
        state, media_id = webhook_instance.upload_media(files={
            "file": ("README.md", open("README.md", "rb")),
        })
        if state and isinstance(media_id, str) and len(media_id):
            print("upload media success")
            state, _ = webhook_instance.send(json=webhook_instance.send_file_formatter(media_id=media_id))
            if state:
                print("send file success")
        self.assertEqual(True, True)  # add assertion here

    def test_work_server(self):
        agentid = "1000035"
        corpid = "ww5f2bb01bebafe097"
        corpsecret = "caVcNxS9qP8utsCkPaG7NH0I-j1vr9EMRi0WpsvkzVU"
        server_instance = server.Server(agentid=agentid, corpid=corpid, corpsecret=corpsecret,
                                        cache_instance=diskcache_default_instance)
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
