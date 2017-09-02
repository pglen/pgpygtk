// -----------------------------------------------------------------------
// Image recognition module. The 'c' module is 2000 times faster than
// the 'py' version. See blank function for timings.
//
// Usage:   Feed an anchor array (pointer to buffer, dim1, dim2, dim3) 
//          then call appropriate function(s).
//
// Functions:
//
//   anchor(arr)                    - associate image arr
//   blank(x, y, x2, y2, color)     - blank rect with color
//   grayen(x, y, x2, y2, addcolor) - blank rect with color
//   whiten(x, y, x2, y2, subcolor) - blank rect with color
//   frame(x, y, x2, y2, color)     - draw frame with color
//   line(x, y, x2, y2, color)      - draw line with color
//
// ColorSpec:   32 bit, 0xAABBGGRR
//              AA = Alpha ; BB = Blue ; GG = Green ; RR = Red 
//              In the range of  0 - 255 (0x0 - 0xff)
//
// Grayen / Whiten addcolor/subcolr spec:  
//              0 - 255  (0x0 - 0xff)
//
// Coordinates:
//              x  = start x-axis ; y  = start y-axis 
//              x2 = end x-axis   ; y2 = end y-axis
//
//      o Coordinates are checked for out of bounds
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

static int __line(int arg1, int arg2, int arg3, int arg4, int arg5)

{
    int loop2, tmp;
    int *curr = anchor;

    // Swap them, if needed
    //if (arg2 > arg4) {
    //    tmp = arg2, arg2 = arg4, arg4 = tmp;  
    //    tmp = arg1, arg1 = arg3, arg3 = tmp; 
    //    }
    
    // Special cases:
    if (arg2 == arg4)               // Horiz
        {
        if(is_verbose())
            printf("horiz\n");
            
        if (arg1 > arg3) {              // Swap them, if needed
            tmp = arg2, arg2 = arg4, arg4 = tmp;  
            tmp = arg1, arg1 = arg3, arg3 = tmp; 
            }
        int offs = dim2 * arg2;
        for (loop2 = arg1; loop2 < arg3; loop2++)
            curr[offs + loop2]  = arg5;
        }
    else if (arg1 == arg3)        // Vert
        {       
        if(is_verbose())
            printf("vert\n");
        if (arg2 > arg4) {
            tmp = arg2, arg2 = arg4, arg4 = tmp;  
            tmp = arg1, arg1 = arg3, arg3 = tmp; 
            }
        for (loop2 = arg2; loop2 < arg4; loop2++)
            curr[dim2 * loop2 + arg1]  = arg5;
        }
    else                       // General case
        {
        //   x=arg1, y=arg2  -- |
        //                      |-- x2=arg3 y2=arg4
        
        if( abs(arg3-arg1) > abs(arg4-arg2))
            {
            // x - major
            if (arg1 > arg3) {                       // Swap them, if needed
                tmp = arg2, arg2 = arg4, arg4 = tmp;  
                tmp = arg1, arg1 = arg3, arg3 = tmp; 
                }
            int dx = arg3 - arg1; int dy =  arg4 - arg2;
            double slope = ((double)dy) / dx;
            if(is_verbose())
                printf("x - major %f\n", slope);
            for (loop2 = 0; loop2 < dx; loop2++)
                {
                int offs = slope * loop2 + arg2;
                curr[offs * dim2 + loop2 + arg1]  = arg5;
                }
            }
        else                
            {
            // y - major
            if (arg2 > arg4) {                      // Swap them, if needed
                tmp = arg2, arg2 = arg4, arg4 = tmp;  
                tmp = arg1, arg1 = arg3, arg3 = tmp; 
                }
            int dx = arg3 - arg1; int dy =  arg4 - arg2;
            double slope = ((double)dx) / dy;
            if(is_verbose())
                printf("y - major %f\n", slope);
            for (loop2 = 0; loop2 < dy; loop2++)
                {
                int offs = slope * loop2 + arg1;
                curr[(loop2 + arg2) * dim2 + offs]  = arg5;
                }
            }
        }
    return 0;
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

static PyObject *_grayen(PyObject *self, PyObject *args, PyObject *kwargs)
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
        unsigned char rr, gg, bb;
        
        int old, offs = loop * dim2;
        for (loop2 = arg1; loop2 < arg3; loop2++)
            {
             old = curr[offs + loop2];
             
             // Break apart
             rr = old & 0xff; gg = (old>>8) & 0xff; bb = (old>>16) & 0xff;
             // Clip to 0
             if (rr > arg5) rr -= arg5; else  rr = 0;
             if (gg > arg5) gg -= arg5; else  gg = 0;
             if (bb > arg5) bb -= arg5; else  bb = 0;
             // Assemble            
             old = 0xff; old <<= 8; old |= bb; old <<= 8; 
             old |= gg; old <<= 8; old |= rr; 
             
             curr[offs + loop2] = old;
             }
        }
    return Py_BuildValue("");
}    

static PyObject *_whiten(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "startx", "starty","endx", "endy", "color", NULL };
    
    int arg1 = 0;  int arg2 = 0; int arg3 = 0;  int arg4 = 0; int arg5 = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiiiI", kwlist, &arg1, &arg2, &arg3, &arg4, &arg5))
            return NULL;
    
    if( is_verbose())
        printf("Whitening %d %d %d %d color=0x%x\n", arg1, arg2, arg3, arg4, arg5);
    
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
        unsigned char rr, gg, bb;
        
        int old, offs = loop * dim2;
        for (loop2 = arg1; loop2 < arg3; loop2++)
            {
             old = curr[offs + loop2];
             
             // Break apart
             rr = old & 0xff; gg = (old>>8) & 0xff; bb = (old>>16) & 0xff;
             // Clip to 255
             if (rr + arg5 < 255) rr += arg5; else  rr = 255;
             if (gg + arg5 < 255) gg += arg5; else  gg = 255;
             if (bb + arg5 < 255) bb += arg5; else  bb = 255;
             // Assemble            
             old = 0xff; old <<= 8; old |= bb; old <<= 8; 
             old |= gg; old <<= 8; old |= rr; 
             
             curr[offs + loop2] = old;
             }
        }
    return Py_BuildValue("");
}    

static PyObject *_median(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "startx", "starty","endx", "endy", NULL };
    
    int arg1 = 0;  int arg2 = 0; int arg3 = 0;  int arg4 = 0; 
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiii", kwlist, &arg1, &arg2, &arg3, &arg4))
            return NULL;
    
    if( is_verbose())
        printf("Median %d %d %d %d\n", arg1, arg2, arg3, arg4);
    
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
    double mediall = 0;
    int *curr = anchor, loop, loop2;
    for (loop = arg2; loop < arg4; loop++)
        {
        int offs = loop * dim2;
        double medi = 0;
        for (loop2 = arg1; loop2 < arg3; loop2++)
            {
            medi += curr[offs + loop2] & 0x00ffffff;
            }
        medi /= (arg3-arg1);
        mediall += medi;    
        }
    mediall /= (arg4-arg2);

    //if( is_verbose())
    //    printf("Median result 0x%x\n", (int)mediall);
    
    return Py_BuildValue("I", (int)mediall);
}    

static PyObject *_frame(PyObject *self, PyObject *args, PyObject *kwargs)
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
    int *curr = anchor, loop2;
    
    int offs = dim2 * arg2;
    for (loop2 = arg1; loop2 < arg3; loop2++)
        curr[offs + loop2]  = arg5;
        
    int offs2 = dim2 * arg4;
    for (loop2 = arg1; loop2 < arg3; loop2++)
        curr[offs2 + loop2]  = arg5;
        
    for (loop2 = arg2; loop2 < arg4; loop2++)
        curr[dim2 * loop2 + arg1]  = arg5;
    
    for (loop2 = arg2; loop2 < arg4; loop2++)
        curr[dim2 * loop2 + arg3]  = arg5;
        
    //for (loop = arg2; loop < arg4; loop++)
    //    {
    //    }
    
    return Py_BuildValue("");
} 
   
static PyObject *_line(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "startx", "starty","endx", "endy", "color", NULL };
    
    int arg1 = 0; int arg2 = 0; int arg3 = 0;  int arg4 = 0; int arg5 = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "iiiiI", kwlist, &arg1, &arg2, &arg3, &arg4, &arg5))
            return NULL;
    
    if( is_verbose())
        printf("Line %d %d %d %d color=0x%x\n", arg1, arg2, arg3, arg4, arg5);
    
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
    __line(arg1, arg2, arg3, arg4, arg5);
    
    return Py_BuildValue("");
} 

static PyObject *_poly(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "color", "points", NULL };
    
    int arg5 = 0; PyObject *tup = 0; 
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "IO", kwlist, &arg5, &tup))
            return NULL;
    
    int len = PyTuple_GET_SIZE(tup);
    if(len % 2 != 0 || len < 4)
        {
        PyErr_Format(PyExc_ValueError, "%s", "num of coords must be dvisible 2 and >= 4");
        return NULL;
        }
        
    if( is_verbose())
        printf("Poly color=%x len=%d\n", arg5, len);
    
    if(!anchor)
        {
        PyErr_Format(PyExc_ValueError, "%s", "anchor must be set before any operation");
        return NULL;
        }
        
    int arg1, arg2, loop;
    // Inital points
    PyObject *d1 = PyTuple_GetItem(tup, 0); arg1 = PyInt_AsLong(d1);
    PyObject *d2 = PyTuple_GetItem(tup, 1); arg2 = PyInt_AsLong(d2);
        
    // Collect valuses, paint
    for(loop = 2; loop < len; loop += 2)
        {
        PyObject *d11 = PyTuple_GetItem(tup, loop);
        int arg3 = PyInt_AsLong(d11);
        
        PyObject *d21 = PyTuple_GetItem(tup, loop+1);
        int arg4 = PyInt_AsLong(d21);

        if( is_verbose())
            printf("Drawing line: %d %d %d %d\n", arg1, arg2, arg3, arg4);
            
         __line(arg1, arg2, arg3, arg4, arg5);
         
         arg1 = arg3; arg2 = arg4;
        }    
        
    return Py_BuildValue("");
} 

// -----------------------------------------------------------------------
// Anchor object

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
        PyErr_Format(PyExc_ValueError, "%s", "argument must have shape property (like: arr)");
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
        printf("Anchor Dimensions: %ld %ld %ld Pointer: %p\n", dim1, dim2, dim3, anchor);
        
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

char blankdoc[] = "Blank part of an image. Args: startx, starty, endx, endy.";

PyMethodDef imgrec_functions[] = 
    {
    { "version",   (PyCFunction)_version, METH_VARARGS|METH_KEYWORDS, "Image recognition version."},
    { "builddate", (PyCFunction)_bdate,   METH_VARARGS|METH_KEYWORDS, "Image recognition build date."},
    { "anchor",    (PyCFunction)_anchor,  METH_VARARGS|METH_KEYWORDS, "Set anchor to image."},
    { "blank",     (PyCFunction)_blank,   METH_VARARGS|METH_KEYWORDS,  blankdoc },
    { "median",    (PyCFunction)_median,  METH_VARARGS|METH_KEYWORDS,  "Calculate median of range." },
    { "grayen",    (PyCFunction)_grayen,  METH_VARARGS|METH_KEYWORDS,  "Grayen range." },
    { "whiten",    (PyCFunction)_whiten,  METH_VARARGS|METH_KEYWORDS,  "Whiten range." },
    { "frame",     (PyCFunction)_frame,   METH_VARARGS|METH_KEYWORDS,  "Frame range." },
    { "line",      (PyCFunction)_line,    METH_VARARGS|METH_KEYWORDS,  "Draw a line." },
    { "poly",      (PyCFunction)_poly,    METH_VARARGS|METH_KEYWORDS,  "Draw a poly line." },
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














