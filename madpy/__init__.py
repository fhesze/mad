#!/usr/bin/env python
"""
    MAD Python Utilities

    Package offers miscellaneous functions and sub-modules in different 
    categories.

    Get help on each function by typing
    >>> import mad_python
    >>> help(mad_python.function)

    Provided functions and modules (alphabetic w/o obsolete functions)
    ------------------------------------------------------------------
    get_variogram               returns variogram function


    Provided functions and modules per category
    -------------------------------------------
        Ascii files
        Data processing
        Date & Time
        Miscellaneous
        Models
        Plotting
        SQLite
    -------------------------------------------


    Ascii files
    -----------
    


    Data processing
    ---------------
    gen_mad_data            generating the different data types for MAD

    
    Date & Time
    -----------
    get_time                getting the time vector.


    Miscellaneous
    -------------
  


    Models
    ------
    


    Plotting
    --------
    plot_type_a_field       plotting the whole type a field


    SQLite
    -------------
   


    License
    -------

    This file is part of the MAD Python package.

    Not all files in the package are free software. The license is given in the
    'License' section of the docstring of each routine.

    There are 3 possibilities:
    1. The routine is not yet released under the GNU Lesser General Public License.
       This is marked by a text such as
            This file is part of the MAD Python package.

            It is NOT released under the GNU Lesser General Public License, yet.

            Copyright 2014-2015 Falk He"sse
       If you want to use this routine for publication or similar, please 
       contact the author for possible co-authorship.

    2. The routine is already released under the GNU Lesser General Public 
       License but if you use the routine in a publication or similar, you have
       to cite the respective publication

    3. The routine is released under the GNU Lesser General Public License. The
       following applies: The MAD Python package is free software: you can 
       redistribute it and/or modify it under the terms of the GNU Lesser 
       General Public License as published by the Free Software Foundation, 
       either version 3 of the License, or (at your option) any later version.

       The MAD Python package is distributed in the hope that it will be useful,
       but WITHOUT ANY WARRANTY; without even the implied warranty of
       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
       GNU Lesser General Public License for more details.

       You should have received a copy of the GNU Lesser General Public License
       along with the UFZ makefile project (cf. gpl.txt and lgpl.txt).
       If not, see <http://www.gnu.org/licenses/>.

    Copyright 2014-2015 Falk He"sse


    History
    -------
    Written,  FH,   Dec 2014
    Modified, FH,   Mar 2015 - check_grid_data
                    Apr 2015 - get_variogram
                    Aug 2015 - reworked with class structure

"""
#from __future__ import print_function

# Routines

from .mad_base import MAD

#from .mad_functions import get_meas_pos
#from .mad_functions import get_meas_data
from .mad_functions import gen_time_data
#from .mad_functions import gen_domain_data
#from .mad_functions import get_grid_data
#from .mad_functions import get_grid_field
#from .mad_functions import get_block_field
#from .mad_functions import get_type_a_field
#from .mad_functions import get_imported_data_field
from .mad_functions import find_element
from .mad_functions import find_pos
from .mad_functions import get_nearest_neighb

#from .mad_import_export_lib import import_type_a_field
#from .mad_import_export_lib import export_type_a_field
#from .mad_import_export_lib import import_type_b_field
#from .mad_import_export_lib import import_grid_field
#from .mad_import_export_lib import export_grid_data

#from .gen_data_lib import gen_type_a_field
#from .gen_data_lib import gen_mad_data
#from .gen_data_lib import gen_priors

#from .mad_plot_lib import plot_time_series
#from .mad_plot_lib import plot_type_a_field
#from .mad_plot_lib import plot_srf
#from .mad_plot_lib import plot_contour_field
#from .mad_plot_lib import plot_surface_field
#from .mad_plot_lib import plot_measurements

#from .check_grid_data import check_grid_data
#from .get_variogram import get_variogram
#from .estim_variogram import estim_variogram
#from .gen_srf import gen_srf

# Information
__author__   = 'Falk Hesse'
__version__  = '0.1.0'
#__revision__ = 
__date__     = 'Date: 01.04.2015'

# Main
#if __name__ == '__main__':
#    print('\nMAD Python Package.')
#    print("Version {:s} from {:s}.".format(__version__,__date__))
#    print('\nThis is the README file. See als the license file LICENSE.\n\n')
#    f = open('README','r')
#    for line in f: print(line,end='')
#    f.close()
