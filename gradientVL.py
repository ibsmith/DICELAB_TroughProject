import numpy as np

from init1D import field
from weedmark_ext import weedmark_ext


class grad:
    dh_m = np.zeros((field.x.shape[0], field.x.shape[1]))
    dmu = np.zeros((field.x.shape[0], field.x.shape[1]))
    dkh = np.zeros((field.x.shape[0], field.x.shape[1]))
    dz_b = np.zeros((field.x.shape[0], field.x.shape[1]))
    dqx_m = np.zeros((field.x.shape[0], field.x.shape[1]))
    dqy_m = np.zeros((field.x.shape[0], field.x.shape[1]))


def minmod(a, b):
    ab = np.multiply(a, b)
    c = np.multiply(ab > 0, (np.multiply(abs(a) < abs(b), a) + np.multiply(~(abs(a) < abs(b)), b)))
    return c


def gradientVL(field=None, par=None, o=None):
    o = 0
    if o == 1:
        dh_m = grad.dh_m
        dmu = grad.dmu
        dkh = grad.dkh
        dz_b = grad.dz_b
        dqx_m = grad.dqx_m
        dqy_m = grad.dqy_m
    else:
        m, n = field.x.shape
        # obtain gradient variables:
        h_m = field.z_m - field.z_b
        z_b = field.z_b
        qx_m = np.multiply(h_m, field.u)
        qy_m = np.multiply(h_m, field.v)
        mu = np.multiply(h_m, field.c_m)
        kh = np.multiply(h_m, field.k_m)
        # extend variables left and right:
        # h_me = np.array([h_m[:, 0], h_m, h_m[:, n]])
        h_me = weedmark_ext(h_m)
        # mu_e = np.array([mu[:, 1], mu, mu[:, n]])
        mu_e = weedmark_ext(mu)
        # kh_e = np.array([kh[:, 1], kh, kh[:, n]])
        kh_e = weedmark_ext(kh)
        # z_be = np.array([z_b[:, 1], z_b, z_b[:, n]])
        z_be = weedmark_ext(z_b)
        # qx_me = np.array([qx_m[:, 1], qx_m, qx_m[:, n]])
        qx_me = weedmark_ext(qx_m)
        # qy_me = np.array([qy_m[:, 1], qy_m, qy_m[:, n]])
        qy_me = weedmark_ext(qy_m)
        # matrix multiplication
        grad.dh_m = minmod(h_me[:, np.arange(2, n + 2)] - h_me[:, np.arange(1, n + 1)],
                           h_me[:, np.arange(1, n + 1)] - h_me[:, np.arange(0, n)])
        grad.dmu = minmod(mu_e[:, np.arange(2, n + 2)] - mu_e[:, np.arange(1, n + 1)],
                          mu_e[:, np.arange(1, n + 1)] - mu_e[:, np.arange(0, n)])
        grad.dkh = minmod(kh_e[:, np.arange(2, n + 2)] - kh_e[:, np.arange(1, n + 1)],
                          kh_e[:, np.arange(1, n + 1)] - kh_e[:, np.arange(0, n)])
        grad.dz_b = minmod(z_be[:, np.arange(2, n + 2)] - z_be[:, np.arange(1, n + 1)],
                           z_be[:, np.arange(1, n + 1)] - z_be[:, np.arange(0, n)])
        grad.dqx_m = minmod(qx_me[:, np.arange(2, n + 2)] - qx_me[:, np.arange(1, n + 1)],
                            qx_me[:, np.arange(1, n + 1)] - qx_me[:, np.arange(0, n)])
        grad.dqy_m = minmod(qy_me[:, np.arange(2, n + 2)] - qy_me[:, np.arange(1, n + 1)],
                            qy_me[:, np.arange(1, n + 1)] - qy_me[:, np.arange(0, n)])

    return grad