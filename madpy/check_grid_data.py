# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 21:48:33 2015

@author: fhesse
"""

def check_grid_data( DataConfig, DomainConfig ):
    
    x_vec = DomainConfig['x_vec']
    y_vec = DomainConfig['y_vec']
    z_vec = DomainConfig['z_vec']
    
    DataConfig['x_pos'] = get_nearest_neighb(DataConfig['x_pos'], x_vec)
    DataConfig['y_pos'] = get_nearest_neighb(DataConfig['y_pos'], y_vec)    
    DataConfig['z_pos'] = get_nearest_neighb(DataConfig['z_pos'], z_vec) 





def get_nearest_neighb(meas_pos, x):
    
    x_neighb = [0]*len(meas_pos)
    
    x = list(set(x))
    x = sorted(x)
    
    for i in range(0, len(meas_pos)):
        index = min(range(len(x)), key = lambda n: abs(x[n] - meas_pos[i]))
        x_neighb[i] = x[index]
    
    return x_neighb