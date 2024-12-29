# -*- coding: utf-8 -*-
"""
cron: 1 0 0 * * *
new Env('HIFINI');
"""

from notify import send
import requests
import re
import os
requests.packages.urllib3.disable_warnings()

def start(cookie):
    msg = ""
    try:
        # 先获取签到的参数
        sign_index = "https://www.hifini.com/"
        headers = {
            'Cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

        rsp = requests.get(sign_index, headers=headers)
        rsp_text = rsp.text
        result = re.search(r"var sign = \"([\w\d]+)\";", rsp_text)
        sign = result.group(1)

        # 发送 POST 请求签到
        rsp = requests.post(
            url="https://www.hifini.com/sg_sign.htm",
            headers={
                'Cookie': cookie,
                'x-requested-with': 'XMLHttpRequest'
            },
            data={"sign": sign}, timeout=15, verify=False
        )
        rsp_text = rsp.text

        # 通知
        msg += rsp_text
        send("HIFINI 签到结果", msg)
    except Exception as e:
        print("签到失败，失败原因:"+str(e))
        send("HIFINI 签到结果", str(e))


if __name__ == "__main__":
    cookie = os.getenv("HIFINI_COOKIE")
    start(cookie)
