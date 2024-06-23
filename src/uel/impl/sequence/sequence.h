#include "core.h"

#ifndef UEL_IMPL_SEQUENCE_H
#define UEL_IMPL_SEQUENCE_H

typedef struct SequenceObject
{
    PyObject_HEAD
        PyObject *list;
} SequenceObject;

extern PyObject * sequence_append(SequenceObject *self, PyObject *args);
extern PyObject * sequence_register(SequenceObject *self, PyObject *args);
extern PyObject * sequence_as_list(SequenceObject *self, PyObject *args);

#endif
