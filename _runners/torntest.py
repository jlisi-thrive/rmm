from salt.ext.tornado.httpclient import AsyncHTTPClient

async def torn():
    http_client = AsyncHTTPClient()
    response = await http_client.fetch("https://jsonplaceholder.typicode.com/posts/1")
    return response.body
