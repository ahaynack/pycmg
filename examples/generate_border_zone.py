# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:10:36 2022

@author: ga67hah
"""

# Generate border zone

import numpy as np

mesostructure = np.load('ab2_mesostructure.npy')

j = -1
check_0 = False

next_layer_list = []
slice_original = mesostructure[0,:,:]

while check_0 == False: 
    # #slice_new = mesostructure[j,:,:]
    # def generate_next_layer(slice_original, slice_new):
    #     def new_value(x):
    #         if x == 1:
    #             x = 1
    #         else:
    #             x = 0
    #         return x
        
    #     slice_output = 2*slice_original - slice_new
    #     slice_output[slice_output < 0] = 0
    #     slice_output[slice_output > 1] = 0
        
    #     return slice_output
    
    # #next_layer = generate_next_layer(slice_original, slice_new)
    
    # new next layer
    slice_new = slice_original
    def generate_next_layer(slice_new):
        def aggr_clusters(data, stepsize=0):
            x = np.split(data, np.where(np.diff(data) != stepsize)[0]+1)
            for i, v in enumerate(x):
                if np.mean(v) > 0:
                    v_copy = v.copy()
                    v_copy[0] = 0
                    v_copy[-1] = 0
                    x[i] = v_copy
            x = np.concatenate(x, axis=0)
            return x
        
        clusters_axis_0 = np.apply_along_axis(aggr_clusters, 0, slice_new)
        clusters_axis_1 = np.apply_along_axis(aggr_clusters, 1, slice_new)
        
        cluster_diff = 2*clusters_axis_0 - clusters_axis_1
        cluster_diff[cluster_diff < 0] = 0
        cluster_diff[cluster_diff > 1] = 0
        
        return cluster_diff
    
    next_layer = generate_next_layer(slice_new)
    
    next_layer_list.append(next_layer)
    slice_original = next_layer
    
    check_0 = np.array_equal(next_layer, np.zeros_like(next_layer))
    j -= 1

boarder_zone = np.flip(np.array(next_layer_list), axis=0)

new_mesostructure = np.concatenate((boarder_zone, mesostructure))


# Ratio matrix / aggregates
axis_1 = 1
axis_2 = 2
axis_len_1 = np.size(new_mesostructure, axis_1)
axis_len_2 = np.size(new_mesostructure, axis_2)
ratio = np.apply_over_axes(np.sum, new_mesostructure, [axis_1,axis_2])
ratio = ratio.flatten() / (axis_len_1*axis_len_2)
#ratio = 1 - ratio


###
import open3d as o3d
z,x,y = new_mesostructure.nonzero()
# z,x,y = np.where(new_mesostructure == 0)
xyz = np.stack((x,y,z), axis=1)

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(xyz)

origin = o3d.geometry.TriangleMesh.create_coordinate_frame()
o3d.visualization.draw_geometries([pcd, origin],
                                  zoom=1,
                                  front=[0.9288, -0.2951, -0.2242],
                                  lookat=[1.6784, 2.0612, 1.4451],
                                  up=[-0.3402, -0.9189, -0.1996])




