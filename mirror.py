import numpy as np
from init1D import field
from weedmark_ext import weedmark_ext


# CLEAN UP WHEN FUNCTIONAL
class newfield:
    x = 0
    y = 0
    z_m = 0
    c_m = 0
    k_m = 0
    z_b = 0
    z_r = 0
    u = 0
    v = 0


# this is absolutely shagged :)
def mirror(field_x):
    # MIRROR extend field left and right using mirror symmetry
    m, n = field_x.x.shape
    dx = field_x.x[0, 1] - field_x.x[0, 0]

    # newfield.x = np.array([field_x.x[0, 0]-dx, field_x.x, field_x.x[0, n-1]+dx], dtype=object)
    newfield.x = weedmark_ext(field_x.x)

    # newfield.y = np.array([field.y[0, 0], field.y, field.y[:, n - 1]], dtype=object)
    newfield.y = weedmark_ext(field_x.y)

    # newfield.z_m = np.array([field.z_m[0, 0], field.z_m, field.z_m[:, n - 1]], dtype=object)
    newfield.z_m = weedmark_ext(field_x.z_m)
    # field.z_m values aren't right so newfield.z_m values aren't right

    # newfield.c_m = np.array([field.c_m[0, 0], field.c_m, field.c_m[:, n - 1]], dtype=object)
    newfield.c_m = weedmark_ext(field_x.c_m)

    # newfield.k_m = np.array([field.k_m[0, 0], field.k_m, field.k_m[:, n - 1]], dtype=object)
    newfield.k_m = weedmark_ext(field_x.k_m)

    # newfield.z_b = np.array([field.z_b[0, 0], field.z_b, field.z_b[:, n - 1]], dtype=object)
    newfield.z_b = weedmark_ext(field_x.z_b)

    # newfield.z_r = np.array([field.z_r[0, 0], field.z_r, field.z_r[:, n - 1]], dtype=object)
    newfield.z_r = weedmark_ext(field_x.z_r)

    # newfield.u = np.array([field.u[0, 0], field.u, field.u[:, n - 1]], dtype=object)
    newfield.u = weedmark_ext(field_x.u)

    # newfield.v = np.array([field.v[0, 0], field.v, field.v[:, n - 1]], dtype=object)
    newfield.v = weedmark_ext(field_x.v)

    #newfield.z_r, newfield.u, newfield.v = weedmark_ext(field_x.zr), weedmark_ext(field_x.u), weedmark_ext(field_x.v)
    return newfield