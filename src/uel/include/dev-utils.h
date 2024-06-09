#include<Python.h>

#ifdef DEBUG
inline void PRINT(PyObject *object)
{
    PyObject* objprint = PyImport_ImportModule("objprint");

    PyObject_CallOneArg(
        PyObject_GetAttrString(objprint, "op"),
        object);
}
#endif
