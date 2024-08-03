#include <Python.h>

static PyMethodDef
_iomethods[] = {
    {NULL, NULL, 0, NULL}
};

static PyModuleDef
_iomodule = {
    PyModuleDef_HEAD_INIT,
    "uel.io._io",
    NULL,
    -1,
    _iomethods
};

PyMODINIT_FUNC
PyInit__io(){
    return PyModule_Create(&_iomodule);
}
