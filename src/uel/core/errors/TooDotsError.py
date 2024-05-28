from uel.core.errors.UELBuildtimeException import UELBuildtimeException


class TooDotsError(UELBuildtimeException):
    """当一个数字中出现太多点时，比如“1.2.4”，将会引发此错误"""
    pass
