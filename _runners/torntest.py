from salt.ext.tornado.httpclient import AsyncHTTPClient
from salt.ext.tornado import gen

@gen.coroutine
def torn():
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch("https://jsonplaceholder.typicode.com/posts/1")
    # In Python versions prior to 3.3, returning a value from
    # a generator is not allowed and you must use
    #   raise gen.Return(response.body)
    # instead.
    return response.body
