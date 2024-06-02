import pickle
import gzip

class BCompressor:
    """
    The Bytecode Compressor and Decompressor
    """
    
    REQUIREMENTS_KEY = "requirements"
    DATA_KEY = "data"
    
    @staticmethod
    def compress(bytecodes):
        return gzip.compress(pickle.dumps(bytecodes))

    @staticmethod
    def decompress(bytes_):
        d = pickle.loads(gzip.decompress(bytes_))
        return d

_bcompressor = BCompressor()
compress = _bcompressor.compress
uncompress = decompress = _bcompressor.decompress
