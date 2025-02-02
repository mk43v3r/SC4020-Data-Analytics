from cdbw import CDbw
from collections import defaultdict
from itertools import product
from sklearn.cluster import HDBSCAN
from sklearn.datasets import make_blobs

import matplotlib.pyplot as plt
import numpy as np
import random

# Attempt to tame the randomness generation for the libraries
# Note that this won't fix all problems
def fix_randomness(seed):
    random.seed(seed)
    np.random.seed(seed)


# Experiment 1A
# Handpicked clusters
def generate_experiment1a_blobs():
    blob_list = list([
        # Cleanly separated clusters  
        make_blobs(1000, 2, random_state=3),

        # Cleanly separated but slightly non-circular clusters
        make_blobs(1000, 2, random_state=7),

        # Slight overlapping of clusters
        make_blobs(1000, 2, random_state=2),

        # Major overlapping of 2 clusters
        make_blobs(1000, 2, random_state=5),

        # Relatively cleanly separted clusters
        make_blobs(1000, 2, centers=7, random_state=10),

        # Major overlapping between 3 clusters
        make_blobs(1000, 2, centers=7, random_state=1),

        # Very messy
        make_blobs(1000, 2, centers=10, random_state=1)
    ])

    return blob_list


# Experiment 1B
# Vary these factors: # of samples, # of clusters, density of clusters
def generate_experiment1b_blobs(seed, sample_sizes, cluster_counts, n):

    # cluster size = 3, center_box = (-1.0, 1.0) fixed
    ss_blob_dict = defaultdict(list)
    for i, ss in product(range(n), sample_sizes):
        seed = seed + i
        ss_blob_dict[ss].append(
            make_blobs(
                n_samples=ss,
                centers=3,
                random_state=seed
            )
        )

    # sample size = 2048 fixed (I dont want this to be too samll because
    # there might only be ~ 10 points per clusters)
    cc_blob_dict = defaultdict(list)
    for i, cc in product(range(n), cluster_counts):
        seed = seed + i
        cc_blob_dict[cc].append(
            make_blobs(
                n_samples=2048,
                centers=cc,
                # center_box have to be expanded because a lot of the clusters overlap
                # and might lead to unfair evaluation
                center_box = (-100.0, 100.0),
                random_state=seed
            )
        )
    
    return ss_blob_dict, cc_blob_dict


# Plot multiple plots from multiple blobs
def plot_blob_data(blob_list):
    dim_dict = {
        1: (1,1),
        2: (1,2),
        3: (2,2),
        4: (2,2),
        5: (2,3),
        6: (2,3),
        7: (3,3),
        8: (3,3),
        9: (3,3),
        10: (3,4)
    }
    bl_len = len(blob_list)
    dim = dim_dict[bl_len]

    fig, axs = plt.subplots(*dim)

    for i,(a, b) in enumerate(product(range(dim[0]), range(dim[1]))):
        if i >= bl_len:
            break

        blob_data = blob_list[i]
        xs, ys = zip(*blob_data[0])
        labels = list(blob_data[1])

        axs[a][b].scatter(x=xs, y=ys, c=labels)
        
    plt.show()


# Returns normalized arr (by column)
def z_scale_np_array(arr):
    copied_arr = arr.copy()
    z_scale_col = lambda c: (c-np.mean(c))/np.std(c)
    return np.apply_along_axis(z_scale_col, axis=0, arr=copied_arr)


def plot_without_noise(xs, ys, cs, **kwargs):
    # array without noise
    xs, ys, cs = zip(*filter(
        lambda e: e[2] != -1,
        zip(xs, ys, cs)
    ))

    plt.scatter(xs, ys, c=cs, **kwargs)

    plt.show()

# HDB tuning will be based on min_cluster_size, min_samples
def hdb_tuning_with_cdbw(arr, arr_scaled, min_cluster_sizes, min_samples):
    xs, ys = zip(*arr)
    pred_w_score = list()
    
    for mcs, ms in product(min_cluster_sizes, min_samples):
        hdb = HDBSCAN(min_cluster_size=mcs, min_samples=ms)
        arr_predictions = hdb.fit_predict(arr_scaled)
        cdbw_score = CDbw(arr, arr_predictions)
        pred_w_score.append((cdbw_score, arr_predictions, mcs, ms))

    return max(pred_w_score, key = lambda x: x[0])
        