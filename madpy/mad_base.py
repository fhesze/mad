
#import os
import sys
import numpy as np

from madpy.mad_functions import get_nearest_neighb
from madpy.mad_functions import find_element
from madpy.mad_functions import find_pos
from madpy.mad_functions import gen_time_data

class MAD(object):
    
    """
    MAD Base class 

    History
    -------
    Written,  FH, Aug 2015    
    
    """
	
    def __init__(self, task_root, task_id, dim_no = 2):
        
        '''
        Input
        ----------
        '''
        
        self.task_root = task_root
        self.task_id = task_id
        self.dim_no = dim_no
        
        self.eov = '\t'
        self.eol = '\n'
        self.mesh_type = 'structured'
        
        self.Type_A = {}
        self.Type_B = {}
        self.Anchor = {}
    
    def set_mesh(self, pos_array):
        
        self.pos_array = pos_array        
        self.x = pos_array[:,0]
        self.y = pos_array[:,1]
        self.z = pos_array[:,2]
        
        self.pos_no = len(self.x)
        
    def set_time(self, **TimeConfig):
        
        self.Time = TimeConfig
        if TimeConfig['t_step'] > 1:
            self.Time['type'] = 'transient'
            self.Time['t'] = gen_time_data( TimeConfig )
        elif TimeConfig['t_step'] == 1:
            self.Time['type'] = 'steady-state'
    
    def set_srf(self, srf ):
        
        self.srf = srf 
        
    def set_typa_a_field(self, type_a_field ):
        
        self.Type_A_field = type_a_field
        
    def set_fm(self, model = 'ogs', lib_path = None,
               type_a = None, type_b = None):
        
        sys.path.append( lib_path )
        
        if model == 'ogs':
            from ogspy import OGS
            OGS_Config = {'task_root' : self.task_root + 'fm_cfg/',
                          'task_id'   : 'fm',
                          'dim_no'    : self.dim_no}
            self.fm = OGS(**OGS_Config)
        elif model == 'modflow':
            print(model)
            
#    def fm_run(self, bin_path):
#        self.fm.run_model( bin_path )
        
    def fm_import_data(self, data_i):
        
        f_path = self.task_root + 'fm_cfg/' + 'fm_time_point' + str(data_i + 1) + '.tec'
#        if self.dat_type == 'TECPLOT':
#            f_path += '.tec'
#        elif self.dat_type == 'VTK':
#            f_path += '.vtk'

        with open(f_path) as f_id:
            lines = f_id.readlines()
            f_id.close()
    
        line_no = len(lines)
#        self.t = np.zeros((line_no - 3))
        fm_data = np.zeros((line_no - 3))
    
        for line_i in range(3,line_no):
            line = lines[line_i]
            line = line.split()
#            self.t[line_i - 3] = line[0]
            fm_data[line_i - 3] = line[1]
        return fm_data
        
    def gen_data(self, DataConfig):
        
        data_no = len(DataConfig['x'])
        data_type = DataConfig['type']
        
        if data_type == 'type_a':
            self.Type_A['data_no'] = data_no
        elif data_type == 'type_b':
            self.Type_B['data_no'] = data_no
        elif data_type == 'anchor':
            self.Anchor['data_no'] = data_no
        
        x = get_nearest_neighb(DataConfig['x'], self.x)
        y = get_nearest_neighb(DataConfig['y'], self.y)
        z = get_nearest_neighb(DataConfig['z'], self.z)
        
        for data_i in range(0, data_no):
            tmp = {}
            tmp['x'] = x[data_i]
            tmp['y'] = y[data_i]
            tmp['z'] = z[data_i]            
            tmp['pos'] = find_element( np.array([x[data_i], y[data_i], z[data_i]]), self.pos_array )[0]
            if self.mesh_type == 'structured':
                tmp['col'] = find_pos( x[data_i], self.x )
                tmp['row'] = find_pos( y[data_i], self.y )
                tmp['lay'] = find_pos( z[data_i], self.z )
#            tmp['srf'] = self.srf[tmp['pos']]
            if (data_type == 'type_a') or (data_type == 'anchor'):
                tmp['value'] = self.Type_A_field[tmp['pos']]
#                tmp['value'] = np.exp( self.srf[tmp['pos']] )
            elif data_type == 'type_b':
                if self.Time['type'] == 'steady-state':
                    tmp['value'] = np.exp( self.srf[tmp['pos']] )
                elif self.Time['type'] == 'transient':
#                    tmp['value'] = 'type_b_' + str(data_i + 1) + '.txt'
                    tmp['value'] = self.fm_import_data(data_i)
                    
            tmp['name'] = data_type + '_' + str(data_i + 1)
            
            if data_type == 'type_a':
                self.Type_A[str(data_i)] = tmp
            elif data_type == 'type_b':
                self.Type_B[str(data_i)] = tmp
            elif data_type == 'anchor':
                self.Anchor[str(data_i)] = tmp
        self.write_data(data_type)
        
    def write_data(self, data_type):
        
        output_header = 'col' + self.eov + 'row' + self.eov + 'layer'    
    
        if data_type == 'type_a': 
            DataConfig = self.Type_A
            output_f_name = self.task_root + '/data/type_a/type_a_data.txt'
            output_header = 'name' +  self.eov + output_header
            output_header+= self.eov + 'value'
        elif data_type == 'type_b':
            DataConfig = self.Type_B
            output_f_name = self.task_root + '/data/type_b/type_b_data.txt'
            output_header = 'name' +  self.eov + output_header
            output_header+= self.eov + 'error'+ self.eov + 'value'
        elif data_type == 'anchor':
            DataConfig = self.Anchor
            output_f_name = self.task_root + '/data/anchors/anchor_data.txt'
            output_header+= self.eov + 'value'
        data_no = DataConfig['data_no']
            
        # writing header into output file
        output_f = open(output_f_name, 'w')    
        output_f.write(output_header + self.eol)
        output_f.close()

        # writing steady-state numerical values into output files
        output_f = open(output_f_name, "a")
        
        f_str = ''
        for data_i in range(0, data_no):
            if (data_type == 'type_a') or (data_type == 'type_b'):
                f_str+= DataConfig[str(data_i)]['name'] + self.eov
            f_str+= str(DataConfig[str(data_i)]['col']) + self.eov
            f_str+= str(DataConfig[str(data_i)]['row']) + self.eov
            f_str+= str(DataConfig[str(data_i)]['lay']) + self.eov
            if data_type == 'type_b':
                f_str+= str(0.001) + self.eov   
            if (data_type == 'type_b') and self.Time['type'] == 'transient':
                f_str+= 'type_b_' + str(data_i + 1) + '.txt'
            else:
                f_str+= str(round(float(DataConfig[str(data_i)]['value']), 10))
            f_str+= self.eol
            
        output_f.write(f_str)
        output_f.close()
        
        # writing time-dependent numerical values into output files
        if (data_type == 'type_b') and self.Time['type'] == 'transient':
            for data_i in range(0, data_no):
                
                output_f_name = self.task_root + 'data/type_b/type_b_'
                output_header = 'date' + self.eov + 'value'
            
                output_f = open(output_f_name + str(data_i + 1) + '.txt', 'w')    
                output_f.write(output_header + self.eol)
                output_f.close()
            
                output_f = open(output_f_name + str(data_i + 1) + '.txt', 'a')
            
                time_series = self.Type_B[str(data_i)]['value']          
                
                f_str = ''
                for t_i in range(0, self.Time['t_no']):
                    f_str+= str(self.Time['t'][t_i]) + self.eov
                    f_str+= str(round(float(time_series[t_i]), 8))
                    if t_i < self.Time['t_no']:
                        f_str+= self.eol
                output_f.write( f_str )                
                output_f.close()
#                print(f_str)
            
        