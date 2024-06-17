#include<Python.h>

PyObject* PRINT(PyObject* object)
{
    PyObject* objprint = PyImport_ImportModule("objprint");

    PyObject_CallOneArg(
        PyObject_GetAttrString(objprint, "op"),
        object);
    
    Py_RETURN_NONE;
}
