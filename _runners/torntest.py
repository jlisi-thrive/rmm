from salt.utils.asynchronous import current_ioloop

def torn(self):
    current_ioloop()
    return "HEY"

# import salt.ext.tornado.gen
# from salt.ext.tornado.concurrent import Future
         
# @salt.ext.tornado.gen.coroutine
# def torn(self):
#     return "HEY"
