"""Parsers for the timestrings used in statbank data
"""

from statbank.error import TimeError

from datetime import datetime
import re


def parse(timestring):
    """Convert a statbank time string to a python datetime object.
    """
    for parser in _PARSERS:
        match = parser['pattern'].match(timestring)
        if match:
            groups = match.groups()
            ints = tuple(map(int, groups))
            time = parser['factory'](ints)
            return time

    raise TimeError('Unsupported time format {}'.format(timestring))


_DAY = '0?[1-9]|[12][0-9]|3[01]'
_WEEK = '0?[1-9]|[1-9]\d'
_MONTH = '0?[1-9]|1[012]'
_QUARTER = '[1-4]'
_YEAR = '\d{4}'

# a parser needs a regex pattern and a factory returning a datetime
_PARSERS = [
    {
        # Day: 2015M12D24
        'pattern': re.compile('^({year})M({month})D({day})$'.format(
            year=_YEAR,
            month=_MONTH,
            day=_DAY,
        ), flags=re.IGNORECASE),
        'factory': lambda groups: datetime(
            year=groups[0],
            month=groups[1],
            day=groups[2],
        ),
    },
    {   # Week interval: 2015U1-10
        'pattern': re.compile('^({year})(?:W|U)({week})-(?:{week})$'.format(
            year=_YEAR,
            week=_WEEK,
        ), flags=re.IGNORECASE),
        'factory': lambda groups: datetime.strptime(
            '{year}-{month}-{monday}'.format(
                year=groups[0],
                month=groups[1] - 1,
                monday=1,
            ),
            '%Y-%W-%w'
        ),
    },
    {
        # Month: 2015M12
        'pattern': re.compile('^({year})M({month})$'.format(
            year=_YEAR,
            month=_MONTH,
        ), flags=re.IGNORECASE),
        'factory': lambda groups: datetime(
            year=groups[0],
            month=groups[1],
            day=1,
        ),
    },
    {
        # Quarter: 2015K4 / 2015Q4 (danish/english)
        'pattern': re.compile('^({year})(?:Q|K)({quarter})$'.format(
            year=_YEAR,
            quarter=_QUARTER,
        ), flags=re.IGNORECASE),
        'factory': lambda groups: datetime(
            year=groups[0],
            month=3 * groups[1] - 2,
            day=1,
        ),
    },
    {   # Half-year: 2015H2
        'pattern': re.compile('^({year})H([12])$'.format(
            year=_YEAR,
        ), flags=re.IGNORECASE),
        'factory': lambda groups: datetime(
            year=groups[0],
            month=1 + 6 * (groups[1] - 1),
            day=1,
        ),
    },
    {   # Year: 2015
        'pattern': re.compile('^({year})$'.format(
            year=_YEAR,
        ), flags=re.IGNORECASE),
        'factory': lambda groups: datetime(
            year=groups[0],
            month=1,
            day=1,
        ),
    },
    {   # Season: 2014/2015
        'pattern': re.compile('^({year})/(?:{year})$'.format(
            year=_YEAR,
        ), flags=re.IGNORECASE),
        'factory': lambda groups: datetime(
            year=groups[0],
            month=1,
            day=1,
        ),
    },
    {   # Year interval: 2000:2015
        'pattern': re.compile('^({year}):(?:{year})$'.format(
            year=_YEAR,
        ), flags=re.IGNORECASE),
        'factory': lambda groups: datetime(
            year=groups[0],
            month=1,
            day=1,
        ),
    },
]
