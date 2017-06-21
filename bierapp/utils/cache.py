from django.core.cache.backends.locmem import LocMemCache
from django.utils.deprecation import MiddlewareMixin

from threading import currentThread


_request_cache = {}
_installed_middleware = False


def get_request_cache():
    return _request_cache[currentThread()]


# LocMemCache is a threadsafe local memory cache
class RequestCache(LocMemCache):
    def __init__(self):
        name = "locmemcache@%i" % hash(currentThread())
        params = dict()
        super(RequestCache, self).__init__(name, params)


class RequestCacheMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        super(RequestCacheMiddleware, self).__init__(get_response)

        global _installed_middleware
        _installed_middleware = True

    def process_request(self, request):
        cache = _request_cache.get(currentThread()) or RequestCache()
        _request_cache[currentThread()] = cache

        cache.clear()
