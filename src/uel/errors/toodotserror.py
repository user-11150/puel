from uel.errors.uelbuildtimeexception import UELBuildtimeException

__all__ = ["TooDotsError"]


class TooDotsError(UELBuildtimeException):
    """当一个数字中出现太多点时，比如“1.2.4”，将会引发此错误"""
    pass
