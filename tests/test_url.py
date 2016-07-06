from statbank.config import BASE_URL
from statbank.url import URL

import unittest


class TestURL(unittest.TestCase):

    def setUp(self):
        self.segments = ['foo', None, [1, 2]]
        self.params = dict(b=False, a='bar', d=['x', 'y', 'z'], c=None)

        self.segmentstring = '/foo/1,2'
        self.paramstring = '?a=bar&b=false&d=x%2Cy%2Cz'

    def test_url(self):
        url = URL(*self.segments, **self.params)
        self.assertEqual(str(url), BASE_URL + self.segmentstring + self.paramstring)

    def test_nosegments(self):
        url = URL(**self.params)
        self.assertEqual(str(url), BASE_URL + self.paramstring)

    def test_noparams(self):
        url = URL(*self.segments)
        self.assertEqual(str(url), BASE_URL + self.segmentstring)


if __name__ == '__main__':
    unittest.main()
