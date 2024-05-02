# -*- coding: utf-8 -*-
"""
cron: 1 0 0 * * *
new Env('HIFINI');
"""

from notify import send
import requests
import re
import os
import time
requests.packages.urllib3.disable_warnings()

def start(cookie):
    max_retries = 3
    retries = 0
    msg = ""
    while retries < max_retries:
        try:
            msg += "第{}次执行签到\n".format(str(retries+1))

            # 先获取签到的参数
            sign_index = "https://www.hifini.com/"
            headers = {
                'Cookie': cookie,
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
            }

            rsp = requests.get(sign_index, headers=headers)
            rsp_text = rsp.text
            result = re.search(r"var sign = \"([\w\d]+)\";", rsp_text)
            sign = result.group(1)

            # 再请求签到页面
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

            rsp = requests.post(url=sign_in_url, headers=headers, data={"sign": sign}, timeout=15, verify=False)
            
            rsp_text = rsp.text
            success = False
            if "今天已经签过啦！" in rsp_text:
                msg += "签到成功！\n今天已经签到过了，不再重复签到!"
                success = True
            elif "操作存在风险" in rsp_text:
                msg += "签到失败！\n提示“操作存在风险”，不再二次尝试。\n可能cookie失效或配置错误，请重新配置cookie\n若cookie已经正确配置，请联系管理员调试脚本，并停止使用，防止网站对账号进行封控"
                success = True
            elif "成功签到！" in rsp_text:
                result = re.search(r"成功签到！今日排名(\d+)，.*?总奖励(\d+)金币", rsp_text)
                if result:
                    rank = result.group(1)
                    reward = result.group(2)
                    msg += f"签到成功！\n今日排名{rank}，奖励{reward}金币！"
                else:
                    msg += "签到成功！\n但解析失败，今日排名与奖励未知，请更正正则表达式"
                success = True
            elif "503 Service Temporarily" in rsp_text or "502 Bad Gateway" in rsp_text:
                msg += "服务器异常！"
            else:
                msg += "未知异常!\n"
                msg += rsp_text + ''
            
            if success:
                print("签到结果: ", msg)
                send("HIFINI 签到结果", msg)
                break  # 成功执行签到，跳出循环
            elif retries >= max_retries:
                print("达到最大重试次数，签到失败。\n", msg)
                send("HIFINI 签到结果", msg)
                break
            else:
                retries += 1
                print("等待20秒后进行重试...")
                time.sleep(20)
        except Exception as e:
            print("签到失败，失败原因:"+str(e))

            # sign 参数获取失败是因为没有登录，该情况不再重试
            if "group" in str(e):
                print("HIFINI 签到结果", str(e) + "\n请正确配置 cookie !!!")
                break
            
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
