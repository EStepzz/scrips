#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2018/11/22 
# @Author  : liangk
# @Site    :
# @File    : auto_archive_ios.py
# @Software: PyCharm


import requests
from bs4 import BeautifulSoup
import json
import asyncio
import time

class GetIp(object):
    """抓取代理IP"""

    def __init__(self):
        """初始化变量"""
        self.url = 'http://www.xicidaili.com/nn/'
        self.check_url = 'https://www.ip.cn/'
        self.ip_list = []

    @staticmethod
    def get_html(url):
        """请求html页面信息"""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        try:
            request = requests.get(url=url, headers=header)
            request.encoding = 'utf-8'
            html = request.text
            return html
        except Exception as e:
            return ''

    def get_available_ip(self, ip_address, ip_port):
        """检测IP地址是否可用"""
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        ip_url_next = '://' + ip_address + ':' + ip_port
        proxies = {'http': 'http' + ip_url_next, 'https': 'https' + ip_url_next}

        try:
            r = requests.get(self.check_url, headers=header, proxies=proxies, timeout=3)
            html = r.text

            # with requests.get(self.check_url,header=header,proxies=proxies,timeout=3) as response:
            #     await asyncio.sleep(1)
            #     html = response.text

        except:
            print('fail-%s:%s' % (ip_address,ip_port))

        else:
            print('success-%s：%s' % (ip_address,ip_port))
            soup = BeautifulSoup(html, 'lxml')
            div = soup.find(class_='well')
            if div:
                print(div.text)
            ip_info = {'address': ip_address, 'port': ip_port}
            self.ip_list.append(ip_info)


    def main(self):
        """主方法"""
        loop = asyncio.get_event_loop()
        web_html = self.get_html(self.url)
        soup = BeautifulSoup(web_html, 'lxml')
        ip_list = soup.find(id='ip_list').find_all('tr')
        newlist = {}
        for ip_info in ip_list:
            td_list = ip_info.find_all('td')
            if len(td_list) > 0:
                ip_address = td_list[1].text
                ip_port = td_list[2].text
                # 检测IP地址是否有效
                self.get_available_ip(ip_address, ip_port)

                #newlist[ip_address]=ip_port
                # 写入有效文件
        # print(self.ip_list)
        # tasks = [self.get_available_ip(k,v) for k,v in newlist.items()]
        #
        # all_group = asyncio.gather(*tasks)
        # loop.run_until_complete(all_group)
        #loop.close()
        with open('ip.txt', 'w') as file:
             json.dump(self.ip_list, file)

# 程序主入口
if __name__ == '__main__':

    get_ip = GetIp()
    start = time.time()
    get_ip.main()
    end = time.time()
    print(end-start)
