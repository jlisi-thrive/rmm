import salt.ext.tornado.gen

def torn():
    orig_loop = salt.ext.tornado.ioloop.IOLoop.current()
    return "Jey"
