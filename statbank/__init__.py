"""
Handle communcation with the statbank API
http://www.dst.dk/en/Statistik/statistikbanken.aspx

The purpose of these functions is to wrap the statbank api endpoints in
pythonic methods, by translating url params from lowercase/underscore to camel-
case, and converting raw nested dicts/lists into iterators over relevant
objects (like instances of a Table class, etc).
"""

from statbank.config import DEFAULT_LANGUAGE
from statbank.request import Request
from statbank.resources import Data, Subject, Tableinfo, Table


def data(tableid,
         variables=dict(),
         stream=False,
         descending=False,
         lang=DEFAULT_LANGUAGE):
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
                      lang=lang,
                      **variables)

    return (Data(datum, lang=lang) for datum in request.csv)


def subjects(subjects=None,
             recursive=False,
             include_tables=False,
             lang=DEFAULT_LANGUAGE):
    """List subjects from the subject hierarchy.

    If subjects is not given, the root subjects will be used.

    Returns a generator.
    """
    request = Request('subjects', *subjects,
                      recursive=recursive,
                      includeTables=include_tables,
                      lang=lang)

    return (Subject(subject, lang=lang) for subject in request.json)


def tableinfo(tableid, lang=DEFAULT_LANGUAGE):
    """Fetch metadata for statbank table

    Metadata includes information about variables,
    which can be used when extracting data.
    """
    request = Request('tableinfo', tableid, lang=lang)

    return Tableinfo(request.json, lang=lang)


def tables(subjects=None,
           pastDays=None,
           include_inactive=False,
           lang=DEFAULT_LANGUAGE):
    """Find tables placed under given subjects.
    """
    request = Request('tables',
                      subjects=subjects,
                      pastDays=pastDays,
                      includeInactive=include_inactive,
                      lang=lang)

    return (Table(table, lang=lang) for table in request.json)
