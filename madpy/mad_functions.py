#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' selection of Python functions for usage with MAD '''

import numpy as np

## -- new function ------------------------------------------------------------
# 

def get_meas_pos( data_type ):
    '''Getting the position and names of the measurements'''
    
    f_path = '../cfg/meas_pos.txt'
    pos_f = open(f_path, 'r')
    
    pos_lines = pos_f.readlines()
    pos_lines = [x.replace('\n', '') for x in pos_lines]
    pos_lines.pop(0) 
    
    n = len(pos_lines) - 1
    for line in reversed(pos_lines):
        line = line.split(',')
        if not data_type in line[1]:
            del pos_lines[n]
        n = n - 1
#    print(line) 
    
    meas_name = []
    meas_num = len(pos_lines)
    meas_pos = np.zeros((meas_num, 3))
    for n in range(0, meas_num ):
        pos_line = pos_lines[n]
        pos_line = pos_line.replace(' ', '')
        pos_line = pos_line.split(',')
        
        meas_pos[:][n] = pos_line[2:5] 
        meas_name.append(pos_line[0])
    
    pos_f.close() 
    

    return meas_pos;
    
## -- new function ------------------------------------------------------------
# 

def get_meas_data( data_type ):
    '''Getting the position, names and values of the measurements'''

    if data_type == 'Type_A':    
        f_path = '../data/type_a/type_a_data.txt'
        line_begin = 1
        line_end = 4        
        value_line_num = 4
    elif data_type == 'Type_B':
        f_path = '../data/type_b/type_b_data.txt'
        line_begin = 1
        line_end = 4   
        value_line_num = 5
    elif data_type == 'Anchor':
        f_path = '../data/anchors/anchor_data.txt'
        line_begin = 0
        line_end = 3   
        value_line_num = 3
    
    f = open(f_path, 'r')
    
    lines = f.readlines()
    lines = [x.replace('\n', '') for x in lines]  
    lines.pop(0)  
    
#    print(lines)
    
    meas_name = []
    meas_num = len(lines)
    meas_pos = np.zeros((meas_num, 3))
    meas_value = np.zeros((meas_num, 1))

    for n in range(0, meas_num ):
        line = lines[n]
        line = line.replace(' ', '')
        line = line.split('\t')
        
        meas_pos[:][n] = line[line_begin:line_end]
        meas_value[n] = line[value_line_num]
        meas_name.append(line[0])
    
    f.close()  
    
#     print(meas_pos)
    return meas_pos, meas_name, meas_value;

## -- new function ------------------------------------------------------------
#     
    
def get_grid_data( ):
    '''Getting the grid configurations of the model'''
    
    f_name     = '../cfg/grid.txt'
    grid_data = []
    f =  open(f_name, 'r')  
    
    for line in f:
        if line.startswith('#'):
            continue
        else:
            line = line.splitlines()
            line = line[0].replace(' ', '')
            line = line.split('=')
#            print(line[1])
            grid_data.append(int(line[1]))
    
    f.close()
    
    Nx = grid_data[0:3]
    dx = grid_data[3:6]
    
    return Nx, dx;

## -- new function ------------------------------------------------------------
#     

def get_type_a_field( SpaceConfig ):
    '''getting the the full amount of type_a data, i.e. the whole field'''

    pos_num = SpaceConfig['x_num']*SpaceConfig['y_num']
    type_a_field_data = np.zeros( (4, pos_num) )    
    f_name    = '../data/type_a_field/type_a_field.txt'    

    # reading numerical data from input file
    pos_i = 0
    with open(f_name, 'r') as f:
        header_line = f.readline()
        for line_i in f:
            tmp = line_i.replace('\n', '')
            tmp = tmp.split('\t')
            type_a_field_data[0, pos_i] = tmp[0]
            type_a_field_data[1, pos_i] = tmp[1]
            type_a_field_data[2, pos_i] = tmp[2]
            type_a_field_data[3, pos_i] = tmp[3]
            pos_i = pos_i + 1
    
    f.close()

    return type_a_field_data;  
    
## -- new function ------------------------------------------------------------
#       
    
def get_type_b_field( f_name ):
    '''getting the full amount of type-b data, i.e. the whole field'''
    
    f = open(f_name, 'r')
    lines = f.readlines()    
    f.close()

    return lines;
            
## -- new function ------------------------------------------------------------
#     

#def get_imported_data_field( field_type ):
#    '''getting the full amount of imported data, i.e. the whole field'''
#    
#    if field_type == 'conductivity':
#        f_name      = '../data/type_a_field/conductivity.txt'
#        
#    elif field_type == 'log_conductivity':
#        f_name      = '../data/type_a_field/log_conductivity.txt'
#          
#    elif field_type == 'head':
#        f_name      = '../data/type_b_field/head.txt'  
#        
#
#    # reading numerical data from input file
#    with open(f_name) as f:
#        lines = (line for line in f if not line.startswith('#'))
#        type_a_field = np.loadtxt(lines, delimiter='\t', skiprows=0)
#    
#    f.close()
#
#    return type_a_field;

## -- new function ------------------------------------------------------------
#     

#def get_imported_type_b_field( field_type ):
#    '''getting the formated full amount of Type B data, i.e. the whole field'''
#    
#    import numpy as np
#    
#    f_name    = '../data/type_b_field/head.txt'    
#
#    # reading numerical data from input file
#    with open(f_name) as f:
#        lines = (line for line in f if not line.startswith('#'))
#        type_b_field = np.loadtxt(lines, delimiter='\t', skiprows=0)
#    
#    f.close()
#
#    return type_b_field;
   
    
## -- new function ------------------------------------------------------------
#       
    
#def get_grid_field( ):
#    '''getting the full amount of grid data'''
#    
#    import numpy as np
#    
#    f_name = '../data/grid/grid_field.txt'    
#    
#        # reading numerical data from input file
#    with open(f_name) as f:
#        lines = (line for line in f if not line.startswith('#'))
#        grid_field = np.loadtxt(lines, delimiter='\t', skiprows=0)
#  
#    f.close()
#
#    return grid_field;
      
## -- new function ------------------------------------------------------------
#       
#    
#def get_block_field( ):
#    '''getting the full amount of grid data'''
#    
#    import numpy as np
#    
#    f_name = '../data/grid/block_field.txt'    
#    
#        # reading numerical data from input file
#    with open(f_name) as f:
#        lines = (line for line in f if not line.startswith('#'))
#        grid_field = np.loadtxt(lines, delimiter='\t', skiprows=0)
#  
#    f.close()
#
#    return grid_field;
    
## -- new function ------------------------------------------------------------
#       
    
#def get_prior_data( data_type ):
#    '''Getting the prior data from the prior file'''
#    
#    f_name = '../data/priors/priors.txt'
#    
#    f = open(f_name, 'r')
#    lines = f.readlines()    
#    f.close()
#    
#    sample_num = len(lines)
#    data = [None]*(sample_num - 1)
#    
#    header_line = lines[0]
#    header_line = header_line.splitlines()
#    header_line = header_line[0].replace(' ', '')
#    header_line = header_line.split(';')
#    
#    for i, j in enumerate(header_line  ):
#        if j == data_type:
#            data_index = i 
#    
#    for sample_i in range(1, sample_num):
#        
#        data_line = lines[sample_i]
#        data_line = data_line.splitlines()
#        data_line = data_line[0].replace(' ', '')
#        data_line = data_line.split(';')
#        
#        data[sample_i - 1] = data_line[data_index]
#        
#    
##    print(sample_num)
##    print(len(data))
#
#    return data;
    
## -- new function ------------------------------------------------------------
#
    
def get_nearest_neighb(meas_pos, x):
    
    x_neighb = [0]*len(meas_pos)
    
    x = list(set(x))
    x = sorted(x)
    
    for i in range(0, len(meas_pos)):
        index = min(range(len(x)), key = lambda n: abs(x[n] - meas_pos[i]))
        x_neighb[i] = x[index]
    
    return x_neighb

## -- new function ------------------------------------------------------------
#

def find_element( pos, numpy_array ):
    
#    grid_field = get_grid_field( )
    
    x_vec = numpy_array[:, 0]
    x_pos = pos[0]
    y_vec = numpy_array[:, 1]
    y_pos = pos[1]
    z_vec = numpy_array[:, 2]
    z_pos = pos[2]

    line_num = 1
    line_pos = [0.0]*line_num
    
    for line_i in range(0, line_num):
        
        tmp     = np.where(x_vec==x_pos)
        x_index = tmp[0]        
        tmp     = np.where(y_vec==y_pos)
        y_index = tmp[0]        
        tmp     = np.where(z_vec==z_pos)
        z_index = tmp[0]
        
        xy_index = np.intersect1d(x_index, y_index)  
        xyz_index = np.intersect1d(xy_index, z_index)
        line_pos[line_i] = xyz_index[0]
    
    return line_pos
    
## -- new function ------------------------------------------------------------
#

def find_pos( value, numpy_array ):
    value_set = sorted(set( numpy_array ))
    tmp =  np.where( value_set==value )[0] + 1
    return tmp[0]

## -- new function ------------------------------------------------------------
#     
    
def gen_time_data( TimeConfig ):    
    '''Generating the time data of the model'''
     
    import datetime
    
    dt = int( TimeConfig['t_step'] )
    t_num = int( TimeConfig['t_no'] )
    t_a = TimeConfig['date_start']
    t = []
    
    if TimeConfig['format'] == 'date':
        start_date = datetime.date(t_a[0], t_a[1], t_a[2])
    elif TimeConfig['format'] == 'datetime':
        start_date = datetime.datetime(t_a[0], t_a[1], t_a[2])
    
    current_date = start_date        
    for t_i in range(0, t_num):
        t.append( str(current_date) )
        current_date += datetime.timedelta(seconds=dt)
    
    return t
    