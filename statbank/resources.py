from statbank import config, time
from collections import namedtuple
import dateutil.parser
import locale
from dateutil.parser import parse as parsedate

Mapping = namedtuple('Mapping', 'label value')


class Resource():

    KEYS = []

    def __init__(self, d):
        for key in self.KEYS:
            setattr(self, key, d[key])


class Data(Resource):
    def __init__(self, row):
        # parse value as float according to locale
        value = row.pop(config.VALUE_KEY)
        locale.setlocale(locale.LC_NUMERIC, config.NUMBERS_LOCALE)
        # empty strings are handled as nulled values
        self.value = None if not value else locale.atof(value)
        locale.resetlocale()
        # parse time as timestamp
        timestring = row.pop('tid').split(' ', 1)[0]
        self.time = time.parse(timestring)
        self.variables = {k.lower(): Value(dict(zip(['id', 'text'], v.split(' ', 1)))) for k, v in row.items()}


class Subject(Resource):
    """"""

    KEYS = ['id',
            'description']

    def __init__(self, raw):
        if raw['hasSubjects']:
            self.subjects = map(raw['subjects'], self.__class__)
        else:
            self.subjects = []

        self.tables = (Table(table) for table in raw['tables'])
        super().__init__(raw)


class Table(Resource):
    """"""

    KEYS = ['id',
            'text',
            'unit',
            'firstPeriod',
            'latestPeriod',
            'active',
            'variables']

    def __init__(self, raw):
        self.updated = parsedate(str(raw['updated']))
        super().__init__(raw)


class Tableinfo(Resource):
    """Creates tableinfo object that hold info from the statbank API"""
    def __init__(self, raw):
        self.id = raw['id'].lower()
        self.raw = raw
        self.updated = dateutil.parser.parse(str(raw['updated']) + 'Z')
        self.unit = raw['unit']
        variables = [Variable(variable) for variable in raw['variables']]
        self.variables = {variable.id: variable for variable in variables}
        super().__init__(raw)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.__dict__)


class Variable(Resource):
    KEYS = ['text', 'time']

    def __init__(self, raw):
        self.id = raw['id'].lower()
        values = raw['values']
        if raw['time']:
            values = [Value.time(value) for value in values]
        else:
            values = [Value(value) for value in values]
        self.values = {v.id: v for v in values}
        super().__init__(raw)


class Value(Resource):
    KEYS = ['text']

    def __init__(self, raw):
        self.id = raw['id'].lower()
        super().__init__(raw)

    @classmethod
    def time(cls, raw):
        ins = cls(raw)
        ins.id = time.parse(raw['id'])
        return ins
