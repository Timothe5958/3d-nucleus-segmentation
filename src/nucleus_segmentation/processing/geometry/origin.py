import numpy as np
from sklearn.linear_model import LinearRegression

from .alignement import find_groove_bottoms


def find_axis_origin(aligned_data):
    """
    Returns a choosen origin coordinates of the algined data.

    Note
    ----
    This origin is choosen to be (z0, x0, 0) with z0 defined the
    linear regression z(y) = a * y + b evaluated in y_center = (y_min - y_max) / 2

    """
    groove_bottoms = find_groove_bottoms(aligned_data)
    z = groove_bottoms[:, 0]
    x = groove_bottoms[:, 1]
    y = groove_bottoms[:, 2]

    y = y.reshape(-1, 1)

    z_model = LinearRegression().fit(y, z)
    x_model = LinearRegression().fit(y, x)

    y_center = (y.min() + y.max()) / 2

    z0 = z_model.predict([[y_center]])[0]
    x0 = x_model.predict([[y_center]])[0]

    return np.array([z0, x0, 0])
