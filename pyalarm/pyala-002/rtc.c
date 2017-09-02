// -----------------------------------------------------------------------
// RTC handler
//

#include <Python.h>
#include <pygobject.h>

#include <stdio.h>
#include <linux/rtc.h>
#include <sys/ioctl.h>
#include <sys/time.h>
#include <sys/types.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <errno.h>

#define READ_RTC 1
  
#include "rtc.h"
#include "bdate.h"
  
// -----------------------------------------------------------------------
// Vars:

int *anchor = NULL;
long dim1 = 0, dim2 = 0, dim3 = 0;  // Replaced but py props
PyObject *module;                   // This is us

static  char version[] = "1.0";
static const char def_rtc[] = "/dev/rtc";

static PyObject *_walarm(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"DateTime", NULL };
    PyObject *anc = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", kwlist, &anc))
        return NULL;
        
    if (!PySequence_Check(anc))
        {
        PyErr_Format(PyExc_ValueError, "%s", "RTC date/time must be a sequence");
        return NULL;
        }
    if (PySequence_Size(anc) != 6)
        {
        PyErr_Format(PyExc_ValueError, "%s", "RTC date/time must have 6 members");
        return NULL;
        }
    PyObject *d1 = PySequence_GetItem(anc, 0);
    PyObject *d2 = PySequence_GetItem(anc, 1);
    PyObject *d3 = PySequence_GetItem(anc, 2);
    PyObject *d4 = PySequence_GetItem(anc, 3);
    PyObject *d5 = PySequence_GetItem(anc, 4);
    PyObject *d6 = PySequence_GetItem(anc, 5);
            
    /* Write the RTC time/date */
    struct rtc_time rtc_tm;
    
    rtc_tm.tm_year = PyInt_AsLong(d1) - 1900;
    rtc_tm.tm_mon  = PyInt_AsLong(d2) - 1;
    rtc_tm.tm_mday = PyInt_AsLong(d3);
    rtc_tm.tm_hour = PyInt_AsLong(d4);
    rtc_tm.tm_min  = PyInt_AsLong(d5);
    rtc_tm.tm_sec  = PyInt_AsLong(d6);
    
    printf("Write alarm: %04d/%02d/%02d %02d:%02d:%02d\n",
                rtc_tm.tm_year + 1900,
                rtc_tm.tm_mon + 1, 
                rtc_tm.tm_mday, 
                rtc_tm.tm_hour, rtc_tm.tm_min, rtc_tm.tm_sec);
    
    //int fd = open(def_rtc, O_RDWR);
    int fd = open(def_rtc, O_RDONLY);
    if (fd ==  -1) 
        {
        PyErr_Format(PyExc_ValueError, "%s", "Cannot open RTC device");
        return NULL;
        }
    
    int retval = ioctl(fd, RTC_ALM_SET, &rtc_tm);
    if (retval == -1) {
        close(fd);
        PyErr_Format(PyExc_IOError, "%s", "Cannot write to RTC device");
        return NULL;
        }
    //printf("Called RTC write date\n"); 
    close(fd);
    return Py_BuildValue("");
}

static PyObject *_wwake(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"DateTime", NULL };
    PyObject *anc = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", kwlist, &anc))
        return NULL;
        
    if (!PySequence_Check(anc))
        {
        PyErr_Format(PyExc_ValueError, "%s", "RTC date/time must be a sequence");
        return NULL;
        }
    if (PySequence_Size(anc) != 8)
        {
        PyErr_Format(PyExc_ValueError, "%s", "RTC date/time must have 8 members");
        return NULL;
        }
        
    PyObject *d1 = PySequence_GetItem(anc, 0);
    PyObject *d2 = PySequence_GetItem(anc, 1);
    PyObject *d3 = PySequence_GetItem(anc, 2);
    PyObject *d4 = PySequence_GetItem(anc, 3);
    PyObject *d5 = PySequence_GetItem(anc, 4);
    PyObject *d6 = PySequence_GetItem(anc, 5);
    PyObject *d7 = PySequence_GetItem(anc, 6);
    PyObject *d8 = PySequence_GetItem(anc, 7);
            
    struct rtc_wkalrm wake_ala;

    wake_ala.enabled = PyInt_AsLong(d1);
    wake_ala.pending = PyInt_AsLong(d2);
    wake_ala.time.tm_year = PyInt_AsLong(d3) - 1900;
    wake_ala.time.tm_mon  = PyInt_AsLong(d4) - 1;
    wake_ala.time.tm_mday = PyInt_AsLong(d5);
    wake_ala.time.tm_hour = PyInt_AsLong(d6);
    wake_ala.time.tm_min  = PyInt_AsLong(d7);
    wake_ala.time.tm_sec  = PyInt_AsLong(d8);
    
    printf("Write wake: %04d/%02d/%02d %02d:%02d:%02d\n",
                wake_ala.time.tm_year + 1900,
                wake_ala.time.tm_mon + 1, 
                wake_ala.time.tm_mday, 
                wake_ala.time.tm_hour, 
                wake_ala.time.tm_min,
                wake_ala.time.tm_sec);
    
    //int fd = open(def_rtc, O_RDWR);
    int fd = open(def_rtc, O_RDONLY);
    if (fd ==  -1) 
        {
        PyErr_Format(PyExc_ValueError, "%s", "Cannot open RTC device");
        return NULL;
        }
    
    int retval = ioctl(fd, RTC_WKALM_SET, &wake_ala);
    if (retval == -1) {
        close(fd);
        PyErr_Format(PyExc_IOError, "%s", "Cannot write to RTC device");
        return NULL;
        }
    //printf("Called RTC write date\n"); 
    close(fd);
    return Py_BuildValue("");
}

static PyObject *_wtime(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = {"DateTime", NULL };
    PyObject *anc = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "O", kwlist, &anc))
        return NULL;
        
    if (!PySequence_Check(anc))
        {
        PyErr_Format(PyExc_ValueError, "%s", "RTC date/time must be a sequence");
        return NULL;
        }
    if (PySequence_Size(anc) != 6)
        {
        PyErr_Format(PyExc_ValueError, "%s", "RTC date/time must have 6 members");
        return NULL;
        }
    PyObject *d1 = PySequence_GetItem(anc, 0);
    PyObject *d2 = PySequence_GetItem(anc, 1);
    PyObject *d3 = PySequence_GetItem(anc, 2);
    PyObject *d4 = PySequence_GetItem(anc, 3);
    PyObject *d5 = PySequence_GetItem(anc, 4);
    PyObject *d6 = PySequence_GetItem(anc, 5);
            
    /* Write the RTC time/date */
    struct rtc_time rtc_tm;
    
    rtc_tm.tm_year = PyInt_AsLong(d1) - 1900;
    rtc_tm.tm_mon  = PyInt_AsLong(d2) - 1;
    rtc_tm.tm_mday = PyInt_AsLong(d3);
    rtc_tm.tm_hour = PyInt_AsLong(d4);
    rtc_tm.tm_min  = PyInt_AsLong(d5);
    rtc_tm.tm_sec  = PyInt_AsLong(d6);
    
    printf("Write time: %04d/%02d/%02d %02d:%02d:%02d\n",
                rtc_tm.tm_year + 1900,
                rtc_tm.tm_mon + 1, 
                rtc_tm.tm_mday, 
                rtc_tm.tm_hour, rtc_tm.tm_min, rtc_tm.tm_sec);
    
    //int fd = open(def_rtc, O_RDWR);
    int fd = open(def_rtc, O_RDONLY);
    if (fd ==  -1) 
        {
        PyErr_Format(PyExc_ValueError, "%s", "Cannot open RTC device");
        return NULL;
        }
    
    int retval = ioctl(fd, RTC_SET_TIME, &rtc_tm);
    if (retval == -1) {
        close(fd);
        PyErr_Format(PyExc_IOError, "%s", "Cannot write to RTC device");
        return NULL;
        }
    //printf("Called RTC write date\n"); 
    close(fd);
    return Py_BuildValue("");
}

static PyObject *_rtime(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { NULL };
    PyObject *anc = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "", kwlist, &anc))
        return NULL;

    int fd = open(def_rtc, O_RDONLY);
    if (fd ==  -1) 
        {
        PyErr_Format(PyExc_ValueError, "%s", "Cannot open RTC device");
        return NULL;
        }

     /* Read the RTC time/date */
    struct rtc_time rtc_tm;
    int retval = ioctl(fd, RTC_RD_TIME, &rtc_tm);
    if (retval == -1) {
        close(fd);
        PyErr_Format(PyExc_IOError, "%s", "Cannot read RTC device");
        return NULL;
        }
    close(fd);
    return Py_BuildValue("(IIIIII)",
        rtc_tm.tm_year + 1900,
        rtc_tm.tm_mon + 1, 
        rtc_tm.tm_mday, 
        rtc_tm.tm_hour, rtc_tm.tm_min, rtc_tm.tm_sec);
}

static PyObject *_rwake(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { NULL };
    PyObject *anc = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "", kwlist, &anc))
        return NULL;

    int fd = open(def_rtc, O_RDONLY);
    if (fd ==  -1) 
        {
        PyErr_Format(PyExc_ValueError, "%s", "Cannot open RTC device");
        return NULL;
        }

    struct rtc_wkalrm wake_ala;
    
    int retval = ioctl(fd, RTC_WKALM_RD, &wake_ala);
    if (retval == -1) {
        close(fd);
        PyErr_Format(PyExc_IOError, "%s", "Cannot read RTC device");
        return NULL;
        }
    close(fd);
    
    return Py_BuildValue("(IIIIIIII)",
        wake_ala.enabled,
        wake_ala.pending,
        wake_ala.time.tm_year + 1900,
        wake_ala.time.tm_mon + 1, 
        wake_ala.time.tm_mday, 
        wake_ala.time.tm_hour, 
        wake_ala.time.tm_min, 
        wake_ala.time.tm_sec);
}

static PyObject *_ralarm(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { NULL };
    PyObject *anc = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "", kwlist, &anc))
        return NULL;

    int fd = open(def_rtc, O_RDONLY);
    if (fd ==  -1) 
        {
        PyErr_Format(PyExc_ValueError, "%s", "Cannot open RTC device");
        return NULL;
        }

     /* Read the RTC time/date */
    struct rtc_time rtc_tm;
    int retval = ioctl(fd, RTC_ALM_READ, &rtc_tm);
    if (retval == -1) {
        close(fd);
        PyErr_Format(PyExc_IOError, "%s", "Cannot read RTC device");
        return NULL;
        }
    close(fd);
    return Py_BuildValue("(IIIIII)",
        rtc_tm.tm_year + 1900,
        rtc_tm.tm_mon + 1, 
        rtc_tm.tm_mday, 
        rtc_tm.tm_hour, rtc_tm.tm_min, rtc_tm.tm_sec);
}

static PyObject *_alarm(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { "OnOff", NULL };
    //PyObject *anc = 0;
    int anc = FALSE;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "b", kwlist, &anc))
        return NULL;
        
    int fd = open(def_rtc, O_RDONLY);
    if (fd ==  -1) 
        {
        PyErr_Format(PyExc_ValueError, "%s", "Cannot open RTC device");
        return NULL;
        }

    int retval = 0;
    if(anc)
        retval = ioctl(fd, RTC_AIE_ON, 0);
    else
        retval = ioctl(fd, RTC_AIE_OFF, 0);
    
    if (retval == -1) {
        close(fd);
        PyErr_Format(PyExc_IOError, "%s", "Cannot read RTC device");
        return NULL;
        }
    close(fd);
    return Py_BuildValue("b", anc);
}

static PyObject *_rtimestr(PyObject *self, PyObject *args, PyObject *kwargs)
{
    static char *kwlist[] = { NULL };
    PyObject *anc = 0;
    
    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "", kwlist, &anc))
        return NULL;

    int fd = open(def_rtc, O_RDONLY);
    if (fd ==  -1) 
        {
        PyErr_Format(PyExc_ValueError, "%s", "Cannot open RTC device");
        return NULL;
        }

     /* Read the RTC time/date */
    struct rtc_time rtc_tm;
    int retval = ioctl(fd, RTC_RD_TIME, &rtc_tm);
    if (retval == -1) {
        close(fd);
        PyErr_Format(PyExc_IOError, "%s", "Cannot read RTC device");
        return NULL;
        }

    close(fd);
    char buff[100];
    sprintf(buff, "%04d/%02d/%02d %02d:%02d:%02d",
                rtc_tm.tm_year + 1900,
                rtc_tm.tm_mon + 1, 
                rtc_tm.tm_mday, 
                rtc_tm.tm_hour, rtc_tm.tm_min, rtc_tm.tm_sec);
                
    return Py_BuildValue("s", buff);
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

PyMethodDef rtc_functions[] = 
    {
    { "version",   (PyCFunction)_version, METH_VARARGS|METH_KEYWORDS, "RTC interface version."},
    { "bdate",     (PyCFunction)_bdate,   METH_VARARGS|METH_KEYWORDS, "Print build date"},
    
    { "rtime",     (PyCFunction)_rtime,  METH_VARARGS|METH_KEYWORDS,  "Read RTC Time. (YYYY, MM, DD, HH, MM, SS"},
    { "rtimestr",  (PyCFunction)_rtimestr,  METH_VARARGS|METH_KEYWORDS,  "Read RTC Time as string. (YYYY, MM, DD, HH, MM, SS"},
    { "wtime",     (PyCFunction)_wtime,  METH_VARARGS|METH_KEYWORDS,  "Set RTC Time. (YYYY, MM, DD, HH, MM, SS"},
    { "ralarm",    (PyCFunction)_ralarm,  METH_VARARGS|METH_KEYWORDS,  "Read RTC Alarm. (YYYY, MM, DD, HH, MM, SS"},
    { "walarm",    (PyCFunction)_walarm,  METH_VARARGS|METH_KEYWORDS,  "Write RTC Alarm. (YYYY, MM, DD, HH, MM, SS"},
    { "alarm",     (PyCFunction)_alarm,  METH_VARARGS|METH_KEYWORDS,   "Turn alarm on / off. (YYYY, MM, DD, HH, MM, SS"},
    
    { "rwake",     (PyCFunction)_rwake,  METH_VARARGS|METH_KEYWORDS,   "Read Wake Alarm. (enabled, pending, YYYY, MM, DD, HH, MM, SS"},
    { "wwake",     (PyCFunction)_wwake,  METH_VARARGS|METH_KEYWORDS,   "Read Wake Alarm. (enabled, pending, YYYY, MM, DD, HH, MM, SS"},
    {  NULL },
    };

// -----------------------------------------------------------------------
// Init:

DL_EXPORT(void) 
initrtc(void)
{
    init_pygobject ();
    char *hhh = "RTC (Real Time Clock) Interface for the PC or compatibles.\n"
                "Functions:     rtime     -   Read RTC date / time\n"
                "               stimestr  -   Read RTC date / time as string\n"
                "               wtime     -   Write RTC date / time\n"
                "               ralarm    -   Read Alarm date / time\n"
                "Date format:   yyyy/MMM/ddd hh:mm:ss (decreasing time units)\n"
                ;

    module = Py_InitModule3("rtc", rtc_functions, hhh);
    //d = PyModule_GetDict (module);
    
    // Constants
    PyModule_AddIntConstant(module, (char *)"READ_RTC", READ_RTC);
    PyModule_AddStringConstant(module, (char *)"author", "Peter Glen");

    // Values:
    PyModule_AddObject(module, "verbose",   Py_BuildValue("i", 0));

    if (PyErr_Occurred ()) {       
	   Py_FatalError ("can't initialise RTC module");
    }
}


