from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import simplejson
import logging
import asyncio
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from mudle import module
import time

class tool:
    def __init__(self):
        self.session = HTMLSession()
        #添加日志
        logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        filehadler = logging.FileHandler('lianjia_out.log',encoding='utf-8')
        self.logger = logging.getLogger('链家')
        self.logger.addHandler(filehadler)
        self.mgdb = module()
        self.hd ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }

    def home_page(self):
        host = 'https://cd.lianjia.com/ershoufang'
        html = self.session.get(host,verify = False)
        self.logger.info('开始爬。。。。')
        return html.html

    def areas(self,html):
        self.logger.info('记录地区')
        areas = html.find('html body div div.m-filter div.position dl dd div div a')
        #self.logger.info(areas)
        with open('area.txt','w+') as f:
            for area in areas:
                #self.logger.info('area')
                f.write( area.text+','+''.join(area.absolute_links)+'\n')


    def zone_first_page(self,url):
        proxies = {'http': 'http' + '121.237.149.141:3000', 'https': 'https' + '121.237.149.141:3000'}
        #html = requests.get(url,headers = self.hd,proxies=proxies,verify = False).text
        html = requests.get(url, verify=False).text
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        return soup

    def zone_num(self,soup):
        '''
        :这个区的总页数
        :param soup: zone_first_page 返回的soup 对象
        :return:
        '''
        page_num = simplejson.loads(soup.find('div', {'class': 'page-box house-lst-page-box'})['page-data'])['totalPage']
        return int(page_num)

    async    def house_data(self,link,name):
        '''
        :单页中的房源信息
        :param link: 构造页面连接
        ：param name: 区的名字，以创建mongoDB 的数据集
        :return:
        '''
        self.logger.info(link)
        #proxies = {'http': 'http' + '121.237.149.141:3000', 'https': 'https' + '121.237.149.141:3000'}
        try:
            with requests.get(link,headers = self.hd,verify = False) as resp:
                html = resp.text
                await asyncio.sleep(1)
        except:
            self.logger.info(link +': '+'请求异常')

        #html = requests.get(link, verify=False).text
        self.logger.info(name+':'+'写db啦')
        soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
        all = soup.select('.clear.LOGCLICKDATA') #select 结果是list 同 find_all() find()是唯一的值可以直接取属性
        for item in all:
            host_detail = item.find('a',{'class' : 'noresultRecommend img LOGCLICKDATA'})['href']
            posiont = item.find('div','positionInfo').text #地点
            houseInfo = item.find('div','houseInfo').text # 房屋信息
            totalPrice = item.find('div', 'totalPrice').text # 总价 w
            unitPrice = item.find('div','unitPrice').text # 单价 w
            #self.logger.info(host_detail+': '+posiont+': '+houseInfo+': '+totalPrice+': '+unitPrice)
            id = host_detail.split('/')[-1].split('.')[0]
            id ={'host_detail':host_detail,
                 'posiont': posiont,
                 'houseInfo': houseInfo,
                 'totalPrice':totalPrice,
                 'unitPrice': unitPrice}

            self.mgdb.insert(name=name, data=id)
        time.sleep(5)

if __name__=='__main__':
    T = tool()
    home_page = T.home_page()
    T.areas(home_page)
    loop = asyncio.get_event_loop()
    link_list = []
    with open('area.txt','r') as f:
        for line in f.readlines():
            #获取各个区的链接地址
            link = line.split(',')[1].split('\n')[0]

            zone_name = link.split('/')[-2]
            sp = T.zone_first_page(link)
            #print(zone_name)
            for i in range(1,T.zone_num(sp)):
                #翻页链接
                node_link = link+'pg'+str(i)
                link_list.append(node_link)
                # T.house_data(node_link,zone_name)
                # T.mgdb.close()
            #使用异步处理
            tasks = [T.house_data(link, zone_name) for link in link_list]
            task = asyncio.gather(*tasks)
            loop.run_until_complete(task)