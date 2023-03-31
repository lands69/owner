# 面码acg每日签到
import requests,json

# 企业微信推送
corpid = ""
agentid = ""
secret = ""

cookie = ""

url = "https://www.acgcbk.vip/api/v1/actions/daily_sign"
headers = {
    "referer": "https://www.acgcbk.vip/me/credits",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "cookie": cookie
    }
data = {"_wpnonce": "45c0cf50c7"}
content = requests.post(url,headers=headers,data=data).json()['message']

s = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}")
token = s.json().get("access_token",False)
data = {
    "touser": "@all",
    "agentid": agentid,

    "msgtype": "text",
    "text": {
       "content": "面码："+content,

    },
}
requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}", data=json.dumps(data))

print(content)
