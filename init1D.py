import numpy as np
from scipy.interpolate import interp1d

# INITFIELD initialise flow field
class field:
    # defines the magnitude of initial bed perturbations for each reach
    # These perturbations refer to variations in the sediment bed's elevation
    # p3 = 0 # (p3) reach 3
    # p2 = 0 # (p2) reach 2
    # p1 = 0 # (p1) reach 1
    p = [0,0,0] # p values at each reach
   # defines the lengths of the three reaches
    # L3 = 5000
    # L2 = 2500 # L2 = 6000
    # L1 = 15000 # (L1) length of reach 6000 (L1 = 6000)
    L = [15000,2500, 5000] # Array for all lengths of the three reaches
   # (Lx) computes the sum of all reach lenghts
    # Lx = L1 + L2 + L3     # Manual 
    Lx = sum(L)             # all elements in the array

    # defines the slopes of the three reaches
    # S3 = 0
    # S2 = 25 # S2 = 0.006
    # S1 = 30 # (S1) slope of reach 1 (S1 = 0.013)
    S = [30,25,0]
    # (x0) defines the starting point of the x-coordinate
    x0 = - L[0] 
    # (n) = number of cells per unit block length
    n = 200 
    # (dx) computes the grid spacing based off the sum of all reach lengths (Lx) and number of cells (n)
    dx = Lx / n; 
    dy = dx
    # (x) genrates an array of x-coordinates for the entire domain
    x = np.arange((x0 - 0.5 * dx), (x0 + Lx + 0.5 * dx) + dx, dx)
    # defines a constant y-coordinate
    y = [1]
    x = np.ones((len(y), 1)) * x
    y = np.transpose(y) * np.ones((1, x.size))
    # defines the initial y-coordinate (y0) and domain height (Ly)
    y0 = 0
    Ly = 0.5
    # initalizes arrays for the follwing flow field variabels 
    k_m = np.ones((x.shape[0], x.shape[1])) * 0 # (k_m) turbulent kinetic energy within the flow
    z_r = np.ones((x.shape[0], x.shape[1])) * - 2000 # (z_r) rigid channel bottom??
    z_b = np.ones((x.shape[0], x.shape[1])) * - 1000 # (z_b) sediment bed elevation?? 
    z_m = np.ones((x.shape[0], x.shape[1])) * - 1000 # (z_m)  elevation of the flow at a certain point??
    c_m = np.ones((x.shape[0], x.shape[1])) * 0 # (c_m) sediment concentration within the current
    v = np.zeros((x.shape[0], x.shape[1])) #  (v) vertical velocity component 
    u = np.zeros((x.shape[0], x.shape[1])) # (u) horizontal velocity component 
    # z_r[-1, -1 - 2] = -1000
    z_r[0][-3:] = -1000 # sets specific values in z_r array
    
    # defines reference points for interpolating the sediment bed elevation 
    xx = np.array([- L[0], 0, L[1], L[1] + L[2]])
    zz = np.array([L[0] * S[0], 0, - L[1] * S[1], - L[1] * S[1] - L[2] * S[2]])
    set_interp = interp1d(xx, zz, kind='linear', fill_value='extrapolate')
    z_b = set_interp(x)
    # sets specific values in z_r array
    # z_b[-1, -1 - 2] = -1000
    z_b[0][-3:] = -1000
    z_r[0][-1] = 1000
    # idientifies certain ranges within the x-coordinate for each reach
    isX1 = np.argwhere(np.logical_and((x[0] > -L[0]), (x[0] < 0)))
    isX2 = np.argwhere(np.logical_and((x[0] > 0), (x[0] < L[1])))
    isX3 = np.argwhere(np.logical_and((x[0] > L[1]), (x[0] < (L[1] + L[2]))))
    # random number generator
    randno = np.random.random()
    # pertubs and alters the sediment bed using a random number and parameters specific to each reach
    for i in isX1:
        sX1 = i[0]
        sX1 = sX1 - 1
        z_b[0, sX1] = z_b[0, sX1] + (randno * p[0] - p[0] / 2)
    for i in isX2:
        sX2 = i[0]
        sX2 = sX2 - 1
        z_b[0, sX2] = z_b[0, sX2] + (randno * p[1] - p[1] / 2)
    for i in isX3:
        sX3 = i[0]
        sX3 = sX3 - 1
        z_b[0, sX3] = z_b[0, sX3] + (randno * p[2] - p[2] / 2)
    # Ensures that z_b is >= to z_r
    z_b = np.maximum(z_b, z_r)
    # Ensures that z_b is >= to z_r
    z_m = np.maximum(z_m, z_b)
    # intializes time variable
    t = 0
    # defines initial values for flow parameters
    H_up = 60 # turbidity current depth/thickness
    C_up = 0.333 # the layer-averaged volume concentration of suspended sediment carried by the turbidity current
    U_up = 1 # flow velocity
    Q_up = H_up * U_up # the volume transport rate of suspended sediment
    K_up = 0 # # turbulent kinetic energy witihn the flow


    def __init__(self, n, par):
        # initializes flow field properties for three reaches
        # self.L1 = 6000
        # self.S1 = 30
        # self.p1 = 0
        # self.L2 = 6000
        # self.S2 = 25
        # self.p2 = 0
        # self.L3 = 5000
        # self.S3 = 0
        # self.p3 = 0
        self.L = [6000, 6000, 5000]
        self.S = [30, 25, 0]
        self.p = [0,0,0]
        # defines parameters for each reach and other flow field variables
        self.n = n
        self.par = par
        self.field = field
        self.x = field.x
        self.v = field.v
        self.u = field.u
        self.c_m = field.c_m
        self.z_b = field.z_b
        self.z_m = field.z_m
        self.k_m = field.k_m
        self.z_r = field.z_r
        self.Q_up = field.Q_up
        self.H_up = field.H_up
        self.C_up = field.C_up
        self.U_up = field.U_up
        self.K_up = field.K_up
        self.t = field.t

    def init1D(self, n, par):
        # initializes parameters and variables for 1D simulation
        # S1 = field.S1
        # S2 = field.S2
        # S3 = field.S3
        # L1 = field.L1
        # L2 = field.L2
        # L3 = field.L3
        # pert1 = field.p1
        # pert2 = field.p2
        # pert3 = field.p3
        S = field.S
        L = field.L
        pert = field.p

        # initial bed perturbations

        # upstream inflow section
        field.H_up = 60
        field.C_up = 0.0015
        field.U_up = 1
        # Ri_up = 0.8;
        # U_up = (par.R*par.g*C_up*H_up/Ri_up)^0.5;
        field.Q_up = field.H_up * field.U_up
        field.K_up = par.CfStar / par.alpha * field.U_up ** 2 # assume turbulence is fully developed at inflow
        # z-ordering condition:
        # field.z_b = np.maximum(field.z_b, field.z_r)
        # field.z_m = np.maximum(field.z_m, field.z_b)
        # velocities:
        # field.u = np.zeros((field.x.shape[0], field.x.shape[1]))
        # field.v = np.zeros((field.x.shape[0], field.x.shape[1]))
        # time:
        # -----
        field.t = 0