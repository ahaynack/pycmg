# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:10:36 2022

@author: ga67hah
"""

# Generate border zone

import numpy as np

mesostructure = np.load('mesostructure.npy')

j = -1
check_0 = False

next_layer_list = []
slice_original = mesostructure[0,:,:]

while check_0 == False: 
    slice_new = mesostructure[j,:,:]
    def generate_next_layer(slice_original, slice_new):
        def new_value(x):
            if x == 1:
                x = 1
            else:
                x = 0
            return x
        
        slice_output = 2*slice_original - slice_new
        slice_output[slice_output < 0] = 0
        slice_output[slice_output > 1] = 0
        
        return slice_output
    
    next_layer = generate_next_layer(slice_original, slice_new)
    
    ### Clean layer
    check_neighbors = next_layer.nonzero()
    u, c = np.unique(check_neighbors[0], return_counts=True)
    dup = u[c > 1]
    #print(dup)
    u2, c2 = np.unique(check_neighbors[1], return_counts=True)
    dup2 = u2[c2 > 1]
    #print(dup2)
    
    # if len(dup) < 1:
    #     break
    # if len(dup2) < 1:
    #     break
    ###
    if ((len(dup) > 0) and (len(dup2) > 0)):
        next_layer_list.append(next_layer)
    slice_original = next_layer
    
    check_0 = np.array_equal(next_layer, np.zeros_like(next_layer))
    j -= 1

boarder_zone = np.flip(np.array(next_layer_list), axis=0)

new_mesostructure = np.concatenate((boarder_zone, mesostructure))


# ###
# import open3d as o3d
# z,x,y = new_mesostructure.nonzero()
# xyz = np.stack((x,y,z), axis=1)

# pcd = o3d.geometry.PointCloud()
# pcd.points = o3d.utility.Vector3dVector(xyz)

# origin = o3d.geometry.TriangleMesh.create_coordinate_frame()
# o3d.visualization.draw_geometries([pcd, origin],
#                                   zoom=1,
#                                   front=[0.9288, -0.2951, -0.2242],
#                                   lookat=[1.6784, 2.0612, 1.4451],
#                                   up=[-0.3402, -0.9189, -0.1996])




