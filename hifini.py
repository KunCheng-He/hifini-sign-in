# -*- coding: utf-8 -*-
"""
cron: 1 0 0 * * *
new Env('ICC2022');
"""

import json
from notify import send
import requests
import re
import os
import sys
import time
requests.packages.urllib3.disable_warnings()

def start(cookie):
    max_retries = 3
    retries = 0
    msg = ""
    while retries < max_retries:
        try:
            msg += "第{}次执行签到\n".format(str(retries+1))
            sign_in_url = "https://www.hifini.com/sg_sign.htm"
            headers = {
                'Cookie': cookie,
                'authority': 'www.hifini.com',
                'accept': 'text/plain, */*; q=0.01',
                'accept-language': 'zh-CN,zh;q=0.9,und;q=0.8',
                'referer': 'https://www.hifini.com/',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                "sec-fetch-user": '?1',
                "sec-gpc": '1',
                "upgrade-insecure-requests": '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            }
            # post请求携带参数
            payload = {"sign": "01223f9271280a62cacd4f289f9e315c7efd5840246cabf615fd6109da65d189"}

            rsp = requests.post(url=sign_in_url, headers=headers, data=payload, timeout=15, verify=False)
            
            rsp_text = rsp.text
            success = False
            if "今天已经签过啦！" in rsp_text:
                msg += '已经签到过了，不再重复签到!\n'
                success = True
            elif "成功" in rsp_text:
                rsp_json = json.loads(rsp_text)
                msg += rsp_json['message']
                success = True
            elif "503 Service Temporarily" in rsp_text or "502 Bad Gateway" in rsp_text:
                msg += "服务器异常！\n"
            elif "请登录后再签到!" in rsp_text:
                msg += "Cookie没有正确设置！\n"
                success = True
            else:
                msg += "未知异常!\n"
                msg += rsp_text + '\n'
            
            if success:
                print("签到结果: ",msg)
                send("HIFINI 签到结果", msg)
                break  # 成功执行签到，跳出循环
            elif retries >= max_retries:
                print("达到最大重试次数，签到失败。")
                send("HIFINI 签到结果", msg)
                break
            else:
                retries += 1
                print("等待20秒后进行重试...")
                time.sleep(20)
        except Exception as e:
            print("签到失败，失败原因:"+str(e))
            send("HIFINI 签到结果", str(e))
            retries += 1
            if retries >= max_retries:
                print("达到最大重试次数，签到失败。")
                break
            else:
                print("等待20秒后进行重试...")
                time.sleep(20)

if __name__ == "__main__":
    cookie = os.getenv("HIFINI_COOKIE")
    start(cookie)
