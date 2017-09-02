// -----------------------------------------------------------------------
// Image recognition module. Misc. utilities.

#include <Python.h>
#include <pygobject.h>

#include "imgrec.h"

// Get module property value

int get_int(char *name)

{
    int ret = 0;
    PyObject *res = PyObject_GetAttrString(module, name);
    if(res)
        ret = (int)PyInt_AsLong(res);
    return ret;
}

// Set module property value

int set_int(char *name, int val)

{
    int ret = PyObject_SetAttrString(module, name,  Py_BuildValue("i", val));
    return ret;
}
     
// Return verbose flag / level

int is_verbose(void)

{
    int ret = 0;
    PyObject *res = PyObject_GetAttrString(module, "verbose");
    if(res)
        ret = PyInt_AsLong(res);
    return ret;
}




