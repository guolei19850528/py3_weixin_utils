# py3_weixin_utils
### py3_weixin_utils
#### 企业微信
##### webhook [document](https://developer.work.weixin.qq.com/document/path/99110)
```python
from py3_weixin_utils.work import webhook

webhook_instance = webhook.Webhook(
    key="your key"
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
```