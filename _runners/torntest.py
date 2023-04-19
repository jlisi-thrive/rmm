from salt.utils.asynchronous import current_ioloop
import salt.ext.tornado.ioloop

def torn():
    orig_loop = salt.ext.tornado.ioloop.IOLoop.current()
    return orig_loop

# import salt.ext.tornado.gen
# from salt.ext.tornado.concurrent import Future
         
# @salt.ext.tornado.gen.coroutine
# def torn(self):
#     return "HEY"
