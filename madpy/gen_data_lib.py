#!/usr/bin/env python3
''' Python 3 script to generate MAD data '''

## importing modules and defining functions and parameters --------------------
# 

# importing modules
import os
import sys
import subprocess
import numpy as np
import math

if (os.name == 'posix'):
    sys.path.append( os.environ['HOME'] + '/Dropbox/MAD/lib/' )
elif (os.name == 'nt'):
    sys.path.append('/home/fhesse/Dropbox/MAD/lib/')

from madpy import *
    
# defining end-of-line and end-of-value encoding
eol = '\n'
eov = '\t'
    
## -- new function ------------------------------------------------------------
#

def gen_type_a_field( SRFConfig, SpaceConfig ):
    
    cov_output_f_name   = 'srf_cfg.R'    
    
    output_f = open(cov_output_f_name, 'w')

    output_f.write('my_cov_model=\'' + SRFConfig['cov_model'] + '\';' + eol)
    output_f.write('my_mean <- ' + str(SRFConfig['mean']) + ';' + eol)
    output_f.write('my_sill <- ' + str(SRFConfig['sill']) + ';' + eol)
    output_f.write('my_range <- ' + str(SRFConfig['range']) + ';' + eol)
    
    output_f.write('Nx <- ' + str(SpaceConfig['x_num']) + ';' + eol)
    output_f.write('Ny <- ' + str(SpaceConfig['y_num']) + ';' + eol)
    output_f.write('Nz <- ' + str(SpaceConfig['z_num']) + ';' + eol) 
    output_f.write('dx <- ' + str(SpaceConfig['dx']) + ';' + eol) 
    output_f.write('dy <- ' + str(SpaceConfig['dy']) + ';' + eol) 
    output_f.write('dz <- ' + str(SpaceConfig['dz']) + ';' + eol)   
    
    output_f.close()

    if os.name == 'posix':
        r_path = 'R'
        script_path = 'gen_type_a_field.R'
    
    elif os.name == 'nt':
        r_path = '\"C:/Program Files/R/R-3.1.0/bin/x64/R\"'
        script_root = 'C:/Users/fhesse/Dropbox/MAD/appl/matern_draw_3d_ss/'
        script_path = script_root + 'scripts/gen_type_a_field.R'
    
    cmd = r_path + ' --vanilla < ' + script_path
    subproc = subprocess.Popen(cmd, shell = True)
    subproc.wait()

## -- new function ------------------------------------------------------------
#

def gen_mad_data( DataConfig, SpaceConfig, TimeConfig ):

    
    time = TimeConfig['t'];
    
    output_header = 'col' + eov + 'row' + eov + 'layer'    
    
    if DataConfig['Type'] == 'Type_A':    
        output_f_name = '../data/type_a/type_a_data.txt'
        output_header = 'name' + eov + output_header + eov + 'value'
        data_field = get_type_a_field( SpaceConfig );
        
    elif DataConfig['Type'] == 'Type_B':
        output_f_name = '../data/type_b/type_b_data.txt'
        output_header = 'name' + eov + output_header + eov+'error'+eov+'value'
        data_field = get_imported_data_field( 'head' );
        
    elif DataConfig['Type'] == 'Anchor':
        output_f_name = '../data/anchors/anchor_data.txt'
        output_header = output_header + eov + 'value'
        data_field = get_type_a_field( SpaceConfig ); 

    ## processing data --------------------------------------------------------
    #

    x_vec = SpaceConfig['x_vec']
    y_vec = SpaceConfig['y_vec']
    z_vec = SpaceConfig['z_vec']
    
    x_pos = get_nearest_neighb(DataConfig['x_pos'], x_vec);
    y_pos = get_nearest_neighb(DataConfig['y_pos'], y_vec);
    z_pos = get_nearest_neighb(DataConfig['z_pos'], z_vec);
        
    line_pos = get_line_pos( x_pos, y_pos, z_pos );    
    meas_num = len( DataConfig['x_pos'] )

    x = sorted(set(x_vec))
    y = sorted(set(y_vec))
    z = sorted(set(z_vec))
    lay_num = len(z)
    z.reverse( )
    
    col = [ 0 ]*meas_num
    row = [ 0 ]*meas_num
    lay = [ 0 ]*meas_num
    value = [ 0.]*meas_num
    
    for meas_i in range(0, meas_num):
        
        col[meas_i] = int( x.index(x_pos[meas_i]) + 1 )
        row[meas_i] = int( y.index(y_pos[meas_i]) + 1 )
        lay[meas_i] = int( z.index(z_pos[meas_i]) + 1 )
        value[meas_i] = data_field[3, line_pos[meas_i]] 
        

    ## postprocessing, plotting and exporting data ----------------------------
    #

    # writing header into output file
    output_f = open(output_f_name, 'w')    
    output_f.write(output_header + eol)
    output_f.close()

    # writing numerical values into output files
    output_f = open(output_f_name, "a")
    
    for z_set_i in range(0, lay_num):      
        for meas_i in range(0, meas_num):
            
            index = meas_i + (z_set_i*meas_num)
            
            if (DataConfig['Type']=='Type_A') or (DataConfig['Type']=='Type_B'):
                output_name = str(int( col[meas_i] ))
                output_name = output_name + '-' + str(int( row[meas_i] ))
                output_name = output_name + '-' + str(z_set_i + 1)           
                line = output_name + eov
                line = line + str(col[index]) + eov
                
            elif DataConfig['Type'] == 'Anchor':
                line = str(col[index]) + eov

            line = line + str(row[index]) + eov
            line = line + str(lay[index]) + eov
            
            if DataConfig['Type'] == 'Type_B':
                line = line + str(0.001) + eov
                
            if (DataConfig['Type'] == 'Type_B') and (len(time) > 1):
                line = line + 'type_b_' + str(meas_i + 1) + '.txt'
            else:            
                line = line + str(round(float(value[index]), 8))
            
            output_f.write(line + eol)
            #    print(output_value)
            
    output_f.close()
    
    if (DataConfig['Type'] == 'Type_B') and (len(time) > 1):
        for meas_i in range(0, meas_num):

            output_f_name = '../data/type_b/type_b_'
            output_header = 'date' + eov + 'value'
            
            output_f = open(output_f_name + str(meas_i + 1) + '.txt', 'w')    
            output_f.write(output_header + eol)
            output_f.close()
            
            output_f = open(output_f_name + str(meas_i + 1) + '.txt', 'a')
            
            time_series = value[meas_i]            
            
            for t_i in range(0, len(time)):
                
                out_line = str(time[t_i]) + eov
                out_line = out_line + str(round(float(time_series[t_i]), 8))
                if t_i < len(time):
                    out_line = out_line + eol
                else:
                    out_line = out_line
                output_f.write(out_line)                
            
            output_f.close()
     
## -- new function ------------------------------------------------------------
#

def get_line_pos( x_pos, y_pos, z_pos ):
    
    grid_field = get_grid_field( )
    
    x_vec = grid_field[:, 0]
    y_vec = grid_field[:, 1]
    z_vec = grid_field[:, 2]
    
    line_num = len(x_pos)
    line_pos = [0.0]*line_num
    
    for line_i in range(0, line_num):
        
        tmp     = np.where(x_vec==x_pos[line_i])
        x_index = tmp[0]        
        tmp     = np.where(y_vec==y_pos[line_i])
        y_index = tmp[0]        
        tmp     = np.where(z_vec==z_pos[line_i])
        z_index = tmp[0]
        
        xy_index = np.intersect1d(x_index, y_index)  
        xyz_index = np.intersect1d(xy_index, z_index)
        line_pos[line_i] = xyz_index[0]
    
#    print(line_pos)
    
    return line_pos
    
## -- new function ------------------------------------------------------------
#
    
def gen_priors( TypeAConfig, AnchorConfig ):

    # defining relevant paths
    prior_cfg_f_name = 'prior_cfg.R'

    ## importing type_a measurements ------------------------------------------
    #
    
    meas_type = 'Type_A'
    meas_pos, meas_name, meas_value = get_meas_data(meas_type);
    meas_num = len(meas_value)

    ## exporting  type_a measurements -----------------------------------------
    #

    output_f = open(prior_cfg_f_name, 'w')

    col_cfg = 'type_a_col = c('
    row_cfg = 'type_a_row = c('
    lay_cfg = 'type_a_lay = c('
    val_cfg = 'type_a_val = c('

    for meas_i in range(0, meas_num):
    
        tmp = meas_pos[meas_i]
        col_cfg = col_cfg + str(int(tmp[0])) + ', '
        row_cfg = row_cfg + str(int(tmp[1])) + ', '
        lay_cfg = lay_cfg + str(int(tmp[2])) + ', '
        
        tmp = meas_value[meas_i]
        tmp = tmp[0]
        tmp = math.log(tmp)
        tmp = round(tmp, 5)
        val_cfg = val_cfg + str(tmp) + ', ' 

    col_cfg = col_cfg[:-2]
    row_cfg = row_cfg[:-2]
    lay_cfg = lay_cfg[:-2]
    val_cfg = val_cfg[:-2]

    output_f.write(col_cfg + ');' + eol)
    output_f.write(row_cfg + ');' + eol)
    output_f.write(lay_cfg + ');' + eol)
    output_f.write(val_cfg + ');' + eol)

    output_f.close()

    ## importing anchors ------------------------------------------------------
    #

    meas_type = 'Anchor'
    meas_pos, meas_name, meas_value = get_meas_data(meas_type);

    meas_num = len(meas_value)

    #print(meas_pos)

    ## exporting anchors ------------------------------------------------------
    #

    output_f = open(prior_cfg_f_name, 'a')

    col_cfg = 'anchor_col = c('
    row_cfg = 'anchor_row = c('
    lay_cfg = 'anchor_lay = c('
    nam_cfg = 'anchor_nam = c('

    for meas_i in range(0, meas_num):  

        tmp = meas_pos[meas_i]
        col_cfg = col_cfg + str(int(tmp[0])) + ', '
        row_cfg = row_cfg + str(int(tmp[1])) + ', '
        lay_cfg = lay_cfg + str(int(tmp[2])) + ', '
        nam_cfg = nam_cfg + '\'Anchor-('+ str(int(tmp[0]))+','+str(int(tmp[1]))
        nam_cfg = nam_cfg + ',' + str(int(tmp[2])) + ')' + '\' ' + ', '
    
    col_cfg = col_cfg[:-2]
    row_cfg = row_cfg[:-2]
    lay_cfg = lay_cfg[:-2]
    nam_cfg = nam_cfg[:-2]

    output_f.write(eol)
    output_f.write(col_cfg + ');' + eol)
    output_f.write(row_cfg + ');' + eol)
    output_f.write(lay_cfg + ');' + eol)
    output_f.write(nam_cfg + ');' + eol)
   
    output_f.close()

    ## processing data ------------------------------------------------------------
    #

    if os.name == 'posix':
        r_path = 'R --vanilla <'
        script_path = 'gen_priors.R'
        
    elif os.name == 'nt':
        r_path = '\"C:/Program Files/R/R-3.1.0/bin/x64/R\" --vanilla < '
        script_root = 'C:/Users/fhesse/Dropbox/MAD/appl/matern_draw_3d_ss/scripts/'
        script_path = script_root + 'gen_priors.R'
    
    cmd     = r_path + script_path
    subproc = subprocess.Popen(cmd, shell = True) 
    
    subproc.wait()
    