import logging
import redis
import elasticsearch

import ruamel.yaml as yaml


class Logger:
    def __init__(self):
        self.logLevel = 1
        self.logFile = 'info.log'

    def set_log_file(self, filename):
        self.logFile = filename

    def write(self, key, value):
        logging.basicConfig(filename=self.logFile)
        logging.info(key + ": " + value)


class RedisLogger(Logger):
    def __init__(self):
        with open("config/config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.Loader)

        Logger.__init__(self)
        self.r = redis.StrictRedis(host=cfg['redis']['host'], port=str(cfg['redis']['port']), db=0)

    def write(self, key, value):
        self.r.set(key, value.encode('utf-8'))

    def load(self, key):
        value = self.r.get(key)
        if value is not None:
            return value.decode('utf-8')

        return value

    def load_sequence(self, key):
        self.r.setnx(key, 0)
        self.r.incr(key, 1)
        return self.r.get(key).decode('utf-8')


class ElasticSearchLogger(Logger):
    def __init__(self, index, doc_type):
        Logger.__init__(self)

        with open("config/config.yml", 'r') as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.Loader)

        elasticsearch_host = cfg['elasticsearch']['host']
        elasticsearch_port = cfg['elasticsearch']['port']

        self.elasticsearch = elasticsearch.Elasticsearch([{'host': elasticsearch_host, 'port': elasticsearch_port}])
        self.index = index
        self.doc_type = doc_type

    def write(self, key, value):
        self.elasticsearch.index(index=self.index, doc_type=self.doc_type, id=str(key), body=value)
