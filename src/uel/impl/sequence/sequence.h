#include "core.h"

#define ABORT -1

typedef struct SequenceObject
{
    PyObject_HEAD
    PyObject *list;
} SequenceObject;
