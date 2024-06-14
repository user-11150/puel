#define PY_SSIZE_T_CLEAN

#define DEBUG
#include <core.h>
#include <dev-utils.h>

void brainfuck(char *code)
{
    char *p = NULL;
    char *data = (char *)malloc(30000);
    char *ptr = data;
    int pc = 0;

    while (*code)
    {
        switch (*code)
        {
        case '>':
            ++ptr;
            break;
        case '<':
            --ptr;
            break;
        case '+':
            ++(*ptr);
            break;
        case '-':
            --(*ptr);

            break;
        case '.':
            PySys_WriteStdout(ptr);
            break;
        case ',':
            *ptr = *p++;
            break;
        case '[':
            if (!*ptr)
            {
                int brackets = 1;
                do
                {
                    ++code;
                    brackets += *code == '[';
                    brackets -= *code == ']';
                } while (brackets);
            }
            break;
        case ']':
            if (*ptr)
            {
                int brackets = 1;
                do
                {
                    --code;
                    brackets += *code == ']';
                    brackets -= *code == '[';
                } while (brackets);
            }
            break;
        }
        ++code;
    }

    free(data);
}

PyObject *
Py_brainfuck_run(PyObject *self, PyObject *args)
{
    char *code = NULL;

    if (!PyArg_ParseTuple(args, "s", &code))
    {
        return NULL;
    }
    brainfuck(code);

    Py_RETURN_NONE;
}

static PyMethodDef
    _brainfuckmethods[] = {
        {"run", (PyCFunction)Py_brainfuck_run, METH_VARARGS},
        {0, NULL} // end
};

static PyModuleDef
    _brainfuckmodule = {
        PyModuleDef_HEAD_INIT,
        "uel.brainfuck._brainfuck",
        NULL,
        -1,
        _brainfuckmethods};

PyMODINIT_FUNC
PyInit__brainfuck()
{
    return PyModule_Create(&_brainfuckmodule);
}
