// -----------------------------------------------------------------------
// Image recognition module
//
// Use: feed an anchor array (pointer to buffer, dim1, dim2, dim3)
//

#include <Python.h>
#include <pygobject.h>

#include "bdate.h"

#define OPEN_IMAGE 1

void initimgrec(void);

// -----------------------------------------------------------------------
// Types: (not used)

#if 0

PyTypeObject G_GNUC_INTERNAL PyMyObj_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                                 /* ob_size */
    "planner.Calendar",                   /* tp_name */
    sizeof(PyGObject),          /* tp_basicsize */
    0,                                 /* tp_itemsize */
    /* methods */
    (destructor)0,        /* tp_dealloc */
    (printfunc)0,                      /* tp_print */
    (getattrfunc)0,       /* tp_getattr */
    (setattrfunc)0,       /* tp_setattr */
    (cmpfunc)0,           /* tp_compare */
    (reprfunc)0,             /* tp_repr */
    (PyNumberMethods*)0,     /* tp_as_number */
    (PySequenceMethods*)0, /* tp_as_sequence */
    (PyMappingMethods*)0,   /* tp_as_mapping */
    (hashfunc)0,             /* tp_hash */
    (ternaryfunc)0,          /* tp_call */
    (reprfunc)0,              /* tp_str */
    (getattrofunc)0,     /* tp_getattro */
    (setattrofunc)0,     /* tp_setattro */
    (PyBufferProcs*)0,  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,                      /* tp_flags */
    NULL,                        /* Documentation string */
    (traverseproc)0,     /* tp_traverse */
    (inquiry)0,             /* tp_clear */
    (richcmpfunc)0,   /* tp_richcompare */
    offsetof(PyGObject, weakreflist),             /* tp_weaklistoffset */
    (getiterfunc)0,          /* tp_iter */
    (iternextfunc)0,     /* tp_iternext */
    (struct PyMethodDef*)_PyMrpCalendar_methods, /* tp_methods */
    (struct PyMemberDef*)0,              /* tp_members */
    (struct PyGetSetDef*)0,  /* tp_getset */
    NULL,                              /* tp_base */
    NULL,                              /* tp_dict */
    (descrgetfunc)0,    /* tp_descr_get */
    (descrsetfunc)0,    /* tp_descr_set */
    offsetof(PyGObject, inst_dict),                 /* tp_dictoffset */
    (initproc)_wrap_mrp_calendar_new,             /* tp_init */
    (allocfunc)0,           /* tp_alloc */
    (newfunc)0,               /* tp_new */
    (freefunc)0,             /* tp_free */
    (inquiry)0              /* tp_is_gc */
};

#endif

// -----------------------------------------------------------------------
// Vars:

static  int *anchor = NULL;
static  int anclen = 0;
static  long dim1 = 0, dim2 = 0, dim3 = 0;
static  PyObject *module; 
	
// -----------------------------------------------------------------------
// Functions:

int is_verbose(void)

{
    int ret = 0;
    PyObject *res = PyObject_GetAttrString(module, "verbose");
    if(res)
        ret = PyInt_AsLong(res);
    return ret;
}

static PyObject *
_blank(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "begx", "begy","endx", "endy", NULL };
    int arg1 = 0;  int arg2 = 0;
    int arg3 = 0;  int arg4 = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiii", kwlist, &arg1, &arg2, &arg3, &arg4))
            return NULL;
    
    if( is_verbose())
        printf("Blanking %d %d %d %d\n", arg1, arg2, arg3, arg4);
    
    if(!anchor)
        {
        PyErr_Format(PyExc_ValueError, "%s", "anchor must be set before any operation");
        return NULL;
        }
        
    return Py_BuildValue("");
}    

static PyObject *
_anchor(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "imgarr", NULL };
    PyObject *anc = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", kwlist, &anc))
        return NULL;

    if(is_verbose())
        printf("Adding anchor\n");
    
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
                
                PyObject *d2 = PyTuple_GetItem(res2, 1);
                dim2 = PyInt_AsLong(d2);
                
                PyObject *d3 = PyTuple_GetItem(res2, 2);
                dim3 = PyInt_AsLong(d3);
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
                        
    int ret3 = PyObject_AsWriteBuffer(anc, &anchor, &anclen);
    if(ret3 < 0)
        {
        //printf("Cannot get pointer to buffer");
        PyErr_Format(PyExc_ValueError, "%s", "Cannot get pointer to buffer");
        return NULL;
        }
  
    // Sanity check
    if(is_verbose())
        printf("Dimensions: %ld %ld %ld\n", dim1, dim2, dim3);
        
    if(dim1*dim2*dim3 != anclen)
        {
        PyErr_Format(PyExc_ValueError, "%s", "Buffer len NE mul dim[123]");
        return NULL;
        }
        
    //printf("ret3 %d buff %p len %d\n", ret3, anchor, anclen);
    //printf("*buff %s", (char*)buff); printf("\n");
    
    return Py_BuildValue("");
}


static PyObject *
_bdate(PyObject *self, PyObject *args, PyObject *kwargs)
{
  return Py_BuildValue("s", bdate);
}
  
static PyObject *
_version(PyObject *self, PyObject *args, PyObject *kwargs)
{
    return Py_BuildValue("s", "1.0");
}

PyMethodDef imgrec_functions[] = 
    {
    { "version",   (PyCFunction)_version, METH_VARARGS|METH_KEYWORDS, "Image recognition version."},
    { "builddate", (PyCFunction)_bdate, METH_VARARGS|METH_KEYWORDS, "Image recognition build date."},
    { "anchor",    (PyCFunction)_anchor, METH_VARARGS|METH_KEYWORDS, "Set anchor to image."},
    { "blank",     (PyCFunction)_blank, METH_VARARGS|METH_KEYWORDS, "Blank part of an image."},
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
    PyObject *verbose;
    verbose = Py_BuildValue("i", 0);
    PyModule_AddObject(module, "verbose", verbose);
    //Py_DECREF(verbose);

    if (PyErr_Occurred ()) {       
	   Py_FatalError ("can't initialise imgrec module");
    }
}





