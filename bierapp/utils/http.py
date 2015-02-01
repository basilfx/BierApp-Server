from django.http import HttpResponse

from bierapp.utils import json

class HttpJSONResponse(HttpResponse):
    """
    An HttpResponse of JSON content
    
    Unlike a Django HttpResponse, this class can accept any JSON-serializable data type as content:
    dictionaries, lists, strings, etc.
    
    Example::
    
        def some_view(request):
            return HttpJSONResponse({'foo': 'bar'})
    """
    def __init__(self, content=None, content_type="application/json"):
        super(HttpJSONResponse, self).__init__(content=json.dumps(content), content_type=content_type)