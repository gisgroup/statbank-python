from urllib.request import urlopen
from urllib.error import HTTPError
import json

from statbank import config
from statbank.url import URL
from statbank.error import RequestError, StatbankError


class Request:
    """Represent a request to the statbank api.

    After initializing the request, one can read an appropriate property to
    parse the response as the corresponding format.
    """
    def __init__(self, *segments, **params):
        """Perform a request in each language and return a list of responses.

        Positional arguments become url segments appended to the base url,
        while keyword arguments turn into query parameters.
        """
        try:
            url = URL(*segments, **params)
            self.response = urlopen(str(url))
        except HTTPError as error:
            try:
                # parse error body as json and use message property as error message
                parsed = self._parsejson(error)
                raise RequestError(parsed['message']) from None
            except ValueError:
                # when error body is not valid json, error might be caused by server
                raise StatbankError() from None

    @property
    def json(self):
        """Parse response as json and return nested dicts/lists.
        """
        return self._parsejson(self.response)

    @property
    def csv(self):
        """Parse response as csv and return row object list.
        """
        lines = self._parsecsv(self.response)

        # set keys from header line (first line)
        keys = next(lines)

        for line in lines:
            yield dict(zip(keys, line))

    @staticmethod
    def _parsecsv(x):
        """Deserialize file-like object containing csv to a Python generator.
        """
        for line in x:
            # decode as utf-8, whitespace-strip and split on delimiter
            yield line.decode('utf-8').strip().split(config.DELIMITER)

    @staticmethod
    def _parsejson(x):
        """Deserialize file-like object containing json to a Python obejct.
        """
        return json.loads(x.read().decode('utf-8'))
