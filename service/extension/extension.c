#include "Python.h"

#include "openssl/crypto.h"
#include "stdio.h"

static PyObject *SpamError;

static PyObject *IdCallback;
static PyObject *LockingCallback;


//--------------------------

static void locking_function(int mode, int n, const char * file, int line)
{
  PyObject *arglist;
  PyObject *result;

  printf("Enter locking_function\n");

  arglist = Py_BuildValue("(i, i, s, i)", mode, n, file, line);
  result = PyObject_CallObject(LockingCallback, arglist);
//  if(mode & CRYPTO_LOCK)
//
//    result = PyObject_CallObject(IdCallback, arglist);
//  else
//    a--;

  Py_DECREF(arglist);
    Py_DECREF(result);

    printf("Leave locking_function\n");
}

static unsigned long id_function(void)
{
    PyObject *arglist;
    PyObject *result;
    int value;

    arglist = Py_BuildValue(NULL);
    result = PyObject_CallObject(IdCallback, arglist);

    if (!PyArg_ParseTuple(result, "i", &value))
       return 0;

    Py_DECREF(arglist);
    Py_DECREF(result);

    return ((unsigned long)value);
}



//--------------------------



static PyObject *
spam_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    if (sts < 0) {
        PyErr_SetString(SpamError, "System command failed");
        return NULL;
    }
    return PyLong_FromLong(sts);
}

static PyObject * enable_mutexes(PyObject *self, PyObject *args) {
    PyObject *pIdCallback, *pLockingCallback;

    if (!PyArg_UnpackTuple(args, "enable_mutexes", 2, 2, &pIdCallback, &pLockingCallback)) {
		return NULL;
	}
	IdCallback = pIdCallback;
	LockingCallback = pLockingCallback;

    CRYPTO_set_id_callback(id_function);
    CRYPTO_set_locking_callback(locking_function);

    printf("Enabled mutexes\n");

    Py_RETURN_NONE;
}


static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
    {"enable_mutexes", enable_mutexes, METH_VARARGS,
     "Enable mutexes for openssl"},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC
initfoobar(void)
{
    (void) Py_InitModule("foobar", SpamMethods);
}
