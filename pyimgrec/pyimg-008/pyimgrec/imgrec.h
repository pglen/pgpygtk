// -----------------------------------------------------------------------
// Image recognition module. Local header.


// Vars shared between modules

extern int *anchor;
extern long dim1, dim2, dim3; 
extern PyObject *module;      

// Lines:

PyObject *_frame(PyObject *self, PyObject *args, PyObject *kwargs);
PyObject *_poly(PyObject *self, PyObject *args, PyObject *kwargs);
PyObject *_line(PyObject *self, PyObject *args, PyObject *kwargs);

// Squares:

PyObject *_median(PyObject *self, PyObject *args, PyObject *kwargs);
PyObject *_whiten(PyObject *self, PyObject *args, PyObject *kwargs);
PyObject *_median(PyObject *self, PyObject *args, PyObject *kwargs);    
PyObject *_blank(PyObject *self, PyObject *args, PyObject *kwargs);
PyObject *_grayen(PyObject *self, PyObject *args, PyObject *kwargs);
PyObject *_medianmulti(PyObject *self, PyObject *args, PyObject *kwargs);

// Colors:

PyObject *_diffcol(PyObject *self, PyObject *args, PyObject *kwargs);

// Utils:

int get_int(char *name);
int set_int(char *name, int val);
int is_verbose(void);




