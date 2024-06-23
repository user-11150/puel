#define PY_SSIZE_T_CLEAN

#define DEBUG

#include <core.h>

#include "./sequence.h"

PyObject *
sequence_append(SequenceObject *self, PyObject *args)
{
    PyObject *item;

    if (!PyArg_ParseTuple(args, "O", &item))
    {
        PyErr_SetString(PyExc_TypeError, "Arg 1 must be a object");
        return NULL;
    };

    if (self)
    {
        PyList_Append(self->list, item);
    }
    Py_RETURN_NONE;
};

PyObject *
sequence_register(SequenceObject *self, PyObject *args)
{
    PyObject *item;

    if (!PyArg_ParseTuple(args, "O", &item))
    {
        PyErr_SetString(PyExc_TypeError, "Arg 1 must be a object");
        return NULL;
    };

    if (self)
    {
        self->list = item;
    }
    Py_RETURN_NONE;
};

PyObject *
sequence_as_list(SequenceObject *self, PyObject *args)
{
    Py_INCREF(self->list);
    return self->list;
};

void Sequence_dealloc(SequenceObject *self)
{
    Py_DECREF(self);
}

static PyObject *
Sequence_New(PyTypeObject *type, PyObject *args, PyObject *kwgs)
{
    SequenceObject *self;
    self = (SequenceObject *)type->tp_alloc(type, 0);
    if (self)
    {
        self->list = PyList_New(0);
    }
    return (PyObject *)self;
};

static PyMethodDef
    sequencemethods[] = {
        {"append", (PyCFunction)sequence_append, METH_VARARGS},
        {"register", (PyCFunction)sequence_register, METH_VARARGS},
        {"as_list", (PyCFunction)sequence_as_list, METH_VARARGS},
        {NULL, NULL, 0, NULL}};

static PyTypeObject SequenceType = {
    PyVarObject_HEAD_INIT(NULL, 0)
        .tp_name = "uel.impl.sequence.Sequence",
    .tp_doc = "sequence",
    .tp_basicsize = sizeof(SequenceObject),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Sequence_New,
    .tp_dealloc = (destructor)Sequence_dealloc,
    .tp_methods = sequencemethods};

static PyModuleDef
    sequencemodule = {
        PyModuleDef_HEAD_INIT,
        "uel.impl.sequence",
        NULL,
        -1,
        NULL};
PyMODINIT_FUNC
PyInit_sequence()
{
    PyObject *module;

    if (PyType_Ready(&SequenceType) < 0)
    {
        return NULL;
    };

    module = PyModule_Create(&sequencemodule);
    Py_INCREF(&SequenceType);

    if (PyModule_AddObject(module, "Sequence", (PyObject *)&SequenceType) < 0)
    {
        return NULL;
    };
    return module;
};
