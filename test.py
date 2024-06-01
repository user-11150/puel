from uel import make_exports
from uel import UENumberObject

def time(f):
	return UENumberObject(1)

bytecodes = make_exports({
  "time": time
})
