import logging
import redis
import elasticsearch


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
        Logger.__init__(self)
        self.r = redis.StrictRedis(host='localhost', port=6379, db=0)

    def write(self, key, value):
        self.r.lpush(key, value)

    def load_sequence(self, key):
        self.r.setnx(key, 0)
        self.r.incr(key, 1)
        value = self.r.get(key)
        return value


class ElasticSearchLogger(Logger):
    def __init__(self, index, doc_type):
        Logger.__init__(self)
        self.elasticsearch = elasticsearch.Elasticsearch()
        self.index = index
        self.doc_type = doc_type

    def write(self, key, value):
        self.elasticsearch.index(index=self.index, doc_type=self.doc_type, id=str(key), body=value)
