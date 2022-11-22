# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 09:10:58 2022

@author: ga67hah
"""

# Create PyCMG Input

import numpy as np
import matplotlib.pyplot as plt

# Input
aggr_original = {
    0.063: 0.000582111, 
    0.125: 0.004178891, 
    0.25: 0.18027441, 
    0.5: 0.282333085, 
    1: 0.261367809, 
    2: 0.23691915, 
    4: 0.033762434, 
    8: 0.000582111
    }

aggr_cement_ratio_original = 0.5

aggr_output_range = [0.5, 4]

global header_list
header_list = ['a', 'vf_max']

# Main
def main(aggr_original, aggr_cement_ratio_original, aggr_output_range):
    # Input dictionary ot numpy array
    aggr_np = np.array(list(aggr_original.items()))
    
    # Volume fraction of aggregates SMALLER THAN input range
    smaller_than_index = np.argwhere(aggr_np[:,0] < aggr_output_range[0])
    smaller_than_volume = np.sum(aggr_np[smaller_than_index.flatten(),1])
    
    # Volume fraction of aggregates BIGGER THAN input range
    bigger_than_index = np.argwhere(aggr_np[:,0] > aggr_output_range[1])
    bigger_than_volume = np.sum(aggr_np[bigger_than_index.flatten(),1])
    
    # Combined volume fraction
    volume_total = smaller_than_volume + bigger_than_volume
    
    # Volume fraction of output
    volume_output = round(aggr_cement_ratio_original - (aggr_cement_ratio_original * volume_total), 3)
    volume_output = np.array([volume_output])
    
    # Aggregate list output
    aggr_output_index = np.argwhere((aggr_np[:,0] >= aggr_output_range[0]) & (aggr_np[:,0] <= aggr_output_range[1]))
    aggr_output = aggr_np[aggr_output_index.flatten(),:]
    aggr_output_sum = np.sum(aggr_output[:,1])
    aggr_output = np.apply_along_axis(lambda x: np.array([x[0], x[1]/aggr_output_sum]), 1, aggr_output)
    
    # # Plot
    # plt.plot(aggr_np[:,0], aggr_np[:,1])
    # plt.plot(aggr_output[:,0], aggr_output[:,1])
    
    return aggr_output, volume_output

def create_header_list_input(header_list):
    header_list_input = ','.join(header_list)
    return header_list_input

def append_column(arr, column, header_name):
    column_axis = 0
    arr_len = np.size(arr,column_axis)
    
    column = np.full((arr_len,1), column)
    
    arr_output = np.append(arr, column, axis=1)
    header_list.append(header_name)
    
    return arr_output


test1, test2 = main(aggr_original, aggr_cement_ratio_original, aggr_output_range)

# Add coat
#test1 = append_column(test1, 'TRUE')
#header_list.append('coat')
test1 = append_column(test1, 30, 'n_cuts')
test1 = append_column(test1, 10, 't_coat')
test1 = append_column(test1, 10, 'space')

#test3 = np.append(test1, np.expand_dims(np.array([1,2,3]), axis=1), axis=1)

header_list_input = create_header_list_input(header_list)
np.savetxt('ab2_input_generated.csv', test1, fmt='%1.4f', delimiter=',', header=header_list_input, comments='')
np.savetxt('ab2_input_generated_vf_max.csv', test2, fmt='%1.4f', delimiter=',')



















