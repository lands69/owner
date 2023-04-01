#coding=utf-8
from sqlite3 import connect
import requests,json,time
from bs4 import BeautifulSoup
from lxml import etree

cookie = ""
corpid = ""
agentid = ""
secret = ""


def sigin():
    url = "https://bbs.kafan.cn/"
    headers = {
        "Cookie": cookie,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54"
    }

    res = requests.get(url,headers=headers).text
    s = etree.HTML(res)
    x = s.xpath('//html/body/div[3]/div/div[2]/a[5]/@href')[0].split('=')[-1]
    return x

def checkin(*args):
    url = f'https://bbs.kafan.cn/plugin.php?id=dsu_amupper&ppersubmit=true&formhash={sigin()}'
    headers = {
        "Cookie": cookie,
        "Referer": "https://bbs.kafan.cn/forum.php",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.54"
    }
    re = requests.get(url,headers=headers)
    time.sleep(5)
    soup = BeautifulSoup(re.text,'lxml')
    msgtext = soup.find_all('div',id='messagetext')
    for i in msgtext:
        msg = '卡饭签到：'+i.get_text()
        print(msg)
    return msg


def sendmsg(content):

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

if __name__=='__main__':
    sendmsg(checkin())
