import pickle
import gzip

def compress(obj):
	return gzip.compress(pickle.dumps(obj))


def decompress(bytes_):
	return pickle.loads(gzip.decompress(bytes_))
