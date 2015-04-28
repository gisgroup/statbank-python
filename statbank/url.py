"""Handle statbank urls
"""

from statbank import config
from urllib.parse import urlencode


class URL:
    def __init__(self, *segments, **params):
        self.segments = segments
        self.params = params

    def __getitem__(self, key):
        return self.params[key]

    def __setitem__(self, key, value):
        self.params[key] = value

    def __str__(self):
        url = config.BASE_URL
        if self.segments:
            prepped = [self.prep(v) for v in self.segments if v]
            url += '/'.join(prepped)

        if self.params:
            prepped = {k: self.prep(v) for k, v in self.params.items() if v}
            encoded = urlencode(prepped)
            url += '?' + encoded

        return url

    @staticmethod
    def prep(value):
        if type(value) == str:
            return value
        try:
            return ','.join(iter(value))
        except TypeError:
            return value
