class StatbankError(Exception):
    pass


class TimeError(StatbankError):
    """Something went wrong in the time parser"""
    pass


class RequestError(StatbankError):
    pass
