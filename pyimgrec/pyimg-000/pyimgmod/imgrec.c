// Image recognition module

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <Python.h>

#define OPEN_IMAGE 1

/* include this first, before NO_IMPORT_PYGOBJECT is defined */
#include <pygobject.h>

void initimgrec(void);

#if 0

/* ----------- types ----------- */

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

/* ----------- functions ----------- */

static PyObject *
_hello(PyObject *self, PyObject *args, PyObject *kwargs)
{
    //static char *kwlist[] = { "name", "calendar", NULL };
    //char *name;
    //PyGObject *calendar;
    //void *ret;

    //if (!PyArg_ParseTupleAndKeywords(args, kwargs,"sO!:mrp_calendar_copy", kwlist, &name, &PyMyObj_Type, &calendar))
    //    return NULL;
    
    //ret = mrp_calendar_copy(name, MRP_CALENDAR(calendar->obj));
    
    return Py_BuildValue("s", "Hello from imgrec");
    
    /* pygobject_new handles NULL checking */
    //return pygobject_new((GObject *)ret);
}

PyMethodDef imgrec_functions[] = {
    { "hello", (PyCFunction)_hello, METH_VARARGS|METH_KEYWORDS, "Hello image recognition function."},
    {  NULL },
    };
    

DL_EXPORT(void)
initimgrec(void)
{
    PyObject *module, *d;
	
    init_pygobject ();

    module = Py_InitModule3("imgrec", imgrec_functions, "Image recognition library for Python");
    d = PyModule_GetDict (module);
	
    char *strip_prefix = "";
    PyModule_AddIntConstant(module, (char *) pyg_constant_strip_prefix("OPEN_IMAGE", strip_prefix), OPEN_IMAGE);

    //#planner_register_classes (d);
    //#planner_add_constants (m, "MRP_");

    if (PyErr_Occurred ()) {
	Py_FatalError ("can't initialise imgrec module");
    }
}



