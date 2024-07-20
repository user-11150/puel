#define PY_SSIZE_T_CLEAN

#include <Python.h>

PyObject*
throw(PyObject* self, PyObject* args)
{
    const char* message; 
    if(!PyArg_ParseTuple(args, "s", &message)){
        perror("error statement");
        return NULL;
        }
    printf("[UEL Internal Error]%s", message);
}

static PyMethodDef
    uelcore_internal_exceptionsmethods[] = {
        {"throw", (PyCFunction) throw, METH_FASTCALL},
        {NULL, NULL, 0, NULL}};

static struct PyModuleDef
    uelcore_internal_exceptionsmodule = {
        PyModuleDef_HEAD_INIT,

        "uel.internal.uelcore_internal_exceptions",
        NULL,
        -1,
        uelcore_internal_exceptionsmethods};

PyMODINIT_FUNC
PyInit_uelcore_internal_exceptions(void)
{
    return PyModule_Create(&uelcore_internal_exceptionsmodule);
};
