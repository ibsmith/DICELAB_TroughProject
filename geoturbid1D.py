# GEOTURBID
#
# Shallow-Water code for turbidity currents
# based on Parker et al 4-eq model
# two-dimensional, single turbid layer, second-order version

# Prepared by Benoit Spinewine (spinewine@gmail.com)

# field.x might be position, and not distance

# Create folder with timestamp for data
# potato
import os
import time

def store_data(folder_name):
    # Create and store your images in folder_name
    pass

if __name__ == "__main__":
    folder_name = 'my_folder_' + time.strftime("%Y_%m_%d_%H_%M_%S")
    folder_data = folder_name+'/data'
    folder_videos = folder_name+'/videos'
    folder_images = folder_name+'/images'
    folder_serialized = folder_name+'/serialized'
    folder_flowprofile = folder_videos + '/flowprofile'
    folder_iacbchanges = folder_videos + '/iacbchanges'
    folder_kfrprofile = folder_videos + '/kfrprofile'
    folder_ucprofile= folder_videos + '/ucprofile'
    os.mkdir(folder_name)
    os.mkdir(folder_data)
    os.mkdir(folder_videos)
    os.mkdir(folder_images)
    os.mkdir(folder_serialized)
    os.mkdir(folder_flowprofile)
    os.mkdir(folder_iacbchanges)
    os.mkdir(folder_kfrprofile)
    os.mkdir(folder_ucprofile)
    store_data(folder_name)


#############################################################################
# initialisation:
import os
import sys
import numpy as np
from createFluxY import createFluxY
from deepCopier import deep_copy
import plotGenerator

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
from fieldIO import stringify_field, parse_field # parse_field implement later to parse in field text files
from timestep import timestep
from serializer import Serializer


#############################################################################
# User Inputs

# Gravity user input
print('Current Gravity (g): ',  initpar.g)
temp = None
while temp is None:
    try:
        temp = float(input('Enter a float for Gravity (g): '))
    except ValueError:
        print("Error: Enter a valid number!".format(temp))
initpar.g = (temp) # Makes new Gravity number 


titleCounter = 0
# Can be changed later somehow based on user's wants
plotCreationFlag = input('Do you want to generate plot images during this run? (y/n)')
if plotCreationFlag.strip().lower() == 'y':
    plotCreationFlag = True
else:
    plotCreationFlag = False

dispflag = 0
t_end = 3600*1000
dt_output = 3600
n = 200
o = 1
geostaticflag = 0
# material and numerical parameters
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

# Storing serialized field objects to folder
# Creates folder if it DNE
if not os.path.isdir('./serialized'):
    os.mkdir('./serialized')

while field.t < t_end:          # Loops from begginning of field to end (usually 0-101)

    print(f'Iteration: {iter}')

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
    
        # ---------------------------------------     Plots/Graphs and data file generation       --------------------------------------- #
        # Generate data for the plot - Data Trimming for graphs
        # For graph generation. I just don't want to outsource it as I am not sure if its pass by reference or by value
        field.x[field.z_b == 1000] = np.nan
        field.x[field.z_b == -1000] = np.nan

        if plotCreationFlag:

            # filename will be grabbed during each run once unique folder is created
            # Remove/change later
            # TODO set this variable to point to the folder, to be done later by anyone
            filename = ''

            plotGenerator.generate_flowprofile(field, field_0, filename + 'flowprofile/plot' + str(titleCounter) + '.png')
            plotGenerator.generate_ucprofile(field, filename + 'ucprofile/plot' + str(titleCounter) + '.png')
            plotGenerator.generate_kfrprofile(field, par, filename + 'kfrprofile/plot' + str(titleCounter) + '.png')
            plotGenerator.generate_iacbchanges(field, field_prev, field_0, dt, filename + 'iacbchanges/plot' + str(titleCounter) + '.png')
        
        # Writing field data to file
        filename = 'data/field' + str(titleCounter) + '.txt'
        # Output to data files
        stringify_field(filename, field)

        # Serialize data and store to file
        # Makes life easier when you want to read in the field objects later
        # serializer.encode(titleCounter, field, field_0, field_prev, par)
        serializerObj = Serializer(field=field, field_0=field_0, field_prev=field_prev, par=par, dt=dt)
        serializerObj.encode(serializerObj, titleCounter)
        returnedObj = serializerObj.decode('serialized/field0.txt')
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

    # (magnitude of sediment flux across the Hydraulic jump in the horizontal direction of the flow)
    flux_x = fluxLHLL(field_x, grad_x, par, dt)


    # impose BC at upstream inflow section
    # WORKS
    flux_x = bc_1D(flux_x, field_x, par)

    # Original flux_y line of code    
    flux_y = createFluxY(field)
    
    #hyperbolic operator:
    if o == 1:
        # 1st order forward Euler:
        field = hyperbolic(field, flux_x, flux_y, par, dt)
        # relaxation operator:
        field = relax(field, par, dt, geostaticflag)
        # time update
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

