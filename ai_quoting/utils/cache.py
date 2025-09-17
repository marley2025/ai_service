import time
from collections import OrderedDict

class TTLCache:
    def __init__(self, max_items=256, ttl=300):
        self.max_items = max_items
        self.ttl = ttl
        self._data = OrderedDict()

    def get(self, key):
        item = self._data.get(key)
        if not item: return None
        value, ts = item
        if time.time() - ts > self.ttl:
            self._data.pop(key, None)
            return None
        self._data.move_to_end(key)
        return value

    def set(self, key, value):
        if key in self._data:
            self._data.move_to_end(key)
        self._data[key] = (value, time.time())
        if len(self._data) > self.max_items:
            self._data.popitem(last=False)
