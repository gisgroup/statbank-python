import statbank

import unittest


class TestService(unittest.TestCase):

    def test_tables(self):
        list(statbank.data('bev107', lang='da', variables={
            'BEVÆGELSE': '*',
        }))
        list(statbank.tables(subjects=['02']))
        statbank.tableinfo('aup03')
        list(statbank.subjects(subjects=['02']))
        pass


if __name__ == '__main__':
    unittest.main()
