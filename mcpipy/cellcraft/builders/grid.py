import numpy as np
import pandas as pd
import math


def create_bins_from_coordinates(coor_df, theta_deg, blocksize, threshold, id_column='chain_id'):
    coordinate_columns = ['x_coord', 'y_coord', 'z_coord']
    coor_arr = coor_df[coordinate_columns].values
    coor_arr = center_coordinates(coor_arr)
    coor_arr = rotate_coordinates(coor_arr, theta_deg)
    bin_count_df = bin_coordinates(coor_df[id_column], coor_arr, blocksize, threshold)
    return bin_count_df


def center_coordinates(coordinates):
    return coordinates - coordinates.mean(axis=0)


def rotate_coordinates(coordinates, theta_deg):
    theta = np.array(theta_deg) / 360 * 2 * np.pi
    rot_mat = eulerAnglesToRotationMatrix(theta)
    coordinates = np.dot(rot_mat, coordinates.T)
    return coordinates.T


def eulerAnglesToRotationMatrix(theta):
    """
    https://www.learnopencv.com/rotation-matrix-to-euler-angles/
    """
    R_x = np.array([
        [1, 0, 0],
        [0, math.cos(theta[0]), -math.sin(theta[0])],
        [0, math.sin(theta[0]), math.cos(theta[0])]
    ])
    R_y = np.array([
        [math.cos(theta[1]), 0, math.sin(theta[1])],
        [0, 1, 0],
        [-math.sin(theta[1]), 0, math.cos(theta[1])]
    ])

    R_z = np.array([
        [math.cos(theta[2]), -math.sin(theta[2]), 0],
        [math.sin(theta[2]), math.cos(theta[2]), 0],
        [0, 0, 1]
    ])
    R = np.dot(R_z, np.dot(R_y, R_x))
    return R


def bin_coordinates(chain_id, coor_arr, blocksize, threshold):
    n_coordinates = 3
    grid_bins = [
        np.arange(coor_arr[:, i].min(), coor_arr[:, i].max() + blocksize, blocksize)
        for i in range(n_coordinates)
    ]
    bin_corr_arr = np.array(
        [np.digitize(coor_arr[:, i], grid_bins[i], right=True) for i in range(n_coordinates)]).T

    df = pd.DataFrame(bin_corr_arr, columns=['x_coord', 'y_coord', 'z_coord'], index=chain_id.index)
    df['id'] = chain_id
    df['count'] = 1

    count = df.set_index(['x_coord', 'y_coord', 'z_coord', 'id'])['count'] \
        .groupby(level=[0, 1, 2, 3]).count().sort_values()
    count = count[count > threshold]
    count = count.reset_index(level=3).groupby(level=[0, 1, 2]).first()
    bin_count_df = count.reset_index()

    return bin_count_df
