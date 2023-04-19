import salt.ext.tornado.gen
from salt.ext.tornado.concurrent import Future
         
@salt.ext.tornado.gen.coroutine
def torn():
    future = Future()
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch("https://jsonplaceholder.typicode.com/posts/1")
    raise salt.ext.tornado.gen.Return(response)
