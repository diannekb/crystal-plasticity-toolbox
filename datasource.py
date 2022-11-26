from email.headerregistry import ContentDispositionHeader
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import fsolve, minimize
import auswert
import cpfort
import crystal_plasticity_module as cp
import yieldfuncs as yf
import odflib
import os
import plotly.express as px
import plotly.graph_objects as go
import base64
import json
import pandas as pd
import dill


UPLOAD_DIRECTORY = "/Users/kimbi/Documents/Specialization Project/CP_Files/uploads/"
ASSET_DIRECTORY = "/Users/kimbi/Documents/Specialization Project/CP_Files/assets/"

def data_source_inputs(selected_grain_ori_state, selected_loading_state,
                        euler_phi1, euler_theta, euler_phi2, uploaded_filename, threshold,
                        L_XX, L_XY, L_XZ, L_YX, L_YY, L_YZ,  L_ZX, L_ZY, L_ZZ,
                        S_dir_XX, S_dir_XY, S_dir_XZ, S_dir_YX, S_dir_YY, S_dir_YZ, S_dir_ZX, S_dir_ZY, S_dir_ZZ,
                        S_abs_XX, S_abs_XY, S_abs_XZ, S_abs_YX, S_abs_YY, S_abs_YZ, S_abs_ZX, S_abs_ZY, S_abs_ZZ,
                        tot_von_mises_strain, number_steps):

    if (selected_grain_ori_state or selected_loading_state) is None:
        return None

    else: 
        if selected_grain_ori_state  == "Random":
            orientations = cp.generate_random_orientations(10000)

        elif selected_grain_ori_state == "Specify Euler Angles (Bunge's notation in degrees)":
            orientations = {}
            orientations['grains'] = [[euler_phi1, euler_theta, euler_phi2]]

        elif selected_grain_ori_state == "Upload file":
            if uploaded_filename.endswith('.ori'):
                orientations = {}
                file_ori = UPLOAD_DIRECTORY + uploaded_filename
                orientations['grains'] = np.loadtxt(file_ori, skiprows=3, usecols=(0,1,2))
            
            elif uploaded_filename.endswith('.ang'):
                orientations = {}
                file_ang = UPLOAD_DIRECTORY + uploaded_filename
                ori1 = np.loadtxt(file_ang, skiprows=103, usecols=(0,1,2))
                ori1 = np.rad2deg(ori1)
                ori2 = []
                threshold_list = np.loadtxt(file_ang, skiprows=103, usecols=(6))

                i = 0
                while i < len(ori1):
                    if threshold_list[i]>=threshold:
                        ori2.append(ori1[i])
                    i+=1

                orientations['grains'] = ori2

        if selected_loading_state == 'Uniaxial tension':
            # prescribed global velocity gradient
            L = np.array([[-0.5,   0.0,  0.0],
                        [ 0.0,  -0.5,  0.0],
                        [ 0.0,   0.0,  1.0]])
            # prescribed stress direction components
            S_direction = None
            # prescribed absolute stress components
            S_absolute = None
            # bool array for indicating known (True) and unknown (False) terms in both vel. gradient and stress tensor
            iL = True
            iS_direction = False
            iS_absolute = False

        elif selected_loading_state == 'Plane-strain compression':
            L = np.array([[1.0,   0.0,  0.0],
              [0.0,   0.0,  0.0],
              [0.0,   0.0, -1.0]])
            # prescribed stress direction components
            S_direction = None
            # prescribed absolute stress components
            S_absolute = None
            # bool array for indicating known (True) and unknown (False) terms in both vel. gradient and stress tensor
            iL = True
            iS_direction = False
            iS_absolute = False
        
        elif selected_loading_state == 'Mixed (strain+stress) boundary condition':
            # prescribed global velocity gradient
            L = None
            # prescribed stress direction components
            ang = np.deg2rad(0.)
            sd1 = 2./3.*np.cos(ang) - 1./3.*np.sin(ang)
            sd2 = 2./3.*np.sin(ang) - 1./3.*np.cos(ang)
            S_direction = [[sd1,     0.,    0.],
                        [    0., sd2,    0.],
                        [    0.,     0., -sd1-sd2]]
            # prescribed absolute stress components
            S_absolute = [[ 0., 0., 0.],
                        [ 0., 0., 0.],
                        [ 0., 0., 0.]]

            # bool array for indicating known (True) and unknown (False) terms in both vel. gradient and stress  
            iL = False
            iS_direction = [[  True, False, False],
                            [ False,  True, False],
                            [ False, False,  True]]
            iS_absolute = [[False,  True,  True],
                        [ True, False,  True],
                        [ True,  True, False]]

        elif selected_loading_state == 'Input Custom Values':
            # prescribed global velocity gradient
            L = np.array([[L_XX, L_XY, L_XZ],
                        [L_YX, L_YY, L_YZ],
                        [L_ZX, L_ZY, L_ZZ]])
            L[L==None]=0

            # prescribed stress direction components
            S_direction = np.array([[S_dir_XX, S_dir_XY,S_dir_XZ],
                        [S_dir_YX, S_dir_YY, S_dir_YZ],
                        [S_dir_ZX, S_dir_ZY, S_dir_ZZ]])
            S_direction[S_direction==None]=0

            # prescribed absolute stress components
            S_absolute = np.array([[S_abs_XX, S_abs_XY,S_abs_XZ],
                        [S_abs_YX, S_abs_YY, S_abs_YZ],
                        [S_abs_ZX, S_abs_ZY, S_abs_ZZ]])
            S_absolute[S_absolute==None]=0


            # bool array for indicating known (True) and unknown (False) terms in both vel. gradient and stress tensor
            if not np.any(L):
                iL = False
            else:
                iL = True

            #TO DO!
            iS_direction = False
            iS_absolute = False
    
        # border for ipf
        x3 = 1./np.sqrt(3.)/(1./np.sqrt(3.)+1.)
        x2 = 1./np.sqrt(2.)/(1./np.sqrt(2.)+1.)
        ipf_trace1=dict(type='scatter',
                                    x=[0., x2],
                                    y=[0., 0.],
                                    marker=dict(color='Black', size =3),
                                    showlegend=False)

        ipf_trace2=dict(type='scatter',
                                    x=[0., x3],
                                    y=[0., x3],
                                    marker=dict(color='Black', size =3),
                                    showlegend=False)
        # plot arc
        a2 = np.arange(0., 0.263, 0.001)
        ipf_trace3=dict(type='scatter',
                                    x=(1.+x2)*np.cos(a2)-1.,
                                    y=(1.+x2)*np.sin(a2),
                                    mode='markers',
                                    marker=dict(color='Black', size =3),
                                    showlegend=False)

        if number_steps == None:
            Nsteps = 100
        elif number_steps != None:
            Nsteps = number_steps

        if tot_von_mises_strain == None:
            dt = 0.01
        elif tot_von_mises_strain != None:
            DD = D_D(L)
            t_max = tot_von_mises_strain/(np.sqrt((3/2)*DD))
            dt = t_max/Nsteps
            print(dt)


        polycrystal_initial = data_source_initial(orientations)
    
        polefigure_initial = polycrystal_initial.plot_orientations_plotly(plot_type='PF')

        polycrystal_loaded = data_source_loaded(polycrystal_initial, orientations,L,S_direction,S_absolute,iL,iS_direction,iS_absolute, Nsteps, dt)
        
        with open('polycrystal_loaded.pkl', 'wb') as f:
            dill.dump(polycrystal_loaded, f)

        polefigure_loaded = polycrystal_loaded.plot_orientations_plotly(plot_type='PF')
    
        ipf_data = polycrystal_loaded.plot_orientations_plotly(plot_type='IPF')
        df_ipf_data = pd.DataFrame(ipf_data)
        df_ipf_data_transposed = df_ipf_data.transpose()


        inversepolefigure_start = []
        inversepolefigure_end = []
        inversepolefigure_trajectory = []
        for i in range(len(df_ipf_data_transposed)):
            inversepolefigure_start.append([i,df_ipf_data_transposed[0][i][0],df_ipf_data_transposed[1][i][0]])
            inversepolefigure_end.append([i,df_ipf_data_transposed[0][i][-1],df_ipf_data_transposed[1][i][-1]])
            for j in range(len(df_ipf_data_transposed[0][0])):
                inversepolefigure_trajectory.append([i,j,df_ipf_data_transposed[0][i][j],df_ipf_data_transposed[1][i][j]])


        df_inversepolefigure_trajectory = pd.DataFrame(inversepolefigure_trajectory, columns=['grain','iteration', 'x', 'y'])

        odf_data = polycrystal_loaded.plot_orientations_plotly(plot_type='ODF')

        
        # IPF trajectory figure
        fig_ipf_trajectory = px.scatter(df_inversepolefigure_trajectory, x="x", y="y", animation_frame="iteration")
        fig_ipf_trajectory.update_xaxes(showticklabels=False, showgrid=False, visible = False) # Hide x axis ticks 
        fig_ipf_trajectory.update_yaxes(showticklabels=False, showgrid=False, visible = False) # Hide y axis ticks
        fig_ipf_trajectory.update_traces(marker=dict(size=4, color = '#00256e'))
        fig_ipf_trajectory.add_trace(ipf_trace1)
        fig_ipf_trajectory.add_trace(ipf_trace2)
        fig_ipf_trajectory.add_trace(ipf_trace3)
        fig_ipf_trajectory.add_annotation(text='111', x=0.37, y=0.38, showarrow=False)
        fig_ipf_trajectory.add_annotation(text='101', x=0.43, y=0, showarrow=False)
        fig_ipf_trajectory.add_annotation(text='001', x=0, y=0.03, showarrow=False)
        fig_ipf_trajectory.update_layout(xaxis_range=[-0.05, 0.5],yaxis_range=[-0.05, 0.5],height=700, width=700, title_text = 'FCC (111)',title_x=0.5)


        # if include_ys == [1]:
        #     YL, r, num = polycrystal_loaded.yield_locus(locus_type='2D', number_of_points=50, plot_axes=('11','22'))
        #     ys_xvalues = YL[0,0,:]
        #     ys_yvalues = YL[1,1,:]
        # else:
        #     ys_xvalues = 0
        #     ys_yvalues = 0
        
        return {"fig_ipf_trajectory": fig_ipf_trajectory,
                "odf_data": odf_data,
                "polefigure_loaded": polefigure_loaded,
                "polefigure_initial": polefigure_initial,
                "inversepolefigure_start": inversepolefigure_start,
                "inversepolefigure_end": inversepolefigure_end,
                "inversepolefigure_trajectory": inversepolefigure_trajectory
                #"ys_xvalues": ys_xvalues,
                #"ys_yvalues": ys_yvalues,
                }

def data_source_loaded(polycrystal_initial, orientations,L,S_direction,S_absolute,iL,iS_direction,iS_absolute, Nsteps, dt):

    # grain orientations
    orientations = orientations

    # prescribed global velocity gradient
    L = L
    # prescribed stress direction components
    S_direction = S_direction
    # prescribed absolute stress components
    S_absolute = S_absolute
    # bool array for indicating known (True) and unknown (False) terms in both vel. gradient and stress tensor
    iL = iL
    iS_direction = iS_direction
    iS_absolute = iS_absolute

    # No elasticity
    elasticity = None

    # choose the crystallography of the grains
    crystal_structure = 'FCC_111'

    # Taylor model without grain interactions
    grain_interaction = 'FCTAYLOR'

    hardening_law = {'model'                : 'RIGID_PLASTIC',    # rigid plasticity with a given critical stress
                    'hardening_parameters' : [10.],              # CRSS [MPa]
                    'relax_penalties'      : [0., 0., 0.]}       # [MPa]

    # number of computation steps
    Nsteps = Nsteps
    # time increment
    dt = dt
    # run with elasticity or without
    run_elasticity = False
    # set export options
    results_output_options = {'grain_results'       : ['euler_angles','sliprates','crss','relaxation','stress_loc'],
                            'polycrystal_results' : ['average_stress','average_slip'],
                            'number_of_outputs'   : 100}
    dofortran = True

    # Load polycrystal
    polycrystal_initial.load(L, S_direction, S_absolute, iL, iS_direction, iS_absolute,
                    Nsteps, dt, run_elasticity, results_output_options, dofortran)

    return polycrystal_initial



def data_source_initial(orientations):

    # grain orientations
    orientations = orientations

    # No elasticity
    elasticity = None

    # choose the crystallography of the grains
    crystal_structure = 'FCC_111'

    # Taylor model without grain interactions
    grain_interaction = 'FCTAYLOR'

    hardening_law = {'model'                : 'RIGID_PLASTIC',    # rigid plasticity with a given critical stress
                    'hardening_parameters' : [10.],              # CRSS [MPa]
                    'relax_penalties'      : [0., 0., 0.]}       # [MPa]

    # Create polycrystal
    polycrystal = cp.Polycrystal(crystal_structure, orientations, elasticity, hardening_law, grain_interaction)

    return polycrystal

def D_D(L):
    L_T = np.transpose(L)
    D = (1/2)*(L+L_T)
    D_D = (((D[0,0])**2) + ((D[1,1])**2) + ((D[2,2])**2)) + (2*(((D[0,1])**2)+((D[0,2])**2)+((D[1,2])**2)))
    return D_D

def ys(plot_axes):
    print(plot_axes)
    with open('polycrystal_loaded.pkl', 'rb') as f:
        polycrystal_loaded = dill.load(f)
        
    YL, r, num = polycrystal_loaded.yield_locus(locus_type='2D', number_of_points=50, plot_axes=plot_axes) 
    ys_xvalues = YL[0,0,:]
    ys_yvalues = YL[1,1,:]
    return ys_xvalues, ys_yvalues



