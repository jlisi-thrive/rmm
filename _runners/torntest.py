from salt.ext.tornado.httpclient import AsyncHTTPClient
from salt.ext.tornado import gen
    
@gen.coroutine
def torn():
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch("https://jsonplaceholder.typicode.com/posts/1")
