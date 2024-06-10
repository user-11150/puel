#include<core.h>

#ifdef DEBUG
#ifdef __cplusplus
extern "C"{
#endif
inline void PRINT(PyObject *object)
{
    PyObject* objprint = PyImport_ImportModule("objprint");

    PyObject_CallOneArg(
        PyObject_GetAttrString(objprint, "op"),
        object);
}
#ifdef __cplusplus
}
#endif
#endif
