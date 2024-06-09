#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <dev-utils.h>

PyObject *
_compress(PyObject *self, PyObject *args)
{
    return PyTuple_GetItem(args, 0);
}

PyObject *
_decompress(PyObject *self, PyObject *args)
{
    return PyTuple_GetItem(args, 0);
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
