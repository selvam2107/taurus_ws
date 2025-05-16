import redis
red= redis.Redis(host= '192.168.5.8',port= '6379')
red.set('test','redy')