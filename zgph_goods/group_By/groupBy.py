'''
@author: qinwang
@time:2020-5-5
@purpose: 通过接口返回数据比价和校验
'''
import logging
import requests
import simplejson

class groupby:
    def __init__(self):
        pass

    def compare_price(self,resp):
        '''
        :goods_details 返回结果: 单个商品
        :团购价和单买价是否正常
        :return:
        '''
        resp = simplejson.loads(resp).decode('utf-8')
        originalPrice = resp['originalPrice']
        sellingPrice = resp['selling']
        if sellingPrice >= originalPrice:
            logging.ERROR(resp['goodsName']+" "+resp['goodsId'])

    def goods_details(self,host,item):
        '''
        :uri: /goodsAppGoodsController/findById
        :method: post
        :body:{"goodsId":"3304865831929909248","goodsType":2,"peroidId":"af632ad2253549e79f524fed84a9484e"}
        :查看商品详情，是否报错
        :return:
        '''
        logging.info(item)
        uri = '/goodsAppGoodsController/findById'
        url = host+ uri
        boday ={
            'goodsid' : item['goodsId'],
            'goodsType' : 2,
            'peroidId': item['peroidId']
        }
        header = {
            'Accept-Encoding': 'identity',
            'User-Agent': 'okhttp/3.11.0'
        }
        response = requests.post(url,body = boday,headers = header,verify = False)
        if response.status_code !=200:
            logging.ERROR(item['goodsId'],item['goodsName'])
        else:
            self.compare_price(response.content)

    def list_price(self, item):
        '''
        :列表中购买价和划线价 比较
        :return:
        '''
        group_price = item['groupPrice']
        originalPrice = item['originalPrice']
        if group_price >originalPrice:
            logging.info(item['goodsName'],item['originalGoodsId'])


    def get_all_list(self):
        '''
        :获取团购列表所有商品 goodsid
        :return:
        '''

        pass
