# -*- coding: utf8 -*-
import base64
import json

import requests
from lxml import etree

cookies = {}
QQ = []
myself_qq = 


def set_cookie(cookie):
    global cookies
    with open('cookie.ini', 'w') as f:
        f.write(cookie)
    cookies_str = {}
    cookie = cookie.split('; ')
    for i in cookie:
        i = i.split('=')
        cookies_str[i[0]] = i[1]
    cookies['p_uin'] = cookies_str['p_uin']
    if 'qq_locale_id' in cookies_str:
        cookies['qq_locale_id'] = cookies_str['qq_locale_id']
    else:
        cookies['qq_locale_id'] = '2052'
    cookies['uin'] = cookies_str['p_uin']
    cookies['pgv_pvid'] = cookies_str['pgv_pvid']
    cookies['ts_uid'] = cookies_str['ts_uid']
    if 'domainId' in cookies_str:
        cookies['domainId'] = cookies_str['domainId']
    else:
        cookies['domainId'] = '338'
    if 'pgv_pvi' in cookies_str:
        cookies['pgv_pvi'] = cookies_str['pgv_pvi']
    else:
        cookies['pgv_pvi'] = '112969728'
    if 'pgv_si' in cookies_str:
        cookies['pgv_si'] = cookies_str['pgv_si']
    else:
        cookies['pgv_si'] = 's6262475776'
    cookies['skey'] = cookies_str['skey']
    cookies['p_skey'] = cookies_str['p_skey']
    cookies['a2'] = cookies_str['a2']
    cookies['ts_last'] = cookies_str['ts_last']


def read_QQ():
    try:
        with open('qq.ini') as f:
            for line in f:
                QQ.append(line.replace('\n', ''))
    except:
        add_QQ()


def add_QQ():
    print('检测到第一次使用，请手动输入批量抽卡的QQ号（QQ号按行分隔，输入空行结束）')
    count = 0
    with open('qq.ini', 'w') as f:
        while True:
            count += 1
            qq = input(str(count) + ' :')
            if qq == '':
                print('添加成功,总共添加', count, '个账号')
                break
            QQ.append(qq)
            f.write(qq + '\n')


def get_all_card():
    user_agent = 'Mozilla/5.0 (Linux; Android 8.0.0; FLA-AL20 Build/HUAWEIFLA-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 V1_AND_SQ_8.2.8_1346_YYB_D QQ/8.2.8.4440 NetType/4G WebP/0.3.0 Pixel/1080 StatusBarHeight/73 SimpleUISwitch/0 QQTheme/1000'
    host = 'ti.qq.com'
    headers = {
        'User-Agent': user_agent,
        'host': host
    }
    url = 'https://ti.qq.com/interactive_logo/word'
    params = {
        'target_uin': '1226381077',
        '_wv': '67108865',
        '_nav_txtclr': 'FFFFFF',
        '_wvSb': '0'
    }
    page = requests.get(url, params=params, headers=headers, cookies=cookies)
    print(page.text)


def chouka(myself_qq):
    user_agent = 'Mozilla/5.0 (Linux; Android 8.0.0; FLA-AL20 Build/HUAWEIFLA-AL20; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 V1_AND_SQ_8.2.8_1346_YYB_D QQ/8.2.8.4440 NetType/4G WebP/0.3.0 Pixel/1080 StatusBarHeight/73 SimpleUISwitch/0 QQTheme/1000'
    host = 'ti.qq.com'
    for qq in QQ:
        print(qq)
        url_get = 'https://ti.qq.com/hybrid-h5/interactive_logo/two'
        params = {
            'target_uin': qq,
            '_wv': '67108867',
            '_nav_txtclr': '000000',
            '_wvSb': '0'
        }
        headers = {
            'User-Agent': user_agent,
            'host': host
        }
        r = requests.get(url_get, params=params, headers=headers, cookies=cookies)
        html = etree.HTML(r.text)
        result = html.xpath('//*[@id="app"]/div[1]/div[3]/div[1]/span/span/text()')
        if len(result) != 0:
            print(result[0], '个好友互动标识')
            for count in range(int(result[0])):
                c_name = html.xpath('//*[@id="app"]/div[1]/div[3]/div[' + str(count + 2) + ']/div[2]/text()')
                c_days = html.xpath(
                    '//*[@id="app"]/div[1]/div[3]/div[' + str(count + 2) + ']/div[3]/span[1]/text()')
                if len(c_days) != 0:
                    print(c_name[0], c_days[0], '天')
                else:
                    print(c_name[0])
        url_post = 'https://ti.qq.com/proxy/domain/oidb.tim.qq.com/v3/oidbinterface/oidb_0xdd0_0'
        params = {
            'sdkappid': '39998',
            'actype': '2',
            'bkn': '125442749'
        }
        headers = {
            'User-Agent': user_agent,
            'host': host,
            'Content-Type': 'application/json'
        }
        while True:
            data = {
                'uin': myself_qq,
                'frd_uin': int(qq)
            }
            r = requests.post(url_post, headers=headers, params=params, data=json.dumps(data), cookies=cookies)
            r = json.loads(r.text)
            if r['ActionStatus'] == 'OK':
                if r['card_url'] == '':
                    print(' 没抽中')
                else:
                    print(' 抽到卡片，卡片信息：')
                    print("   卡片ID：", base64.b64decode(r['card_id']).decode())
                    print("   卡片文字：", base64.b64decode(r['card_word']).decode())
                    print("   卡片图片地址：", base64.b64decode(r['card_url']).decode())
                    print("   卡片描述：", base64.b64decode(r['rpt_wording'][0]).decode())
            elif r['ActionStatus'] == 'FAIL':
                if r['ErrorCode'] == 10005:
                    print(' 今日次数已用完')
                    break
                elif r['ErrorCode'] == 151:
                    print(' 登录过期')
                    return 151
                elif r['ErrorCode'] == 10006:
                    print(' 该QQ号不是你的好友')
                    break
                elif r['ErrorCode'] == 304:
                    print(' 请检查你的myself_qq，该数据应为int类型数字')
                    return 304
                print(' ErrorInfo: ', r['ErrorInfo'], ' ErrorCode: ', r['ErrorCode'])
            else:
                print(r)
    return 0


if __name__ == '__main__':
    read_QQ()
    try:
        with open('cookie.ini') as f:
            cookie = f.read()
    except:
        cookie = input('请输入cookie：')
    set_cookie(cookie)
    status = chouka(myself_qq)
    while status != 0:
        if status == 151:
            cookie = input('请输入cookie：')
            set_cookie(cookie)
            status = chouka(myself_qq)
        if status == 304:
            break