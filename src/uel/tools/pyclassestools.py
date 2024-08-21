class Singletonmode:
    def __new__(cls, *args, **kwargs):
        if hasattr(cls, '__slots__'):
            raise TypeError("'__slots__' is defined")
        if hasattr(cls, 'obj'):
            return cls.obj
        ＯＢＪ = cls.obj = super().__new__(cls)
        return ＯＢＪ
