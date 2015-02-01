from __future__ import absolute_import

# Try to load the best available JSON module
__loaded__ = None

try:
    from ujson import *
    __loaded__ = "ujson"
except ImportError:
    try:
        from cjson import *
        __loaded__ = "cjson"

        # Monkey patch methods
        dumps = encode
        loads = decode
    except ImportError:
        from json import loads, dumps
        __loaded__ = "json"