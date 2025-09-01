import json,enum,datetime
from typing import Any

# JSON
class BaseType:
    def to_dict(self):
        # return dict([(k.lstrip("_"), v) for k, v in self.__dict__.items()])
        return {k.lstrip('_'):v for k, v in self.__dict__.items()}

    def to_dict_with_type(self):
        def _dict(obj):
            module = None
            if issubclass(obj.__class__, BaseType):
                data = {}
                for attr, v in obj.__dict__.items():
                    k = attr.lstrip("_")
                    data[k] = _dict(v)
                module = obj.__module__
            elif isinstance(obj, (list, tuple)):
                data = []
                for i, vv in enumerate(obj):
                    data.append(_dict(vv))
            elif isinstance(obj, dict):
                data = {}
                for _k, vv in obj.items():
                    data[_k] = _dict(vv)
            else:
                data = obj
            return {"type": obj.__class__.__name__,
                    "data": data, "module": module}

        return _dict(self)

class CustomJSONEncoder(json.JSONEncoder):
    def __init__(self, **kwargs):
        self._with_type = kwargs.pop("with_type", False)
        super().__init__(**kwargs)

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.timedelta):
            return str(obj)
        elif issubclass(type(obj), enum.Enum) or issubclass(type(obj), enum.IntEnum):
            return obj.value
        elif isinstance(obj, set):
            return list(obj)
        elif issubclass(type(obj), BaseType):
            if not self._with_type:
                return obj.to_dict()
            else:
                return obj.to_dict_with_type()
        elif isinstance(obj, type):
            return obj.__name__
        else:
            return json.JSONEncoder.default(self, obj)

def write_obj2file(obj:Any, filename:str):
    with open(filename_withext(filename,'json')) as jfile:
        jfile.write(json_dumps(obj=obj, ensure_ascii=False, indent=4))
        jfile.close()

def read_obj4file(filename:str) -> Any:
    jobj:Any
    with open(filename_withext(filename,'json')) as jfile:
        jobj=json_loads(jfile.read())
        jfile.close()
    return jobj

def filename_withext(filename:str,extname:str) -> str:
    return filename if filename.endswith(extname) \
    else f'{filename}.{extname}'

def json_dumps(obj:Any, **kw) -> str:
    return json.dumps(
        obj=obj,
        skipkeys=kw.get('skipkeys', False),
        ensure_ascii=kw.get('ensure_ascii', True),
        check_circular=kw.get('check_circular', True),
        allow_nan=kw.get('allow_nan', True),
        cls=kw.get('cls', CustomJSONEncoder),
        indent=kw.get('indent', None),
        separators=kw.get('separators', None),
        default=kw.get('default', None),
        sort_keys=kw.get('sort_keys', False),
    )

def json_loads(s:str|bytes|bytearray, **kw) -> Any:
    return json.loads(
        s=s,
        cls=kw.get('cls', None),
        object_hook=kw.get('object_hook', None),
        parse_float=kw.get('parse_float', None),
        parse_int=kw.get('parse_int', None),
        parse_constant=kw.get('parse_constant', None),
        object_pairs_hook=kw.get('object_pairs_hook', None),
    )

# Time
def datetimenow() -> datetime.datetime:
    return datetime.datetime.now()

def datenow() -> datetime.date:
    return datetimenow().date()

def timenow() -> datetime.time:
    return datetimenow().time()