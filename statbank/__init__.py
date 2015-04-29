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
         language=DEFAULT_LANGUAGE):
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
                      lang=language,
                      **variables)

    return (Data(datum, language=language) for datum in request.csv)


def subjects(subjects=None,
             recursive=False,
             include_tables=False,
             language=DEFAULT_LANGUAGE):
    """List subjects from the subject hierarchy.

    If subjects is not given, the root subjects will be used.

    Returns a generator.
    """
    request = Request('subjects', *subjects,
                      recursive=recursive,
                      includeTables=include_tables,
                      lang=language)

    return (Subject(subject, language=language) for subject in request.json)


def tableinfo(tableid, language=DEFAULT_LANGUAGE):
    """Fetch metadata for statbank table

    Metadata includes information about variables,
    which can be used when extracting data.
    """
    request = Request('tableinfo', tableid, lang=language)

    return Tableinfo(request.json, language=language)


def tables(subjects=None,
           pastDays=None,
           include_inactive=False,
           language=DEFAULT_LANGUAGE):
    """Find tables placed under given subjects.
    """
    request = Request('tables',
                      subjects=subjects,
                      pastDays=pastDays,
                      includeInactive=include_inactive,
                      lang=language)

    return (Table(table, language=language) for table in request.json)
