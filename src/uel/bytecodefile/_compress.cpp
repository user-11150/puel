#define PY_SSIZE_T_CLEAN

#include <core.h>
#include <dev-utils.h>
// Since this is a "meta-include" file, no #ifdef __cplusplus / extern "C" {

// Include Python header files
#include "patchlevel.h"
#include "pyconfig.h"
#include "pymacconfig.h"

#if defined(__sgi) && !defined(_SGI_MP_SOURCE)
#  define _SGI_MP_SOURCE
#endif

// stdlib.h, stdio.h, errno.h and string.h headers are not used by Python
// headers, but kept for backward compatibility. They are excluded from the
// limited C API of Python 3.11.
#if !defined(Py_LIMITED_API) || Py_LIMITED_API+0 < 0x030b0000
#  include <stdlib.h>
#  include <stdio.h>              // FILE*
#  include <errno.h>              // errno
#  include <string.h>             // memcpy()
#endif
#ifndef MS_WINDOWS
#  include <unistd.h>
#endif
#ifdef HAVE_STDDEF_H
#  include <stddef.h>             // size_t
#endif

#include <assert.h>               // assert()
#include <wchar.h>                // wchar_t

#include "pyport.h"
#include "pymacro.h"
#include "pymath.h"
#include "pymem.h"
#include "pytypedefs.h"
#include "pybuffer.h"
#include "object.h"
#include "objimpl.h"
#include "typeslots.h"
#include "pyhash.h"
#include "cpython/pydebug.h"
#include "bytearrayobject.h"
#include "bytesobject.h"
#include "unicodeobject.h"
#include "cpython/code.h"
#include "cpython/initconfig.h"
#include "pystate.h"
#include "pyerrors.h"
#include "longobject.h"
#include "cpython/longintrepr.h"
#include "boolobject.h"
#include "floatobject.h"
#include "complexobject.h"
#include "rangeobject.h"
#include "memoryobject.h"
#include "tupleobject.h"
#include "listobject.h"
#include "dictobject.h"
#include "cpython/odictobject.h"
#include "enumobject.h"
#include "setobject.h"
#include "methodobject.h"
#include "moduleobject.h"
#include "cpython/funcobject.h"
#include "cpython/classobject.h"
#include "fileobject.h"
#include "pycapsule.h"
#include "pyframe.h"
#include "traceback.h"
#include "sliceobject.h"
#include "cpython/cellobject.h"
#include "iterobject.h"
#include "cpython/genobject.h"
#include "descrobject.h"
#include "genericaliasobject.h"
#include "warnings.h"
#include "weakrefobject.h"
#include "structseq.h"
#include "cpython/picklebufobject.h"
#include "cpython/pytime.h"
#include "codecs.h"
#include "pythread.h"
#include "cpython/context.h"
#include "modsupport.h"
#include "compile.h"
#include "pythonrun.h"
#include "pylifecycle.h"
#include "ceval.h"
#include "sysmodule.h"
#include "osmodule.h"
#include "intrcheck.h"
#include "import.h"
#include "abstract.h"
#include "bltinmodule.h"
#include "cpython/pyctype.h"
#include "pystrtod.h"
#include "pystrcmp.h"
#include "fileutils.h"
#include "cpython/pyfpe.h"
#include "tracemalloc.h"

class Compressor
{
  public:
    Compressor(PyObject *bytes)
    {
        this->gzipmodule = PyImport_ImportModule("gzip");
        this->bytes = bytes;
    };
    inline PyObject *compress()
    {
        return PyObject_CallOneArg(
            PyObject_GetAttrString(
                this->gzipmodule, "compress"),
            this->bytes);
    };
    inline PyObject *decompress()
    {
        return PyObject_CallOneArg(
            PyObject_GetAttrString(
                this->gzipmodule, "decompress"),
            this->bytes);
    };

  private:
    PyObject *bytes;
    PyObject *gzipmodule;
};

PyObject *
_compress(PyObject *self, PyObject *args)
{
    PyObject *raw_text = NULL;

    if (!PyArg_ParseTuple(args, "S", &raw_text))
    {
        return NULL;
    }

    Compressor *compressor = new Compressor(raw_text);
    return compressor->compress();
}

PyObject *
_decompress(PyObject *self, PyObject *args)
{
    PyObject *compressd = NULL;

    if (!PyArg_ParseTuple(args, "S", &compressd))
    {
        return NULL;
    }
    Compressor *compressor = new Compressor(compressd);
    return compressor->decompress();
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
