"""Handle statbank urls
"""

from statbank import config

from collections import namedtuple
from operator import itemgetter
from urllib.parse import urlencode

Param = namedtuple('Param', 'key value')


class URL:
    def __init__(self, *segments, **params):
        self.segments = segments
        self.params = params

    def __str__(self):
        url = config.BASE_URL
        if self.segments:
            segments = [s for s in self.prep(self.segments) if s]
            url += '/' + '/'.join(segments)

        if self.params:
            # sort and unzip parameter dictionary
            keys, values = zip(*sorted(self.params.items(), key=itemgetter(0)))

            # prep and re-zip
            pairs = zip(keys, self.prep(values))

            filtered = [pair for pair in pairs if pair[1]]
            #url += '?' + '&'.join(strings)
            url += '?' + urlencode(list(filtered))

        return url

    @staticmethod
    def prep(values):
        for value in values:
            if value is None or type(value) == str:
                yield value
            else:
                try:
                    yield ','.join([str(v) for v in value])
                except TypeError:
                    yield str(value).lower()
