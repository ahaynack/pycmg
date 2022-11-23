# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 10:10:36 2022

@author: ga67hah
"""

# Generate border zone

import numpy as np
import copy
from scipy import ndimage
import open3d as o3d

mesostructure = np.load('ab2_new_2_mesostructure.npy')

#######################################################################################################################
# OLD
j = -1
check_0 = False

next_layer_list = []
meso_diff_list = []
slice_original = mesostructure[0,:,:]

while check_0 == False: 
    # OPTION 1
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
    
    # ### Clean layer
    # check_neighbors = next_layer.nonzero()
    # u, c = np.unique(check_neighbors[0], return_counts=True)
    # dup = u[c > 1]
    # #print(dup)
    # u2, c2 = np.unique(check_neighbors[1], return_counts=True)
    # dup2 = u2[c2 > 1]
    # #print(dup2)
    
    # # if len(dup) < 1:
    # #     break
    # # if len(dup2) < 1:
    # #     break
    # ##
    
    # OPTION 2
    slice_new = next_layer #slice_original
    def generate_next_layer2(slice_new):
        def aggr_clusters(data, stepsize=0):
            x = np.split(data, np.where(np.diff(data) != stepsize)[0]+1)
            for i, v in enumerate(x):
                if np.mean(v) > 0:
                    v_copy = v.copy()
                    v_copy[0] = 0
                    v_copy[-1] = 0
                    # 1
                    if np.sum(v_copy) < 1:
                        x[i] = v_copy
                    else:
                        x[i] = v
                    # # 2
                    # x[i] = v_copy
            x = np.concatenate(x, axis=0)
            return x
        
        clusters_axis_0 = np.apply_along_axis(aggr_clusters, 0, slice_new)
        clusters_axis_1 = np.apply_along_axis(aggr_clusters, 1, slice_new)
        
        cluster_diff = 2*clusters_axis_0 - clusters_axis_1
        cluster_diff[cluster_diff < 0] = 0
        cluster_diff[cluster_diff > 1] = 0
        
        return cluster_diff
    
    next_layer = generate_next_layer2(slice_new)
    
    #if ((len(dup) > 1) and (len(dup2) > 1)):
    next_layer_list.append(next_layer)
    slice_original = next_layer
    
    # Copy from 'old' mesostructure
    meso_diff = mesostructure[j,:,:] + next_layer
    meso_diff_list.append(meso_diff)
    
    check_0 = np.array_equal(next_layer, np.zeros_like(next_layer))
    j -= 1

boarder_zone = np.flip(np.array(next_layer_list), axis=0)
meso_diff_np = np.array(meso_diff_list)
meso_diff_np_copy = meso_diff_np.copy()

def test(arr):
    if np.all(arr) == False:
        output = 1
    else:
        output = 0
    return output

iter_range = list(range(np.size(meso_diff_np, 0)))
for index, value in enumerate(iter_range):
    sdf = 0
    for ind, val in np.ndenumerate(meso_diff_np[value,:,:]):
        if val == 1:
            meso_diff_np[value,ind[0],ind[1]] = test(meso_diff_np[value:,ind[0],ind[1]])
        if val == 2:
            meso_diff_np[value,ind[0],ind[1]] = 1
        sdf += 1

meso_diff_np = np.flip(meso_diff_np, axis=0)


new_mesostructure = np.concatenate((boarder_zone, mesostructure))


# Ratio matrix / aggregates
axis_1 = 1
axis_2 = 2
axis_len_1 = np.size(new_mesostructure, axis_1)
axis_len_2 = np.size(new_mesostructure, axis_2)
ratio = np.apply_over_axes(np.sum, new_mesostructure, [axis_1,axis_2])
ratio = ratio.flatten() / (axis_len_1*axis_len_2)
#ratio = 1 - ratio

#######################################################################################################################
# # NEW
# mcr = mesostructure

# def threeDperc(mcr, H):
#     '''mcr is the microstructure matrix and H is the kernel: Function uses
#     convolution filtering to estimate the percolation from edge'''
#     p, perfrac = 1, 0
#     tempout = copy.deepcopy(mcr)
#     tempout[0, :, :] = 50

#     while abs(p - perfrac) > 0:
#         p = perfrac
#         #
#         tempout = (((tempout > 0).astype(int)) +
#                    49 * ((ndimage.convolve(tempout, H, mode='constant', cval=0.0) > 1323).astype(int)))
#         perfrac = np.mean(tempout)
#     return (tempout > 2).astype(int)


# systemSideLength = 20
# phi = 0.25

# kernel = np.array([[[0, 0, 0], [0, 1, 0], [0, 0, 0]],
#                    [[0, 1, 0], [1, 1274, 1], [0, 1, 0]],
#                    [[0, 0, 0], [0, 1, 0], [0, 0, 0]]])

# res = threeDperc(mcr, kernel)

# new_mesostructure = res


###
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




