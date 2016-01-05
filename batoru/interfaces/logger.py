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
        self.elasticsearch = elasticsearch.Elasticsearch()
        self.index = index
        self.doc_type = doc_type

    def write(self, key, value):
        self.elasticsearch.index(index=self.index, doc_type=self.doc_type, id=str(key), body=value)
