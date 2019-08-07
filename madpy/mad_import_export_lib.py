#!/usr/bin/env python3
''' Python 3 script for exporting and importing MAD data '''

## importing modules and defining functions and parameters --------------------
# 

# importing modules
import numpy as np

from madpy import *
#from mad_functions import get_meas_pos
#from mad_functions import get_grid_data
#from mad_functions import get_time_data
#from mad_functions import get_nearest_neighb
#from mad_functions import get_type_a_field
#from mad_functions import get_type_b_field

eol = '\n'
eov = '\t'

## -- new function ------------------------------------------------------------
# 

def import_grid_field():
    
    f_name_01   = '../data/grid/grid_field.txt'
    f_name_02   = '../data/grid/block_field.txt'
    
    # defining end-of-line and end-of-value encoding
    eol = '\n'
    
    matrix      = get_type_a_field( );
    
    matrix_shape= matrix.shape

    x_vec       = matrix[0:(matrix_shape[0]), 0]
    y_vec       = matrix[0:(matrix_shape[0]), 1]
    z_vec       = matrix[0:(matrix_shape[0]), 3]
    
    col_vec     = matrix[0:(matrix_shape[0]), 4]
    row_vec     = matrix[0:(matrix_shape[0]), 5]
    lay_vec     = matrix[0:(matrix_shape[0]), 7]

    
    output_f    = open(f_name_01, 'w')

    for n in range(0, len(x_vec)):
        
        output_line = str( x_vec[n] ) + eov
        output_line = output_line + str( y_vec[n] ) + eov
        output_line = output_line + str( z_vec[n] )
        output_f.write( output_line + eol)

    output_f.close()
    
    output_f    = open(f_name_02, 'w')

    for n in range(0, len(col_vec)):
        
        output_line = str( col_vec[n] ) + eov
        output_line = output_line + str( row_vec[n] ) + eov
        output_line = output_line + str( lay_vec[n] )
        output_f.write( output_line + eol)

    output_f.close()

## -- new function ------------------------------------------------------------
#  

def import_type_a_field( field_type ):
     
    # defining end-of-line and end-of-value encoding
    eol = '\n'
        
    matrix      = get_type_a_field( );
    matrix_shape= matrix.shape    
    
    if field_type == 'conductivity':
        f_name      = '../data/type_a_field/conductivity.txt'
        data_vec    = matrix[0:(matrix_shape[0]), 8]
        
    elif field_type == 'log_conductivity':
        f_name      = '../data/type_a_field/log_conductivity.txt'
        data_vec    = matrix[0:(matrix_shape[0]), 9]

    output_f    = open(f_name, 'w')

    for n in range(0, len(data_vec)):
        output_f.write( str(data_vec[n]) + eol)

    output_f.close() 
    
## -- new function ------------------------------------------------------------
# 
    
def export_type_a_field( fm ):
    
    eol         = '\n'
    
    if fm == 'modflow':
        f_name      = '../data/type_a_field/type_a_field_modflow.txt'
    elif fm == 'ogs':
        f_name      = '../data/type_a_field/type_a_field_ogs.txt'
    
    matrix      = get_type_a_field( ); 
    matrix_shape= matrix.shape
    
    x_vec       = matrix[0:(matrix_shape[0]), 0]
    y_vec       = matrix[0:(matrix_shape[0]), 2]
    z_vec       = matrix[0:(matrix_shape[0]), 3]
    
    K_vec       = matrix[0:(matrix_shape[0]), 8]
#    Y_vec       = matrix[0:(matrix_shape[0]), 9]
    
    output_f    = open(f_name, 'w')
    
    for n in range(0, len(x_vec)):
        
        v_1 = str( x_vec[n] ) + eov
        v_2 = str( y_vec[n] ) + eov 
        v_3 = str((z_vec[n] + 0.5) ) + eov
        v_4 = str((z_vec[n] - 0.5) ) + eov
        v_5 = str( K_vec[n] )
        
        output_f.write( v_1 + v_2 + v_3 + v_4 + v_5 + eol )
    
    output_f.close()
    
## -- new function ------------------------------------------------------------
#  

def import_type_b_field( FmConfig, SpaceConfig, TimeConfig ):
    
    # importing modules
    import math

    # defining relevant paths
    input_f_name    = '../fm_cfg/fm.fhd'
    head_f_name     = '../data/type_b_field/' + FmConfig['type_b'] + '.txt'

    header_line_num = []
    nlines          = 0

    # search string
    search_str      = 'HEAD'

    ## importing data ---------------------------------------------------------
    #
    
    input_lines = get_type_b_field( input_f_name );
    time        = TimeConfig['time'];

    x_num       = SpaceConfig['x_num']
    y_num       = SpaceConfig['y_num']
    z_num       = SpaceConfig['z_num']
    pos_num     = x_num*y_num*z_num
    t_num       = len(time)
    l_num       = int(math.ceil(x_num/10))

    #print(l_num)

    ## processing data --------------------------------------------------------
    #

    data_matrix = np.zeros( (x_num, y_num, z_num) )
    data_vec    = np.zeros( (pos_num, t_num) )
    pos_vec     = get_pos_vec( SpaceConfig )

    # getting linenumbers of headerlines
    for line in input_lines:
        nlines += 1
        if search_str in line:
            header_line_num.append(int(nlines))            
    header_line_num.append(int(len(input_lines) + 1))
    
    for t_i in range(0, t_num):
        
        z_i = 0
        y_i = y_num - 1
        # getting data per time step
        for line in range(header_line_num[t_i], header_line_num[t_i+1] - 1, l_num):
                
            retrieved_line = []
            for n in range(0, l_num):
                my_line = input_lines[line + n].split('  ')
                my_line.pop(0)
                retrieved_line = retrieved_line + my_line
        
            retrieved_line = [x.replace(' ', '') for x in retrieved_line]
            retrieved_line = [x.replace('\n', '') for x in retrieved_line]
            retrieved_line = [x.replace('\r', '') for x in retrieved_line]
        
            for x_i in range(0, x_num):
                data_matrix[x_i, y_i, z_i] = retrieved_line[x_i]
                
                # getting rid of non-active modflow data
                if data_matrix[x_i, y_i, z_i] == -2e+20:
                    data_matrix[x_i, y_i, z_i] = 0.0
                          
            y_i = y_i - 1
          
        pos_i = 0
        for x_i in range(0, x_num):
            for y_i in range(0, y_num):
                for z_i in range(0, z_num):
                    data_vec[pos_i, t_i] = data_matrix[x_i, y_i, z_i]
                    pos_i = pos_i + 1
    
   
   # writing numerical values into output files
    output_f = open(head_f_name, 'w')
    
    output_line = 'x' + eov + 'y' + eov + 'z' + eov
    for t_i in range(0, t_num):
#        output_line = output_line + time[t_i] + eov
        output_line = output_line + 't_' + str(t_i) + eov
    output_f.write(output_line + eol)
    
    for pos_i in range(0, pos_num):  
        
        output_line = str( pos_vec[pos_i, 0] ) + eov
        output_line = output_line + str( pos_vec[pos_i, 1] ) + eov
        output_line = output_line + str( pos_vec[pos_i, 2] ) + eov
        output_line = output_line + str(data_vec[pos_i, t_i]) + eov

        for t_i in range(1, t_num - 1):
            output_line = output_line + str(data_vec[pos_i, t_i]) + eov
            
        output_line = output_line + str(data_vec[pos_i, t_num - 1])
        output_f.write(output_line + eol)

    output_f.close()
    
## -- new function ------------------------------------------------------------
# 

def get_pos_vec( SpaceConfig ):

    x_num       = SpaceConfig['x_num']
    y_num       = SpaceConfig['y_num']
    z_num       = SpaceConfig['z_num']
    pos_num     = x_num*y_num*z_num
    
    pos_vec     = np.zeros( (pos_num, 3) )
    
    pos_i = 0
    for x_i in range(0, x_num):
            for y_i in range(0, y_num):
                for z_i in range(0, z_num):
                    
                    pos_vec[pos_i, 0] = x_i + 0.5
                    pos_vec[pos_i, 1] = y_i + 0.5
                    pos_vec[pos_i, 2] = - z_i - 0.5
                    pos_i = pos_i + 1
                    
    return pos_vec

## -- new function ------------------------------------------------------------
#  

def export_grid_data( ):
    
    grid_output_f_name  = '../cfg/grid.R'
    
    Nx, dx = get_grid_data( );
    
    output_f = open(grid_output_f_name, 'w')

    output_f.write('Nx <- ' + str(Nx[0]) + ';' + eol)
    output_f.write('Ny <- ' + str(Nx[1]) + ';' + eol)
    output_f.write('Nz <- ' + str(Nx[2]) + ';' + eol)
    output_f.write('dx <- ' + str(dx[0]) + ';' + eol)
    output_f.write('dy <- ' + str(dx[1]) + ';' + eol)
    output_f.write('dz <- ' + str(dx[2]) + ';' + eol)
    
    output_f.close()
    