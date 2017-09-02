// -----------------------------------------------------------------------
// Image recognition module. Line primitives.

#include <Python.h>
#include <pygobject.h>

#include "imgrec.h"

// -----------------------------------------------------------------------
//   diffcol(col1, col2) - diff color

PyObject *_diffcol(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "color1", "color2",  NULL };
    
    int arg1 = 0;  int arg2 = 0; 
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "II", kwlist, &arg1, &arg2))
            return NULL;
    
    if( is_verbose())
        printf("Sub Color %x %x\n", arg1, arg2);
    
     // Break apart
     int rr = arg1 & 0xff; int gg = (arg1>>8) & 0xff; 
     int bb = (arg1>>16) & 0xff;
     int rrr = arg2 & 0xff; int ggg = (arg2>>8) & 0xff; 
     int bbb = (arg2>>16) & 0xff;
     
     // Assemble
     int old = 0xff; old <<= 8; old |= abs(bb-bbb); old <<= 8; 
     old |= abs(gg-ggg); old <<= 8; old |= abs(rr - rrr); 

    int sin = abs(bb-bbb) + abs(gg-ggg) + abs(rr-rrr); sin /= 3;
    return Py_BuildValue("Ii", old, sin);
}    



