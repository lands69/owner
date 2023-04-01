import requests,json
from lxml import etree

cookie = ''
corpid = ""
agentid = ""
secret = ""


def get_formhash():
    url = "https://gkdworld.cf/plugin.php?id=k_misign:sign"
    headers = {
        "referer": "https://gkdworld.cf/",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "cookie": cookie
        }
    resp = requests.get(url,headers=headers)
    s = etree.HTML(resp.text)
    href = s.xpath("//a[@class='logout']/@href")
    formhash = ''.join(href).split('=')[-1]
    return formhash

def main(*args):
    url = 'https://gkdworld.cf/plugin.php'
    headers = {
        'authority': 'gkdworld.cf',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44',
        'Referer': 'https://gkdworld.xyz/plugin.php?id=k_misign:sign',
        'cookie': cookie
    }
    formhash = get_formhash()
    params = {
        "id": "k_misign:sign",
        "operation":"qiandao",
        "formhash": formhash,
        "format": "empty"
        }
    content = requests.get(url,headers=headers,params=params).text
    print(content)
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
    return 


if __name__ == '__main__':
    main()
