#define PY_SSIZE_T_CLEAN

#define DEBUG

#include <core.h>
#include <dev-utils.h>

PyObject* gzipmodule = NULL;

PyObject *
_compress(PyObject *self, PyObject *args)
{
    PyObject *raw_text = NULL;

    if (!PyArg_ParseTuple(args, "S", &raw_text))
    {
        return NULL;
    }
    
    return PyObject_CallOneArg(
        PyObject_GetAttrString(gzipmodule, "compress"),
        raw_text
    );
}

PyObject *
_decompress(PyObject *self, PyObject *args)
{
    PyObject *compressd = NULL;

    if (!PyArg_ParseTuple(args, "S", &compressd))
    {
        return NULL;
    }
    
    return PyObject_CallOneArg(
       PyObject_GetAttrString(gzipmodule, "decompress"),
       compressd
    );
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
    
    gzipmodule = PyImport_ImportModule("gzip");
    
    return module;
}
