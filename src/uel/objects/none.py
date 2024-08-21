from uel.tools.pyclassestools import Singletonmode
from uel.objects.object import UELObject


class UELNone(UELObject, Singletonmode):
    '''
    The None Object
    '''
    tp_name = 'None'

    def __repr__(self):
        return 'NoneObject'


uel_none = UELNone()
