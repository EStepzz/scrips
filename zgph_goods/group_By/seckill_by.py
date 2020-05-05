import logging
class seckillBy():
    def __init__(self):
        logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        filehadler = logging.FileHandler('seckill.log',encoding='utf-8')
        self.logger = logging.getLogger('seckill')
        self.logger.addHandler(filehadler)

    def goods_detail(self):
        pass

    def seckill_price(self,item):
        '''
        :抢购价&划线价
        :return:
        '''

        seckillPrice = item['seckillPrice']
        originalPrice = item['originalPrice']
        if seckillPrice> originalPrice:
            self.logger.error(item['goodsId']+': '+item['goodsName'])
        else:
            self.logger.info(item['goodsName']+':  '+'没问题')

    def goods_detail(self):
        '''
        查询商品详情不报错
        :return:
        '''
        pass
