import salt.ext.tornado.gen
 
@salt.ext.tornado.gen.coroutine
def torn():
    http_client = AsyncHTTPClient()
    response = yield http_client.fetch("https://jsonplaceholder.typicode.com/posts/1")
    return "Maybe"
