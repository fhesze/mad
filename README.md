# mad

This is the MAD libary of the MAD Software Project

Created September 2014, Copyright 2014-2015 

The libary conists of two different packages: (i) a Python package and (ii) a R package.

Contact Falk He"sse - falk.hesze (at) gmail.com for the Python package
	Heather Savoy - heather.m.savoy (at) gmail.com for the R package

-- Python package --

The package has to be in your Python path. For example in bash:
    export PYTHONPATH=/path/to/the/mad/package
It can also be installed with the usual setup.py commands using distutils:
    python setup.py install
If one wants to use the development capabilities of setuptools, you can use something like
    python -c "import setuptools; execfile('setup.py')" develop
This basically creates an .egg-link file and updates an easy-install.pth file so that the project
is on sys.path by default.
Distutils also allows to make Windows installers with
    python setup.py bdist_wininst


The documentation of the package is in the docstring of __init__.py so that one can get help on the
Python prompt:
>>> import madpy
>>> help(madpy)

The individual functions also provide their help as doctrings.
Getting, for example, help on gen_priors for generating priors for MAD applications:
>>> import madpy
>>> help(madpy.gen_priors)

The Python package is compatible with 3 (> 3.2).

Essential third-party packages are numpy and scipy.
Some functions provide visual checks using matplotlib for plotting.

-- R package --

The R package has been updated and the most recent version can be found on CRAN as achoredDistr
