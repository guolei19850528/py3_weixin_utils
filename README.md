# py3_weixin_utils
### py3_weixin_utils
#### 企业微信
##### webhook [document](https://developer.work.weixin.qq.com/document/path/99110)
```python
from py3_weixin_utils.work import webhook, server

webhook_instance = webhook.Webhook(
    key="your key"
)
state, _, _ = webhook_instance.send(json=webhook_instance.send_text_formatter(content="test"))
if state:
    print("send text success")
state, media_id = webhook_instance.upload_media(files={
    "file": ("README.md", open("README.md", "rb")),
})
if state and isinstance(media_id, str) and len(media_id):
    print("upload media success")
    state, _, _ = webhook_instance.send(json=webhook_instance.send_file_formatter(media_id=media_id))
    if state:
        print("send file success")
```
##### server [document](https://developer.work.weixin.qq.com/document/path/90664)
```python
from py3_weixin_utils.work import webhook, server

agentid = ""
corpid = ""
corpsecret = ""
server_instance = server.Server(agentid=agentid, corpid=corpid, corpsecret=corpsecret,
                                cache_instance="your cache instance")
state, ip_list, _ = server_instance.refresh_access_token().get_api_domain_ip()
state, media_id, _ = server_instance.refresh_access_token().media_upload(files={
    "file": ("README.md", open("README.md", "rb"))
})
state, url, _ = server_instance.refresh_access_token().media_uploadimg(files={
    "file": ("README.png", open("README.png", "rb"))
})
state, _, _ = server_instance.refresh_access_token().message_send(json={})
```