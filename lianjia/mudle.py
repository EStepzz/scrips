import pymongo
import pprint
class module:
    def __init__(self):
        self.mgdb = '127.0.0.1'
        self.port = 27017
        self.lianjia = 'lianjia'
        self.mgClient = pymongo.MongoClient(host = self.mgdb,port =self.port)

    def insert(self,name,data):
        '''

        :param name:数据集的名字，也就是区的名字
        :param data:
        :return:
        '''
        db = self.mgClient[self.lianjia]
        celection = db[name]
        celection.insert_one(data).inserted_id

    def search(self,name):
        db = self.mgClient[self.lianjia]
        celection = db[name]
        i= 1
        for data in celection.find():
            i = i+1
            pprint.pprint(data)
        print(i)
    def drop(self,dbname):
        self.mgClient[self.lianjia][dbname].drop()
    def close(self):
        self.mgClient.close()

if __name__=='__main__':
    mgdb = module()
    data = {'test':'test'}
    #mgdb.insert('test',data)
    mgdb.search('jinjiang')
    #mgdb.drop('jinjiang')