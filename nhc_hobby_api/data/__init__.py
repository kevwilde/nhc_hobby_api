from itertools import islice
import re


class NHCData(object):

    def __init__(self, context, api):
        self.ctx = context
        self.api = api

    def __getattr__(self, name):
        # exception to generic naming convention
        if name == "sw_versions":
            return self.ctx.get("SWversions")
        return self.ctx.get(self.to_camel_case(name))

    def to_snake_case(self, camel_case_string):
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        return pattern.sub('_', camel_case_string).lower()

    def to_camel_case(self, snake_case_object):
        if type(snake_case_object) == str:
            components = snake_case_object.split('_')
            return ''.join(x.title() for x in components)
        elif type(snake_case_object) == list:
            return [self.to_camel_case(v) for v in snake_case_object]
        elif type(snake_case_object) == dict:
            return {self.to_camel_case(k): self.to_camel_case(v) for k, v in snake_case_object.items()}

    def chunkify_dict(self, data):
        it = iter(data)
        for _ in range(0, len(data), 1):
            yield {k:data[k] for k in islice(it, 1)}

    def canonical_name(self):
        return self.__class__.__name__

    def keys(self):
        return [self.to_snake_case(k) for k in self.ctx.keys()]

    def __str__(self):
        return f"<nhc.{self.canonical_name()}>"


class NHCDictionary(NHCData):
    
    def __init__(self, context):
        self.ctx = {}
        if context is not None:
            for item in context: 
                self.ctx.update(item)

    def __str__(self):
        return f"<nhc.{self.canonical_name()}[" + ",".join(self.keys()) + "]>"

    def get(self, key):
        return self.ctx.get(key)


from .system import *
from .devices import *
from .locations import *