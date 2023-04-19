import salt.ext.tornado.gen
from salt.ext.tornado.concurrent import Future
         
@salt.ext.tornado.gen.coroutine
def torn(self):
    return "HEY"
