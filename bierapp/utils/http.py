from django.http import StreamingHttpResponse
from django.core.serializers.json import DjangoJSONEncoder

import json


class StreamingJsonResponse(StreamingHttpResponse):
    """
    Streaming JSON response.
    """

    def __init__(self, data, encoder=DjangoJSONEncoder, *args, **kwargs):
        """
        """

        kwargs["streaming_content"] = encoder().iterencode(data)
        kwargs["content_type"] = "application/json"

        super(StreamingJsonResponse, self).__init__(*args, **kwargs)