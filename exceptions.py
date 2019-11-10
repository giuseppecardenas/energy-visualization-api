import logging


class GisBackendBaseException(Exception):
    """
    Base exception class.
    """
    def __init__(self, msg=''):
        self.msg = msg
        logging.exception(msg)

    def __str__(self):
        return self.msg


class MapEntityException(GisBackendBaseException):
    """
    Raised when an invalid object is used to instantiate
    a MapEntity.
    """


class InvalidMapQueryException(GisBackendBaseException):
    """
    Raised when invalid parameters are used when creating
    a MapQuery object.
    """


class GisBackendException(GisBackendBaseException):
    """
    Raised when an error occurs getting results for a query.
    """