import salt.ext.tornado.gen
from salt.ext.tornado.concurrent import Future

class Any(Future):
    """
    Future that wraps other futures to "block" until one is done
    """

    def __init__(self, futures):
        super().__init__()
        for future in futures:
            future.add_done_callback(self.done_callback)

    def done_callback(self, future):
        # Any is completed once one is done, we don't set for the rest
        if not self.done():
            self.set_result(future)
         
@salt.ext.tornado.gen.coroutine
def torn():
    http_client = AsyncHTTPClient()
    response = yield Any(http_client.fetch("https://jsonplaceholder.typicode.com/posts/1"))
    return "Maybe"
