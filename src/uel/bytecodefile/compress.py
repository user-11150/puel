import pickle

from uel.bytecodefile._compress import _compress, _decompress

def compress(obj):
	return _compress(pickle.dumps(obj))


def decompress(bytes_):
	return pickle.loads(_decompress(bytes_))
