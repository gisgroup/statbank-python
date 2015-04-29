"""
Handle communcation with the statbank API
http://www.dst.dk/en/Statistik/statistikbanken.aspx

The purpose of these functions is to wrap the statbank api endpoints in
pythonic methods, by translating url params from lowercase/underscore to camel-
case, and converting raw nested dicts/lists into iterators over relevant
objects (like instances of a Table class, etc).
"""

from statbank.request import Request
from statbank.resources import Data, Subject, Tableinfo, Table


def data(tableid, variables, stream=False, descending=False):
    """Pulls data from a table and generates rows.

    Variables is a dictionary mapping variable codes to values.

    Streaming:
    Values must be chosen for all variables when streaming
    """
    # bulk is also in csv format, but the response is streamed
    format = 'BULK' if stream else 'CSV'

    request = Request('data', tableid, format,
                      timeOrder='Descending' if descending else None,
                      valuePresentation='CodeAndValue',
                      **variables)

    return (Data(datum) for datum in request.csv)


def subjects(subjects=None, recursive=False, include_tables=False):
    """List subjects from the subject hierarchy.

    If subjects is not given, the root subjects will be used.

    Returns a generator.
    """
    request = Request('subjects', *subjects,
                      recursive=recursive,
                      includeTables=include_tables)

    return (Subject(subject) for subject in request.json)


def tableinfo(tableid):
    """Fetch metadata for statbank table

    Metadata includes information about variables,
    which can be used when extracting data.
    """
    request = Request('tableinfo', tableid)

    return Tableinfo(request.json)


def tables(subjects=None, pastDays=None, include_inactive=False):
    """Find tables placed under given subjects.
    """
    request = Request('tables',
                      subjects=subjects,
                      pastDays=pastDays,
                      includeInactive=include_inactive)

    return (Table(table) for table in request.json)
