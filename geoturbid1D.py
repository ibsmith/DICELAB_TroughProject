# GEOTURBID
#
# Shallow-Water code for turbidity currents
# based on Parker et al 4-eq model
# two-dimensional, single turbid layer, second-order version
#
# Prepared by Benoit Spinewine (spinewine@gmail.com)

# field.x might be position, and not distance

# initialisation:
import math
import numpy as np
import os
from createFluxY import createFluxY
from deepCopier import deep_copy

import init1D
from initMonterrey import initMonterrey
import initpar
from bc_1D import bc_1D
from fieldplot import fieldplot
from fluxLHLL import fluxLHLL
from gradientVL import gradientVL
from hyperbolic import hyperbolic
from mirror import mirror
from relax import relax
from fieldIO import stringify_field, parse_field
from tag2str import tag2str
from timestep import timestep

import matplotlib.pyplot as plt

titleCounter = 0

dispflag = 0
t_end = 3600*1000
dt_output = 3600
n = 200
o = 1
geostaticflag = 0
par = initpar
# field = init1D.field(n, par) # input file
field = initMonterrey(n, par)
# field_0 = field
field_0 = initMonterrey(n, par)
# field_prev = field
field_prev = initMonterrey(n, par)

# disk output and screen display parameters
# t0 = (par.h0/par.g)^0.5;]
t_output = np.arange(0, t_end + dt_output, dt_output)
i_output = 1

# main loop:
firstTimeStep = 1
# continue previous run
# load field_202;
# i_output = 203;
# firstTimeStep = 0;
iter = 1
flux_x = None


while field.t < t_end:          # Loops from begginning of field to end (usually 0-101)

    if np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1)))):

        dt = timestep(field, par)           # timestep evaluation
        if firstTimeStep:
            dt = min(dt, 0.1)           
            firstTimeStep = 0
        # disp(['t = ' num2str(field.t) ' [sec]']); # time display
    # empty outflowing pit
    field.z_b[field.z_r == - 1000] = field.z_r[field.z_r == - 1000]
    field.z_m[field.z_r == - 1000] = field.z_r[field.z_r == - 1000]

    field.u[field.z_r == - 1000] = 0
    field.v[field.z_r == - 1000] = 0
    field.c_m[field.z_r == - 1000] = 0
    field.k_m[field.z_r == - 1000] = 0
    


    # screen display:
    if np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1)))):
        if dispflag == 1:
            print('im in the insane if')
            fieldplot(field, field_0, field_prev, par, dt)
            #            pause;
    
    # disk output:
    if np.logical_and((np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1))))),
                      (np.logical_and((i_output <= len(t_output)), ((field.t + dt) > t_output[i_output])))):
        # eval(np.array(['save field_', tag2str(i_output - 1), ' field field_0 field_prev dt']))
        # eval('save field_', tag2str(i_output - 1), np.array['field field_0 field_prev dt'])
        # fieldplot_2(field, field_0, field_prev, par, dt)
    
        # Generate data for the plot - Data Trimming for graphs
        field.x[field.z_b == 1000] = np.nan
        field.x[field.z_b == -1000] = np.nan

        x1 = field.x[0]
        y1 = field_0.z_b[0]
        x2 = field.x[0]
        y2 = field.z_b[0]
        x3 = field.x[0]
        y3 = field.z_m[0]

        # Create the plot
        # -------------------------------------------------     FLOW PROFILE GRAPH       ------------------------------------------------- #
        plt.plot(x1, y1, color=(0.7, 0.7, 0.7))
        plt.plot(x2, y2, color='r')
        plt.plot(x3, y3, color='b')
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.xlabel('field.x (m)')
        plt.ylabel('(m)')
        title = 'flow profile, t = ' + str(math.floor(field.t/3600))
        plt.title(title)
        # Save the plot as a PNG image
        filename = "images/python/flowprofile/plot" + str(titleCounter) + ".png"
        plt.savefig(filename)
        plt.close()  # Close the figure to clear it for the next run

        # -------------------------------------------------     U and C PROFILES GRAPH       ------------------------------------------------- #


        # fig, ax1 = plt.subplots()

        # # Plot the first dataset on the left y-axis
        # ax1.plot(field.x[0], field.u[0], color='blue')
        # ax1.set_yticks([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4])
        # ax1.set_xlabel('x')
        # ax1.set_ylabel('u', color='blue')

        # # Create a secondary y-axis
        # ax2 = ax1.twinx()

        # # Plot the second dataset on the right y-axis
        # ax2.plot(field.x[0], field.c_m[0], color='red')
        # # ax2.set_yticks([0, 0.002, 0.004, 0.006, 0.008, 0.01, 0.012, 0.014, 0.016])
        # ax2.set_ylabel('c_m', color='red')

        # filename = "images/testing/plot" + str(titleCounter) + ".png"
        # plt.savefig(filename)
        # plt.close()  # Close the figure to clear it for the next run



        # U and C profiles plotting
        plt.title('U and C profiles')
        plt.plot(field.x[0], field.u[0], color='blue', label='Left Y-axis')
        plt.xlabel('field.x (m)')
        plt.ylabel('field.u (m/s)', color='blue')
        plt.tick_params(axis='y', colors='blue')
        ax2 = plt.twinx()
        ax2.plot(field.x[0], field.c_m[0], color='red', label='Right Y-axis')
        ax2.set_ylabel('field.c_m', color='red')
        ax2.tick_params(axis='y', colors='red')
        filename = "images/python/ucprofile/plot" + str(titleCounter) + ".png"
        plt.savefig(filename)
        plt.close()  # Close the figure to clear it for the next run

        
        # -------------------------------------------------     K and Fr PROFILES GRAPH       ------------------------------------------------- #

        # K and Fr profiles plotting data and making graph
        plt.title('K and Fr profiles')
        plt.plot(field.x[0], field.k_m[0], color='blue', label='Left Y-axis')
        plt.xlabel('field.x (m)')
        plt.ylabel('K (J/Kg)', color='blue')
        plt.tick_params(axis='y', colors='blue')
        ax2 = plt.twinx()
        # ("h") This equation computes the depth of the fluid layer 
        # calculates the depth of each layer ("h") by subtracting the bottom elevation ("z_b") from the midpoint elevation ("z_m").
        h = field.z_m - field.z_b
        #The Richardson number (Ri) is a dimensionless number used to predict the likelihood of turbulence within the fluid flow of these turbidity currents.
        #The ()"np.maximum") function is used to ensure that the denominator is never zero, which could lead to undefined behavior.
        Ri = par.R * par.g * field.c_m * h / np.maximum(field.u**2, (par.g * par.h_min))
        # Froude Number, perdicts the transition from supercritical (Fr>1) to subcritical(Fr<1)
        Fr = np.sqrt(1.0 / np.maximum(Ri, 1e-10))
        ax2.plot(field.x[0], Fr[0], color='red', label='Right Y-axis')
        ax2.set_ylabel('Fr', color='red')
        ax2.tick_params(axis='y', colors='red')
        filename = "images/python/kfrprofile/plot" + str(titleCounter) + ".png"
        plt.savefig(filename)
        plt.close()  # Close the figure to clear it for the next run
        
        # -------------------------------------------------     INSTANT AND CUMUL BED CHANGES GRAPH       ------------------------------------------------- #
        plt.title('Instant and cumul. bed changes')
        plot1 = (field.z_b - field_prev.z_b) / dt
        plot2 = field.z_b - field_0.z_b
        plt.plot(field.x[0], plot1[0], color='blue', label='Left Y-axis')
        plt.xlabel('field.x (m)')
        plt.ylabel('', color='blue')
        plt.tick_params(axis='y', colors='blue')
        ax2 = plt.twinx()
        ax2.plot(field.x[0], plot2[0], color='red', label='Right Y-axis')
        ax2.set_ylabel('', color='red')
        ax2.tick_params(axis='y', colors='red')
        filename = "images/python/iacbchanges/plot" + str(titleCounter) + ".png"
        plt.savefig(filename)
        plt.close()  # Close the figure to clear it for the next run
        # Writing field data to file
        filename = 'data/field' + str(titleCounter) + '.txt'
        stringify_field(filename, field)

        # Incrementing title counter
        titleCounter = titleCounter + 1
        i_output = i_output + 1
    
    # book-keeping
    field_prev = deep_copy(field, field_prev)
    # half-step relaxation operator:
    if np.logical_and((o == 2), (iter % 2 == 1)):
        field = relax(field, par, 0.5 * dt, geostaticflag)
    # extend field left and right:   
    
    field_x = mirror(field)

    # computation of in-cell gradients:
    # note: cell slopes are NOT recomputed for the second step of the predictor-corrector
    if np.logical_or((o == 1), (np.logical_and((o == 2), (iter % 2 == 1)))):
        grad_x = gradientVL(field_x, par, o)
        #        grad_y = gradientVL(field_y,par,o);
    # fluxing scheme (LHLL):

    # Original --> flux_x = fluxLHLL_2('x', field_x, grad_x, par, dt) # grad_x can be undefined but maybe we don't care?

    # WORKS(flux of H2O across the Hydraulic jump in horizontal direction of the flow)
    flux_x = fluxLHLL(field_x, grad_x, par, dt)


    # impose BC at upstream inflow section
    # WORKS
    flux_x = bc_1D(flux_x, field_x, par)

    # Original flux_y line of code    
    flux_y = createFluxY(field)

    if o == 1:
        # 1st order forward Euler:
        field = hyperbolic(field, flux_x, flux_y, par, dt)
        # relaxation operator:
        field = relax(field, par, dt, geostaticflag)
        field.t = field.t + dt

    else:
        if o == 2:
            # 2nd order predictor-corrector (Alcrudo & Garcia-Navarro 1993):
            if iter % 2 == 1:
                # book-keeping of previous field:
                # field_prev = field
                field_prev = deep_copy(field, field_prev)
                # predictor step:
                field = hyperbolic(field, flux_x, flux_y, par, 0.5 * dt)
            else:
                # corrector step:
                field = hyperbolic(field_prev, flux_x, flux_y, par, dt)
                # half-step relaxation operator:
                field = relax(field, par, 0.5 * dt, geostaticflag)
                # time update:
                field.t = field.t + dt
    
    
    iter = iter + 1
    

    # 206516
    if iter == 206516:
        break
    if titleCounter == 102:
        break
