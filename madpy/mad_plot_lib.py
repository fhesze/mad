#!/usr/bin/env python3

''' libary of Python functions for plotting MAD data'''

#from mad_functions import get_type_a_field
#from mad_functions import get_meas_pos
#from mad_functions import get_imported_data_field
#from mad_functions import get_grid_field
    
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata 

import time
from datetime import datetime

from madpy import *

## -- new function ------------------------------------------------------------
#

def plot_srf( SpaceConfig, field_data ):
    '''Plotting Type A field '''
    
    col_num = SpaceConfig['x_num']
    row_num = SpaceConfig['y_num']
    
    x_ireg = field_data[0,:]
    y_ireg = field_data[1,:]
#    z_ireg = field[2,:]
    
    x_reg = np.linspace(x_ireg.min(), x_ireg.max(), col_num)
    y_reg = np.linspace(y_ireg.min(), y_ireg.max(), row_num)
    
    XI, YI = np.meshgrid(x_reg, y_reg)  
    UI = griddata(x_ireg, y_ireg, field_data[3,:], XI, YI)   
        
    fig, ax = plt.subplots()
    im = ax.contourf(XI, YI, UI)
    fig.colorbar(im)
    plt.axes().set_aspect('equal', 'datalim')
    plt.axis('equal')
    plt.title('SRF with mean = ' + str(np.mean(field_data[3,:])))
    
## -- new function ------------------------------------------------------------
#

def plot_type_a_field( SpaceConfig ):
    '''Plotting Type A field '''
    
    field = get_type_a_field( SpaceConfig )
    
    col_num = SpaceConfig['x_num']
    row_num = SpaceConfig['y_num']
    
    x_ireg = field[0,:]
    y_ireg = field[1,:]
#    z_ireg = field[2,:]
    
    x_reg = np.linspace(x_ireg.min(), x_ireg.max(), col_num)
    y_reg = np.linspace(y_ireg.min(), y_ireg.max(), row_num)
    
    XI, YI = np.meshgrid(x_reg, y_reg)  
    UI = griddata(x_ireg, y_ireg, field[3,:], XI, YI)   
        
    fig, ax = plt.subplots()
    im = ax.contourf(XI, YI, UI)
    fig.colorbar(im)
    plt.axes().set_aspect('equal', 'datalim')
    plt.axis('equal')
    plt.title('SRF with mean = ' + str(np.mean(field[3,:])))

## -- new function ------------------------------------------------------------
#    
    
def plot_contour_field( field_type ):
    '''Plotting data field '''
    
    field = get_imported_data_field( field_type );
    grid_field = get_grid_field( );  
    
    col_num = 100
    row_num = 100
    
    x_ireg = grid_field[:,0]
    y_ireg = grid_field[:,1]
#    z_ireg = grid_field[:,2]
    
    x_reg = np.linspace(x_ireg.min(), x_ireg.max(), col_num)
    y_reg = np.linspace(y_ireg.min(), y_ireg.max(), row_num)
    
    XI, YI = np.meshgrid(x_reg, y_reg)  
    UI = griddata(x_ireg, y_ireg, field, XI, YI)   
        
    fig, ax = plt.subplots()
    im = ax.contourf(XI, YI, UI)
    fig.colorbar(im)
    plt.axes().set_aspect('equal', 'datalim')
#    plt.axis('equal')

## -- new function ------------------------------------------------------------
# 
    
def plot_surface_field( field_type ):
    '''surface plot of the data of the model'''
    
#    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    
    field = get_imported_data_field( field_type );
    grid_field = get_grid_field( );  
    
    col_num = 100
    row_num = 100
    
    x_ireg = grid_field[:,0]
    y_ireg = grid_field[:,1]
#    z_ireg = grid_field[:,2]
    
    x_reg = np.linspace(x_ireg.min(), x_ireg.max(), col_num)
    y_reg = np.linspace(y_ireg.min(), y_ireg.max(), row_num)
    
    XI, YI = np.meshgrid(x_reg, y_reg)  
    UI = griddata(x_ireg, y_ireg, field, XI, YI)  
    
    ## plotting data ----------------------------------------------------------
    #
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(XI, YI, UI, rstride=1, cstride=1, cmap=cm.jet)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
#    ax.set_zlabel('head')
#    plt.axes().set_aspect('equal', 'datalim')
    
#    fig, ax = plt.subplots()
#    im = ax.contourf(x_i, y_i, z_i)
#    plt.figure()    
#    plt.contour(data_matrix[1,:,1:9])
#    fig.colorbar(im)
#    plt.show()
    
    #print(u)
    
## -- new function ------------------------------------------------------------
#     
    
def plot_time_series(  ):
    '''plotting type b time series'''
    
    path = '../data/type_b/'
    
    file_name_array = []
    t = []
    time_series = []
    
    time_series_in = 4
    
    f_id = open(path + 'type_b_data.txt', 'r')
    
    for line in f_id:
        if line.startswith('name'):
            continue
        else:
            line = line.splitlines()
            line = line[0].replace(' ', '')
            line = line.split('\t')
            file_name_array.append( line[5] )
            
    f_id.close( )
    
    f_id = open(path + file_name_array[time_series_in - 1], 'r')
    
    for line in f_id:
        if line.startswith('date'):
            continue
        else:
            line = line.splitlines()
            line = line[0].replace(' ', '')
            line = line.split('\t')
            t.append( line[0] )
            time_series.append( line[1] )
            
    f_id.close( )
    
#    t1 = t[0].timetuple( )
#    print(time.mktime(t1))
    
    plt.plot( time_series )
    plt.show( )
    