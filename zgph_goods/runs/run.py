from configparser import ConfigParser
import requests
import simplejson
from group_By.groupBy import groupby
from group_By.seckill_by import seckillBy
def urls(name):
    config = ConfigParser()
    config.read('F:\\爬虫\\zgph_goods\\.env',encoding='utf-8')
    host = config['host']['host']
    uri = config['sc'][name]
    return host+uri
def sc_homepage():
    url = urls('sc_homepage')
    header ={
        'token':'b0946f49-d8c3-46ba-9f28-7e593958c578',
        "Content-Type": "application/json;Charset=UTF-8"
    }
    data = {
        "goodsType": 'null',
        "page": 1,
        "pageSize": 10,
        "shopId": "null"
    }
    content = requests.post(url,json= data,headers = header,verify = False)
    print(content)
    content = simplejson.loads(content.content.decode('utf-8'))
    print(content['data'])
    for i in range(len(content['data'])):
        groupby().goods_details(content['data'])

def sc_groupby():
    pass

def sc_seckill():
    url = urls('sc_seckill')
    header = {
        'token': 'b0946f49-d8c3-46ba-9f28-7e593958c578',
        "Content-Type": "application/json;Charset=UTF-8"
    }
    data = {
        "platformId": 0,
        "type": 1
    }
    content = requests.post(url, json=data, headers=header, verify=False)
    content = simplejson.loads(content.content.decode('utf-8'))
    #print(content['data'])
    json = content['data']['list']
    for i in range(len(json)):
        seckillBy().seckill_price(json[i])




if __name__ == '__main__':
    #sc_homepage()
    sc_seckill()