import math

import numpy as np
from scipy import ndimage


def find_groove_bottoms(data):
    max_outside_ratio = 0.05

    _, x_dim, y_dim = data.shape
    points = []

    for y in y_dim:
        plane = data[:, y, :]

        z_min = np.where(plane)[0].min()
        z_max = z_min + 8

        x_min, x_max = x_dim//2-20, x_dim//2+20

        # default values of x_0 and y_0
        x_0, z_0, best_score = x_dim//2, z_min, -1

        for z in range(z_min, z_max):
            for x in range(x_min, x_max):

                # compute the amount of positive px outside the V shape.
                z_grid, x_grid = np.indices(plane.shape)

                line_left = z + (x_grid - x)
                line_right = z - (x_grid - x)

                outside = (z_grid <= line_left) | (z_grid <= line_right)

                outside_left = outside[:, :x]
                outside_right = outside[:, x:]

                n_outside_left = np.sum(plane[:, :x][outside_left])
                n_outside_right = np.sum(plane[:, x:][outside_right])

                # compute the amount of positive px on the left and right part of x.
                n_total_left = np.sum(plane[:, :x])
                n_total_right = np.sum(plane[:, x:])

                # the ratio between left and right should be similar for good approximation.
                if n_total_left * n_total_right == 0:
                    continue
                ratio_left = n_outside_left / n_total_left
                ratio_right = n_outside_right / n_total_right

                score = abs(ratio_left - ratio_right)

                if best_score == -1 or score > best_score:
                    x_0, z_0, best_score = x, z, score

        # adjust the z_0 value, in order to have a certain proportion of
        # pixels inside
        updated_z_0 = z_0
        for z in range(z_0, 0, -1):
            # compute the proportion of inside/outside px
            z_grid, x_grid = np.indices(plane.shape)

            line_left = z + (x_grid - x)
            line_right = z - (x_grid - x)

            outside = (z_grid <= line_left) | (z_grid <= line_right)
            n_outside, n_total = np.sum(plane[outside]), np.sum(plane)

            if n_outside * n_total == 0 or n_outside / n_total <= max_outside_ratio:
                updated_z_0 = z
                break

        points.append(updated_z_0, y, x_0)

    return np.array(points)


def find_rotation_angle(x, z):
    slope = np.polyfit(x, z, 1)[0]
    return np.arctan(slope)


def rotate(data):
    binary_data = ...
    groove_bottoms = find_groove_bottoms(data)
    phi = find_rotation_angle(groove_bottoms[:, 1], groove_bottoms[:, 0])
    rotated_data = ndimage.rotate(data, math.degrees(phi), axes=(0,1))

    binary_rotated_data = ...

