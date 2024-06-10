#define PY_SSIZE_T_CLEAN

#define DEBUG

#include <Python.h>
#include <dev-utils.h>

class Compressor
{
  public:
    Compressor(PyObject *bytes)
    {
        this->gzipmodule = PyImport_ImportModule("gzip");
        this->bytes = bytes;
    };
    inline PyObject *compress()
    {
        return PyObject_CallOneArg(
            PyObject_GetAttrString(
                this->gzipmodule, "compress"),
            this->bytes);
    };
    inline PyObject *decompress()
    {
        return PyObject_CallOneArg(
            PyObject_GetAttrString(
                this->gzipmodule, "decompress"),
            this->bytes);
    };

  private:
    PyObject *bytes;
    PyObject *gzipmodule;
};

PyObject *
_compress(PyObject *self, PyObject *args)
{
    PyObject *raw_text = NULL;

    if (!PyArg_ParseTuple(args, "S", &raw_text))
    {
        return NULL;
    }

    Compressor *compressor = new Compressor(raw_text);
    return compressor->compress();
}

PyObject *
_decompress(PyObject *self, PyObject *args)
{
    PyObject *compressd = NULL;

    if (!PyArg_ParseTuple(args, "S", &compressd))
    {
        return NULL;
    }
    Compressor *compressor = new Compressor(compressd);
    return compressor->decompress();
}

static PyMethodDef
    _compressmethods[] = {
        {"_compress", (PyCFunction)_compress, METH_VARARGS},
        {"_decompress", (PyCFunction)_decompress, METH_VARARGS},
        {0, NULL} // end
};

static struct PyModuleDef
    _compressmodule = {
        PyModuleDef_HEAD_INIT,        // head
        "uel.bytecodefile._compress", // name
        NULL,                         // doc
        -1,                           // size
        _compressmethods              // methods
};

PyMODINIT_FUNC
PyInit__compress(void)
{
    PyObject *module = PyModule_Create(&_compressmodule);
    return module;
}
