from distutils.core import setup, Extension

module1 = Extension('imgrec',
                    sources = ['imgrec.c'])

setup (name = 'imgrec',
       version = '1.0',
       description = 'Image recognition for python',
       ext_modules = [module1])

