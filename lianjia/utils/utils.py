from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import logging
import time


class Utils:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('https://cd.lianjia.com/ershoufang/')
        #添加日志
        logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        filehadler = logging.FileHandler('lianjia_out.log',encoding='utf-8')
        self.logger = logging.getLogger('下一页')
        self.logger.addHandler(filehadler)

    def next_page(self):
        with open('area.txt','r+',encoding='utf-8') as f :
            zone_names = f.readlines()
            for zone in zone_names:
                zone_url = zone.split(',')[1]
                zone_url = zone_url.split('\n')[0]
                # zone_url = lambda zone: zone.split(',')[1]+'1'
                for i in range(1, 100):
                    page_num = 'pg'+str(i)
                    next_url = zone_url+page_num
                    print(next_url)
                    try:
                        self.new_window(next_url)
                    except:
                        self.logger.info('获取下一页地址内容失败了')
                        continue


    def new_window(self,url):
        data_handle = self.driver.window_handles[-1]
        js = 'window.open({});'.format('"' + url + '"')
        self.driver.execute_script(js)
        time.sleep(15)
        handles = self.driver.window_handles
        self.logger.info('开始 创建新页面')
        # self.driver.switch_to_window(handles[-1])  # 切换到新创建的窗口
        #self.data()
        self.driver.switch_to_window(handles[-1])
        self.data()





    def area(self):
        '''
        :查找区域连接，注意find_elements 和 find_element 的区别
        :return:
        '''
        area = self.driver.find_elements_by_xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a')
        with open('area.txt','w+') as f:
            for item in area:
                print(item.text,item.get_attribute('href'))

                # self.data()
                # self.next_page()
                # time.sleep(1)

        self.driver.close()
        return

    def data(self):
        items = self.driver.find_elements_by_xpath('//*[@id="content"]/div[1]/ul/li')
        for item in items:
            try:
                flood = item.find_element_by_class_name('positionInfo').text
                address = item.find_element_by_class_name('address').text
                follow = item.find_element_by_class_name('followInfo').text
                tag = item.find_element_by_class_name('tag').text
                price = item.find_element_by_class_name('priceInfo').text
                self.logger.info(flood+address+follow+tag+price)

            except:
                continue

    def test(self):
        url = 'https://cd.lianjia.com/ershoufang/jinjiang/pg1'
        js = 'window.open({});'.format('"'+url+'"')
        self.driver.execute_script(js)
        handles = self.driver.window_handles
        self.logger.info('开始 创建新页面')
        # self.driver.close()
        self.driver.switch_to_window(handles[-1])  # 切换到新创建的窗口
if __name__=='__main__':
    #Utils().next_page()
    Utils().next_page()