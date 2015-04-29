import statbank

import unittest


class TestService(unittest.TestCase):

    def test_tables(self):
        statbank.data('aup03', language='en')
        statbank.tables(subjects=['02'])
        statbank.subjects(subjects=['02'])
        pass


if __name__ == '__main__':
    unittest.main()
