class UELInternalError(Exception):
    pass


def throw(message):
    raise UELInternalError(message)
