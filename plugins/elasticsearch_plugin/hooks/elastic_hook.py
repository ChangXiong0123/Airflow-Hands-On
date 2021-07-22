from airflow.hooks.base import BaseHook
from elasticsearch import Elasticsearch


class ElasticHook(BaseHook): ##inherit from BaseHook

    def __init__(self,conn_id ='elasticsearch_default', *args, **kwargs):
        super().__init__(*args, **kwargs) # this is to initialize the attributes of BaseHook
        conn = self.get_connection(conn_id) #this is to fetch from hook
        #once the connection from UI to airflow is created, you have to fetch it from the hook
        
        ##########to get the attributes of that connection ###################
        conn_config = {}
        hosts = [] #elasticsearch can have multiple hosts

        #########check if the required attributes for elasticsearch###########
        if conn.host:
            hosts = conn.host.split(',') # if there is multiple hosts, we separate it with comma and make it a list
        if conn.port:
            conn_config['port'] = int(conn.port) #make sure the port is number instead of string
        if conn.login:
            conn_config['http_auth'] = (conn.login,conn.password)

        
        self.es = Elasticsearch(hosts, **conn_config) #create the Elasticsearch object
        self.index = conn.schema #As elasticsearch specify schema in indexs
        # we can specify index if we want
        # so in the attribution schema from the UI, you will specify the index where you want to store the data

#####create some methods that can interact with elasticsearch
    def info(self): 
        """get information from our elasticsearch object"""
        return self.es.info()


    def set_index(self,index):
        """define a index """
        self.index = index

    def add_doc(self, index, doc_type, doc):
        """add documents and data in the index"""
        self.set_index(index)
        res = self.es.index(index = index, doc_type = doc_type, body = doc)
        #we call the method index from elasticsearch object
        return res
