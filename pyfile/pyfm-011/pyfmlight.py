#!/usr/bin/env python

# 3D File Manager in Python OpenGL, light helper routines
# 

#import math, sys, rand

#import gtk.gtkgl
from OpenGL.GL import *
from OpenGL.GLU import *
       
def light(self): 

    # Lighting properties.
    #light_ambient = [0.0, 0.0, 0.0, 1.0]
    #light_ambient = [1.0, 1.0, 1.0, 1.0]
    light_ambient = [0.5, 0.5, 0.5, 1.0]
    
    #light_diffuse = [0.0, 0.0, 0.0, 1.0]
    light_diffuse = [0.5, 0.5, 0.5, 1.0]
    #light_diffuse = [1.0, 1.0, 1.0, 1.0]
    
    light_specular = [.5, .5, .5, 1.0]
    #light_specular = [1.0, 1.0, 1.0, 1.0]
    #light_specular = [.2, .2, .2, 1.0]
    
    #light_position = [1.0, 1.0, 1.0, 1.0]
    #light_position = [0.0, 5.0, 5.0, 0.0]
    light_position = [0.0, 0.0, 1.0, 0.0]
    #light_position = [5.0, 5.0, 5.0, 0.0]
    
    #light_model_ambient = [0.2, 0.2, 0.2, 1.0]
    light_model_ambient = [0.5, 0.5, 0.5, 1.0]
    #light_model_ambient = [0.9, 0.9, 0.9, 1.0]
    light_local_view = 0.0
    #pos = (5.0, 5.0, 5.0, 0.0)

    # Initialise the lighting properties.
    glLightfv (GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv (GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv (GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv (GL_LIGHT0, GL_POSITION, light_position)
    #glLightModelfv (GL_LIGHT_MODEL_AMBIENT, light_model_ambient)
    #glLightModelf (GL_LIGHT_MODEL_LOCAL_VIEWER, light_local_view)

    glEnable (GL_LIGHTING)
    glEnable (GL_LIGHT0)
    glEnable (GL_DEPTH_TEST)

    glClearColor(.0, .0, .0, 1.0)
    #glClearColor(.5, .5, .5, 1.0)
    #glClearColor(1.0, 1.0, 1.0, 1.0)
    glClearDepth(1.0)



