#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' selection Python functions '''
 
## -- new function ------------------------------------------------------------
# 
   
def get_row_id( cursor, table_name, search_str ):
    
    sql = 'SELECT rowid FROM ' + table_name + ' WHERE idmeasure = ?'
    cursor.execute( sql, (search_str,) )
    row_id = cursor.fetchall()
    row_id = row_id[0]
    row_id = row_id[0]
    
#    print(row_id)    
    
    return row_id
   
## -- new function ------------------------------------------------------------
# 
   
def get_row_from_table( cursor, table_name, row_id ):
    
    sql = 'SELECT * FROM ' + table_name + ' WHERE rowid = ?'
    cursor.execute( sql, (row_id,) )
    data = cursor.fetchall()
    
#    print(data)    
    
    return data
    
## -- new function ------------------------------------------------------------
# 
  
def get_meas_id( cursor, table_name, search_str ):
    
    sql = 'SELECT rowid FROM ' + table_name + ' WHERE typevar = ?'
#    print(sql)
    cursor.execute( sql, (search_str,) )
    
    meas_id = cursor.fetchall()
    
    for meas_i in range(0, len(meas_id)):
        tmp = meas_id[meas_i]
        meas_id[meas_i] = tmp[0]
    
#    print(meas_id)
    
    return meas_id
    
## -- new function ------------------------------------------------------------
#     
    
def get_column_names( cursor, table_name ):
    
    sql = 'PRAGMA table_info(' + table_name + ')'   
    cursor.execute(sql)
    field = cursor.fetchall()
    
    for i in range(len(field)):
        field[:][0] = []
       
    return field

## -- new function ------------------------------------------------------------
#     
    
def get_number_of_rows_in_table( cursor, table_name ):
    
    sql = 'SELECT COUNT(*) FROM ' + table_name   
    cursor.execute(sql)
    row_num = cursor.fetchall()
    
    print(row_num)
       
    return row_num

## -- new function ------------------------------------------------------------
#     
    
def get_row_id_array( cursor, table_name, id_name, id_value ):
    
    sql = 'SELECT * FROM ' + table_name
    sql = sql + ' WHERE ' + id_name + ' = ?'
    cursor.execute(sql, (id_value,) )
    data = cursor.fetchall()
    
    row_num = len(data)
    row_id_array = [None]*row_num
    
    for row_id in range(0, row_num):
        
        tmp = data[row_id]        
        row_id_array[row_id] = tmp[0] 

#    print(row_id_array[0])
       
    return row_id_array

   
## -- new function ------------------------------------------------------------
# 
  
def insert_row_into_table( cursor, table_name, row_arg ):
    
    sql = 'INSERT INTO ' + table_name + ' VALUES ('   
    for i in range(0, len(row_arg) - 1):
        sql = sql + '?, '  
    sql = sql + '?)'
        
    cursor.execute(sql, (row_arg))
 
## -- new function ------------------------------------------------------------
# 

def delete_some_rows_in_table( cursor, table_name, field_name, field_id ):
    
    sql = 'SELECT rowid FROM ' + table_name + ' WHERE ' + field_name + ' = ?'
    cursor.execute(sql, [field_id])
    
    row_id_array = cursor.fetchall()
    row_id_num = len(row_id_array)
    
    for row_id_i in range(0, row_id_num):
        
        tmp = row_id_array[row_id_i]
        tmp = tmp[0]
#        print(tmp)
#    row_id = row_id[0]
#    row_id = row_id[0]
    
#    print(sql)
     
        sql = 'DELETE FROM ' + table_name + ' WHERE rowid = ?'
        cursor.execute(sql, [tmp])
   
 
## -- new function ------------------------------------------------------------
# 

def delete_row_from_table( cursor, table_name, idmeasure ):
    
    sql = 'SELECT rowid FROM ' + table_name + ' WHERE idmeasure = ?'
    cursor.execute(sql, [idmeasure])
    row_id = cursor.fetchall()
    row_id = row_id[0]
    row_id = row_id[0]
    
#    print(row_id)
     
    sql = 'DELETE FROM ' + table_name + ' WHERE rowid = ?'
    cursor.execute(sql, [row_id])

## -- new function ------------------------------------------------------------
# 

def delete_all_rows_in_table( cursor, table_name ):
    
    sql = 'SELECT COUNT(*) FROM ' + table_name
    cursor.execute(sql)
    field = cursor.fetchall()
    field = field[0]
    
    for row_i in range(field[0], 0, -1):
        sql = 'DELETE FROM ' + table_name + ' WHERE rowid = ?'
        cursor.execute(sql, [row_i])
#        print(row_i)
#    
#    print(field[0])
     