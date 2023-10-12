import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def generate_flowprofile(field, field_0, titleCounter):
        '''Function generates the flow profile graph to predetermined directory. Change directory in this method directly'''

        x1 = field.x[0]
        y1 = field_0.z_b[0]
        x2 = field.x[0]
        y2 = field.z_b[0]
        x3 = field.x[0]
        y3 = field.z_m[0]

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



def generate_iacbchanges(field, field_prev, field_0, dt, titleCounter):
    '''Function generates the instant and cumulative bed changes graph to predetermined directory. Change directory in this method directly'''

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



def generate_kfrprofile(field, par, titleCounter):
    '''Function generates the K and Fr profiles graph to predetermined directory. Change directory in this method directly'''

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



def generate_ucprofile(field, titleCounter):
    '''Function generates the U and C profiles graph to predetermined directory. Change directory in this method directly'''

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