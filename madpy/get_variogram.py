# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 21:48:33 2015

@author: fhesse
"""

import numpy as np
#import matplotlib.pyplot as plt

def get_variogram(x, SRFConfig):
    
    sill = SRFConfig['sill']
    length_scale = SRFConfig['range']
    
    if SRFConfig['cov_model'] == 'Gau':
        t = (x/length_scale)**2
        variogram = sill*( 1 - np.exp(-t) )
    elif SRFConfig['cov_model'] == 'Exp':
        t = np.abs(x/length_scale)
        variogram = sill*( 1 - np.exp(-t) ) 
    else:
        print('no valid variogram model')
    
    return variogram
    