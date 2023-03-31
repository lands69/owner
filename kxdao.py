import requests,json
from lxml import etree

cookie = ''
corpid = ""
agentid = ""
secret = ""

url = "https://www.kxdao.org"
sigin_url = "https://www.kxdao.org/plugin.php"

headers = {
    "referer": url,
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "cookie": cookie
    }
formhash_resp = requests.get(url,headers=headers).text
s = etree.HTML(formhash_resp)
formhash = s.xpath('//input[@name="formhash"]/@value')[0]
# print(formhash)
params = {
    "id": "dsu_amupper",
    "ppersubmit": "true",
    "formhash": formhash,
    "infloat": "yes",
    "handlekey": "dsu_amupper",
    "inajax": "1",
    "ajaxtarget": "fwin_content_dsu_amupper"
    }

resp = requests.get(sigin_url,headers=headers,params=params).text
x = etree.XML(resp.encode('utf-8'))
content = x.xpath('/root/text()')

s = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}")
token = s.json().get("access_token",False)
data = {
    "touser": "@all",
    "agentid": agentid,

    "msgtype": "text",
    "text": {
        "content": content,

    },
}
requests.post(url=f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}", data=json.dumps(data))

print(content)
