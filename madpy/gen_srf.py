# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 21:53:11 2015

@author: fhesse
"""

import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata 

from madpy import *

def gen_srf( DomainConfig, SRFConfig ):
    
    x_vec = DomainConfig['x_vec']
    y_vec = DomainConfig['y_vec']
    u_vec = np.zeros(( len(x_vec) ))
    data_vec = np.zeros(( 4, len(x_vec) ))
    
    mode_num = 2**10
    mu = 0.0
    sigma = SRFConfig['sill']

    ksi = np.zeros(( mode_num, 2 ))
    ksi[:,0] = np.random.normal(mu, 1, mode_num)   
    ksi[:,1] = np.random.normal(mu, 1, mode_num)                                     
    nu = get_random_set( SRFConfig, mode_num )                                    
    
    for mode_i in range(0, mode_num):
            
            theta = nu[mode_i, 0]*x_vec + nu[mode_i, 1]*y_vec
            A = ksi[mode_i, 0]*np.cos(theta)
            B = ksi[mode_i, 1]*np.sin(theta)
            u_vec = u_vec + np.sqrt(1.0/mode_num)*(A + B)
    
    data_vec[0,:] = DomainConfig['x_vec']
    data_vec[1,:] = DomainConfig['y_vec']
    data_vec[2,:] = DomainConfig['z_vec']
    data_vec[3,:] = np.sqrt(sigma)*u_vec + SRFConfig['mean']

    return data_vec
    
def get_random_set( SRFConfig, mode_num ):
    
    nu = np.zeros(( mode_num, 2 ))
    gamma = np.zeros(( mode_num, 2 ))
    gamma[:,0] = np.random.uniform(0, 1, mode_num)
    gamma[:,1] = np.random.uniform(0, 1, mode_num)
    lam = SRFConfig['range']

    if  SRFConfig['cov_model'] == 'Gau':
    
        nu[:,0] = np.random.normal(0, 1, mode_num)/( 2*np.pi ) 
        nu[:,1] = np.random.normal(0, 1, mode_num)/( 2*np.pi )
        
    elif SRFConfig['cov_model'] == 'Exp':
    
        r = np.sqrt(1.0/gamma[:,0]**2 - 1);
        nu[:,0] = r*np.cos( 2*np.pi*gamma[:,1] )/lam
        nu[:,1] = r*np.sin( 2*np.pi*gamma[:,1] )/lam
    
    return nu
    