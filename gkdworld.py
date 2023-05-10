import requests,json,hashlib
from lxml import etree

corpid = ""
agentid = ""
secret = ""

usr = ""
pwd = ""

session = requests.session()


def main(*args):
    ## 加密密码
    md = hashlib.md5()
    md.update(pwd.encode('utf-8'))
    password = md.hexdigest()

    ## 获取登陆参数
    url = "https://gkdworld.cf/member.php?mod=logging&action=login"
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
        }
    resp = session.get(url,headers=headers)
    s = etree.HTML(resp.text)
    login_url = s.xpath("//form[@method='post']/@action")[0]
    login_formhash = s.xpath("//input[@name='formhash']/@value")[0]
    cookietime = s.xpath("//input[@name='cookietime']/@value")[0]

    ## 登陆
    login_urls = f'https://gkdworld.cf/{str(login_url)}&inajax=1'
    login_headers = {
        "Origin":"https://gkdworld.cf",
        "Referer":"https://gkdworld.cf/member.php?mod=logging&action=login",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
        }
    data = {
        "formhash": str(login_formhash),
        "referer": "https://gkdworld.cf/./",
        "username": usr,
        "password": password,
        "questionid": "0",
        "answer": "",
        "cookietime": str(cookietime)
        }
    res = session.post(login_urls,headers=login_headers,data=data)
    # print(res.text)

    ## 签到formhash
    check_formhash_url = "https://gkdworld.cf/plugin.php?id=k_misign:sign"
    resp = session.get(check_formhash_url,headers=headers)
    s = etree.HTML(resp.text)
    href = s.xpath("//a[@class='logout']/@href")
    checkin_formhash = ''.join(href).split('=')[-1]
    # print(checkin_formhash)

    ## 签到
    checkin_url = 'https://gkdworld.cf/plugin.php'
    checkin_headers = {
        'authority': 'gkdworld.cf',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44',
        'Referer': check_formhash_url,
    }
    params = {
        "id": "k_misign:sign",
        "operation":"qiandao",
        "formhash": checkin_formhash,
        "format": "empty"
        }
    content = session.get(checkin_url,headers=checkin_headers,params=params).text
    print(content)
 
    ## 发送结果
    result = requests.get(f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corpid}&corpsecret={secret}")
    token = result.json().get("access_token",False)
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
    
