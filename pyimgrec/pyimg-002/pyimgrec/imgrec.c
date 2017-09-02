// -----------------------------------------------------------------------
// Image recognition module. The 'c' module is 2000 times faster than
// the 'py' version. See blank function for timings.
//
// Use: feed an anchor array (pointer to buffer, dim1, dim2, dim3)
//
// Functions:
//
//   anchor(arr)                - associate image arr
//   blank(x, y, x2, y2, color) - blank rect with color
//

#include <Python.h>
#include <pygobject.h>

#include "bdate.h"

#define OPEN_IMAGE 1

// -----------------------------------------------------------------------
// Vars:

static  char version[] = "1.0";
static  int *anchor = NULL;
static  int anclen = 0;
static  long dim1 = 0, dim2 = 0, dim3 = 0;  // Replaced but py props
static  PyObject *module;                   // This is us
	
// -----------------------------------------------------------------------
// Functions:

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

// -----------------------------------------------------------------------
//   blank(x, y, x2, y2, color) - blank rect with color

static PyObject *_blank(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "startx", "starty","endx", "endy", "color", NULL };
    
    int arg1 = 0;  int arg2 = 0; int arg3 = 0;  int arg4 = 0; int arg5 = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiiiI", kwlist, &arg1, &arg2, &arg3, &arg4, &arg5))
            return NULL;
    
    if( is_verbose())
        printf("Blanking %d %d %d %d color=0x%x\n", arg1, arg2, arg3, arg4, arg5);
    
    if(!anchor)
        {
        PyErr_Format(PyExc_ValueError, "%s", "anchor must be set before any operation");
        return NULL;
        }
    if (arg1 < 0 || arg2 < 0 ||  arg3 < 0 ||  arg4  < 0 )
        {
        PyErr_Format(PyExc_ValueError, "%s", "argument(s) cannot be negative");
        return NULL;
        }
     if (arg1 > dim2 || arg2 > dim1 || arg3 > dim2 || arg4  > dim1 )
        {
        PyErr_Format(PyExc_ValueError, "%s (%ld %ld)", "must be within array limits", dim1, dim2);
        return NULL;
        }
        
    // All set, flush it out
    int *curr = anchor, loop, loop2;
    for (loop = arg2; loop < arg4; loop++)
        {
        int offs = loop * dim2;
        for (loop2 = arg1; loop2 < arg3; loop2++)
             curr[offs + loop2]  = arg5;
        }
    return Py_BuildValue("");
}    

static PyObject *_anchor(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "imgarr", NULL };
    PyObject *anc = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", kwlist, &anc))
        return NULL;

    char *pname = "shape";
    if (PyObject_HasAttrString(anc, pname))
        {
        PyObject *res2 = PyObject_GetAttrString(anc, pname);
        if (PyTuple_Check(res2))
            {
            if (PyTuple_GET_SIZE(res2) == 3)
                {                    
                PyObject *d1 = PyTuple_GetItem(res2, 0);
                dim1 = PyInt_AsLong(d1);
                PyObject_SetAttrString(module, "dim1", Py_BuildValue("i", dim1));
                
                PyObject *d2 = PyTuple_GetItem(res2, 1);
                dim2 = PyInt_AsLong(d2);
                PyObject_SetAttrString(module, "dim2", Py_BuildValue("i", dim2));
                
                PyObject *d3 = PyTuple_GetItem(res2, 2);
                dim3 = PyInt_AsLong(d3);
                PyObject_SetAttrString(module, "dim3", Py_BuildValue("i", dim3));
                }
           else {                                
                //printf("shape dim must be 3");
                PyErr_Format(PyExc_ValueError, "%s", "shape dim must be 3");
                return NULL;
                }
            }
        else
            {
            //printf("shape must be tuple");
            PyErr_Format(PyExc_ValueError, "%s", "shape must be tuple");
            return NULL;
            }
        }
    else
        {
        //printf("must have shape attr");
        PyErr_Format(PyExc_ValueError, "%s", "argument must have shape proerty");
        return NULL;
        }
    
    //printf("_anchor %p %d %p\n", anc, res, res2); 
                        
    // Cast it so int * will not complain                        
    int ret3 = PyObject_AsWriteBuffer(anc, (void**)&anchor, &anclen);
    if(ret3 < 0)
        {
        //printf("Cannot get pointer to buffer");
        PyErr_Format(PyExc_ValueError, "%s", "Cannot get pointer to buffer");
        return NULL;
        }
  
    if(is_verbose())
        printf("Anchor Dimensions: %ld %ld %ld\n", dim1, dim2, dim3);
        
    // Sanity check
    if(dim1*dim2*dim3 != anclen)
        {
        PyErr_Format(PyExc_ValueError, "%s", "Buffer len NE mul dim[123]");
        return NULL;
        }
        
    //printf("ret3 %d buff %p len %d\n", ret3, anchor, anclen);
    //printf("*buff %s", (char*)buff); printf("\n");
    
    return Py_BuildValue("");
}


static PyObject *_bdate(PyObject *self, PyObject *args, PyObject *kwargs)
{
  return Py_BuildValue("s", bdate);
}
  
static PyObject *_version(PyObject *self, PyObject *args, PyObject *kwargs)
{
    return Py_BuildValue("s", version);
}

char blankdoc[] = "Blank part of an image. Args: startx, starty, endx, endy";

PyMethodDef imgrec_functions[] = 
    {
    { "version",   (PyCFunction)_version, METH_VARARGS|METH_KEYWORDS, "Image recognition version."},
    { "builddate", (PyCFunction)_bdate, METH_VARARGS|METH_KEYWORDS, "Image recognition build date."},
    { "anchor",    (PyCFunction)_anchor, METH_VARARGS|METH_KEYWORDS, "Set anchor to image."},
    { "blank",     (PyCFunction)_blank, METH_VARARGS|METH_KEYWORDS,  blankdoc },
    {  NULL },
    };

// -----------------------------------------------------------------------
// Init:

DL_EXPORT(void) 
initimgrec(void)
{
 
    init_pygobject ();

    module = Py_InitModule3("imgrec", imgrec_functions, "Image Recognition library for Python");
    //d = PyModule_GetDict (module);
    
    // Constants
    PyModule_AddIntConstant(module, (char *)"OPEN_IMAGE", OPEN_IMAGE);
    PyModule_AddStringConstant(module, (char *)"author", "Peter Glen");

    // Values:
    PyModule_AddObject(module, "verbose",   Py_BuildValue("i", 0));
    PyModule_AddObject(module, "dim1",      Py_BuildValue("i", 0));
    PyModule_AddObject(module, "dim2",      Py_BuildValue("i", 0));
    PyModule_AddObject(module, "dim3",      Py_BuildValue("i", 0));

    if (PyErr_Occurred ()) {       
	   Py_FatalError ("can't initialise imgrec module");
    }
}







