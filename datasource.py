import numpy as np
import crystal_plasticity_module as cp
import odflib
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import dill

# Path where the uploaded files will be stored
UPLOAD_DIRECTORY = "/Users/kimbi/Documents/Specialization Project/CP_Files/uploads/"

# Funtion that triggers the creation of the initial polycvrystal data and returns flag if initial polycrystal data is generated
def create_initial_polycrystal(selected_grain_ori_state, random_num,
                        euler_phi1, euler_theta, euler_phi2, uploaded_filename, threshold):
    """
    Input: Grain Orientaion selected, Entered number of random grains, Euler angeles, Uploaded filename, .ang threshold
    Output: Flag if initial polycrystal data is generated. Returns 'None' if is is NOT generated and returns 1 if it is generated.
    """
    if selected_grain_ori_state is None:
        return None

    else: 
        if selected_grain_ori_state  == "Random":
            orientations = cp.generate_random_orientations(random_num)

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
        polycrystal_initial = cp.Polycrystal(crystal_structure, orientations, elasticity, hardening_law, grain_interaction)

        with open('polycrystal_initial.pkl', 'wb') as f:
            dill.dump(polycrystal_initial, f)
        
        return 1

# Function that triggers the creation of the loaded polycvrystal data and returns flag if loaded polycrystal data is generated
def create_loaded_polycrystal(initial_data, selected_loading_state,
                                L_XX, L_XY, L_XZ, L_YX, L_YY, L_YZ,  L_ZX, L_ZY, L_ZZ,
                                S_dir_XX, S_dir_XY, S_dir_XZ, S_dir_YX, S_dir_YY, S_dir_YZ, S_dir_ZX, S_dir_ZY, S_dir_ZZ,
                                S_abs_XX, S_abs_XY, S_abs_XZ, S_abs_YX, S_abs_YY, S_abs_YZ, S_abs_ZX, S_abs_ZY, S_abs_ZZ,
                                tot_von_mises_strain, number_steps):
    """
    Input: Initial polycrystal data, Loading condition selected, Global velocitry gradient values, Stress direction component values, Absolute stress component values, Total Von Mises Strain value, Number of Steps value
    Output: Flag if loaded polycrystal data is generated. Returns 'None' if is is NOT generated and returns 1 if it is generated.
    """
    if initial_data is None:
        return None
        
    elif initial_data == 1:
        if selected_loading_state is None:
            return None

        else:
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

            if number_steps == None:
                Nsteps = 100
            elif number_steps != None:
                Nsteps = number_steps

            D = deformation_rate(L)
            t_max = tot_von_mises_strain/(np.sqrt((3/2)*D))
            dt = t_max/Nsteps

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

            with open('polycrystal_initial.pkl', 'rb') as f:
                polycrystal_initial = dill.load(f)

            # Load polycrystal
            polycrystal_initial.load(L, S_direction, S_absolute, iL, iS_direction, iS_absolute,
                            Nsteps, dt, run_elasticity, results_output_options, dofortran)

            with open('polycrystal_loaded.pkl', 'wb') as f:
                dill.dump(polycrystal_initial, f)

            return 1

# Function that generates data and figures for initial and loaded pole figures
def generate_pf(loaded_data, pf_cl_value, planes_input, pf_normal_value, selected_grain_ori_state):
    """
    Input: Loaded polycrystal data, Pole figure to show checkbox value, Pole figure plane, Pole figure normal value, Grain orientation selected
    Output: Pole figure
    """
    if loaded_data is None:

        with open('polycrystal_initial.pkl', 'rb') as f:
            polycrystal_initial = dill.load(f)
        

        polefigure_initial = polycrystal_initial.plot_orientations_plotly(plot_type='PF', crystal_structure = planes_input)

        
        if selected_grain_ori_state == "Specify Euler Angles (Bunge's notation in degrees)":
            marker_size = 5
        else:
            marker_size = 3

        fig_pf_initial_nd = go.Scatter(x = polefigure_initial[0], y = polefigure_initial[3], mode='markers', marker=dict(color = '#78abde',size=marker_size), showlegend=False)

        fig_pf_initial_td = go.Scatter(x = polefigure_initial[1], y = polefigure_initial[4], mode='markers', marker=dict(color = '#78abde',size=marker_size), showlegend=False)

        fig_pf_initial_rd = go.Scatter(x = polefigure_initial[2], y = polefigure_initial[5], mode='markers', marker=dict(color = '#78abde',size=marker_size), showlegend=False)

        pf_figure = go.Figure(
            data=[go.Scatter(x = [], y = [], mode='markers', showlegend=False)],
            layout = {'xaxis': {'visible': True,
                                'showticklabels': False},
                    'yaxis': {'visible': True,
                                'showticklabels': False}
            }            
        )

        #circle for pf
        a1 = np.arange(0,2*np.pi,0.01)
        x1 = np.cos(a1)
        y1 = np.sin(a1)
        trace_circle=dict(type='scatter',
                                    x=x1,
                                    y=y1,
                                    mode='markers',
                                    marker=dict(color='#b8b8b8', size =3),
                                    showlegend=False)

        pf_figure.add_trace(trace_circle)
        
        if pf_normal_value == 'ND':
            pf_figure.add_trace(fig_pf_initial_nd)
            pf_figure.add_annotation(text='RD', x=0, y=-1.1, showarrow=False)
            pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)
        elif pf_normal_value == 'TD':
            pf_figure.add_trace(fig_pf_initial_td)
            pf_figure.add_annotation(text='RD', x=0, y=-1.1, showarrow=False)
            pf_figure.add_annotation(text='ND', x=-1.1, y=0, showarrow=False)
        elif pf_normal_value == 'RD':
            pf_figure.add_trace(fig_pf_initial_rd)
            pf_figure.add_annotation(text='ND', x=0, y=1.1, showarrow=False)
            pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)


        pf_figure.update_layout(height=700, width=700)

        return pf_figure

    elif loaded_data == 1:

        with open('polycrystal_initial.pkl', 'rb') as f:
            polycrystal_initial = dill.load(f)

        polefigure_initial = polycrystal_initial.plot_orientations_plotly(plot_type='PF', crystal_structure = planes_input)


        with open('polycrystal_loaded.pkl', 'rb') as f:
            polycrystal_loaded = dill.load(f)
        
        if selected_grain_ori_state == "Specify Euler Angles (Bunge's notation in degrees)":
            marker_size = 5
        else:
            marker_size = 3

        polefigure_loaded = polycrystal_loaded.plot_orientations_plotly(plot_type='PF', crystal_structure = planes_input)

        fig_pf_initial_nd = go.Scatter(x = polefigure_initial[0], y = polefigure_initial[3], mode='markers', marker=dict(color = '#78abde',size=marker_size), showlegend=False)
        fig_pf_loaded_nd = go.Scatter(x = polefigure_loaded[0], y = polefigure_loaded[3], mode='markers', marker=dict(color = '#00256e',size=marker_size), showlegend=False)

        fig_pf_initial_td = go.Scatter(x = polefigure_initial[1], y = polefigure_initial[4], mode='markers', marker=dict(color = '#78abde',size=marker_size), showlegend=False)
        fig_pf_loaded_td = go.Scatter(x = polefigure_loaded[1], y = polefigure_loaded[4], mode='markers', marker=dict(color = '#00256e',size=marker_size), showlegend=False)

        fig_pf_initial_rd = go.Scatter(x = polefigure_initial[2], y = polefigure_initial[5], mode='markers', marker=dict(color = '#78abde',size=marker_size), showlegend=False)
        fig_pf_loaded_rd = go.Scatter(x = polefigure_loaded[2], y = polefigure_loaded[5], mode='markers', marker=dict(color = '#00256e',size=marker_size), showlegend=False)

        pf_figure = go.Figure(
            data=[go.Scatter(x = [], y = [], mode='markers', showlegend=False)],
            layout = {'xaxis': {'visible': True,
                                'showticklabels': False},
                    'yaxis': {'visible': True,
                                'showticklabels': False}
            }            
        )

        #circle for pf
        a1 = np.arange(0,2*np.pi,0.01)
        x1 = np.cos(a1)
        y1 = np.sin(a1)
        trace_circle=dict(type='scatter',
                                    x=x1,
                                    y=y1,
                                    mode='markers',
                                    marker=dict(color='#b8b8b8', size =3),
                                    showlegend=False)

        pf_figure.add_trace(trace_circle)
        
        if pf_cl_value != []:
            if 1 in pf_cl_value:
                if pf_normal_value == 'ND':
                    pf_figure.add_trace(fig_pf_initial_nd)
                    pf_figure.add_annotation(text='RD', x=0, y=-1.1, showarrow=False)
                    pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)
                elif pf_normal_value == 'TD':
                    pf_figure.add_trace(fig_pf_initial_td)
                    pf_figure.add_annotation(text='RD', x=0, y=-1.1, showarrow=False)
                    pf_figure.add_annotation(text='ND', x=-1.1, y=0, showarrow=False)
                elif pf_normal_value == 'RD':
                    pf_figure.add_trace(fig_pf_initial_rd)
                    pf_figure.add_annotation(text='ND', x=0, y=1.1, showarrow=False)
                    pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)

            if 2 in pf_cl_value:
                if pf_normal_value == 'ND':
                    pf_figure.add_trace(fig_pf_loaded_nd)
                    pf_figure.add_annotation(text='RD', x=0, y=-1.1, showarrow=False)
                    pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)
                elif pf_normal_value == 'TD':
                    pf_figure.add_trace(fig_pf_loaded_td)
                    pf_figure.add_annotation(text='RD', x=0, y=-1.1, showarrow=False)
                    pf_figure.add_annotation(text='ND', x=-1.1, y=0, showarrow=False)
                elif pf_normal_value == 'RD':
                    pf_figure.add_trace(fig_pf_loaded_rd)
                    pf_figure.add_annotation(text='ND', x=0, y=1.1, showarrow=False)
                    pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)

            pf_figure.update_layout(height=700, width=700)

            return pf_figure 
        
# Function that generates data and figures for initial and loaded inverse pole figures
def generate_ipf(selected_grain_ori_state, loaded_data):
    """
    Input: Grain orientation selected, Loaded polycrystal data
    Output: Inverse Pole Figure
    """

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

    if selected_grain_ori_state == "Specify Euler Angles (Bunge's notation in degrees)":
        marker_size = 4
        trajectory_size = 3
    else:
        marker_size = 3
        trajectory_size = 1

    inversepolefigure_start = []
    inversepolefigure_end = []
    inversepolefigure_trajectory = []

    if loaded_data is None:

        with open('polycrystal_initial.pkl', 'rb') as f:
            polycrystal_initial = dill.load(f)

        ipf_data = polycrystal_initial.plot_orientations_plotly(plot_type='IPF')

        df_ipf_data = pd.DataFrame(ipf_data)
        df_ipf_data_transposed = df_ipf_data.transpose()

        for i in range(len(df_ipf_data_transposed)):
            inversepolefigure_start.append([i,df_ipf_data_transposed[0][i][0],df_ipf_data_transposed[1][i][0]])

        df_inversepolefigure_start = pd.DataFrame(inversepolefigure_start, columns=['grain','x', 'y'])

        ipf_start = go.Scatter(x = df_inversepolefigure_start.loc[:,"x"], y = df_inversepolefigure_start.loc[:,"y"], mode='markers', marker=dict(color = '#78abde',size=marker_size), showlegend=False)
        
        return ipf_start, ipf_trace1, ipf_trace2, ipf_trace3
    
    elif loaded_data == 1:

        with open('polycrystal_loaded.pkl', 'rb') as f:
            polycrystal_loaded = dill.load(f)

        ipf_data = polycrystal_loaded.plot_orientations_plotly(plot_type='IPF')

        df_ipf_data = pd.DataFrame(ipf_data)
        df_ipf_data_transposed = df_ipf_data.transpose()

        for i in range(len(df_ipf_data_transposed)):
            inversepolefigure_start.append([i,df_ipf_data_transposed[0][i][0],df_ipf_data_transposed[1][i][0]])
            inversepolefigure_end.append([i,df_ipf_data_transposed[0][i][-1],df_ipf_data_transposed[1][i][-1]])
            for j in range(len(df_ipf_data_transposed[0][0])):
                inversepolefigure_trajectory.append([i,j,df_ipf_data_transposed[0][i][j],df_ipf_data_transposed[1][i][j]])

        df_inversepolefigure_trajectory = pd.DataFrame(inversepolefigure_trajectory, columns=['grain','iteration', 'x', 'y'])
        
        # IPF trajectory figure
        fig_ipf_trajectory = px.scatter(df_inversepolefigure_trajectory, x="x", y="y", animation_frame="iteration")
        fig_ipf_trajectory.update_xaxes(showticklabels=False, showgrid=False, visible = False) # Hide x axis ticks 
        fig_ipf_trajectory.update_yaxes(showticklabels=False, showgrid=False, visible = False) # Hide y axis ticks
        fig_ipf_trajectory.update_traces(marker=dict(size=marker_size, color = '#00256e'))
        fig_ipf_trajectory.add_trace(ipf_trace1)
        fig_ipf_trajectory.add_trace(ipf_trace2)
        fig_ipf_trajectory.add_trace(ipf_trace3)
        fig_ipf_trajectory.add_annotation(text='111', x=0.37, y=0.38, showarrow=False)
        fig_ipf_trajectory.add_annotation(text='101', x=0.43, y=0, showarrow=False)
        fig_ipf_trajectory.add_annotation(text='001', x=0, y=0.03, showarrow=False)
        fig_ipf_trajectory.update_layout(xaxis_range=[-0.05, 0.5],yaxis_range=[-0.05, 0.5],height=700, width=700)

        df_inversepolefigure_start = pd.DataFrame(inversepolefigure_start, columns=['grain','x', 'y'])
        df_inversepolefigure_end = pd.DataFrame(inversepolefigure_end, columns=['grain','x', 'y'])
        df_inversepolefigure_trajectory = pd.DataFrame(inversepolefigure_trajectory, columns=['grain','iteration', 'x', 'y'])

        ipf_start = go.Scatter(x = df_inversepolefigure_start.loc[:,"x"], y = df_inversepolefigure_start.loc[:,"y"], mode='markers', marker=dict(color = '#78abde',size=marker_size), showlegend=False)
        ipf_end = go.Scatter(x = df_inversepolefigure_end.loc[:,"x"], y = df_inversepolefigure_end.loc[:,"y"], mode='markers', marker=dict(color = '#00256e',size=marker_size), showlegend=False)
        ipf_trajectory = go.Scatter(x = df_inversepolefigure_trajectory.loc[:,"x"], y = df_inversepolefigure_trajectory.loc[:,"y"], mode='markers', marker=dict(color = '#00d900',size=trajectory_size), showlegend=False)

        return fig_ipf_trajectory, ipf_start, ipf_end, ipf_trajectory, ipf_trace1, ipf_trace2, ipf_trace3

# Function that generates ODF figures
def generate_odf(odf_levels_list, loaded_data):
    """
    Input: ODF levels value, Loaded polycrystal data
    Output: Inverse Pole Figure
    """

    with open('polycrystal_initial.pkl', 'rb') as f:
        polycrystal_initial = dill.load(f)

    odf_data = polycrystal_initial.plot_orientations_plotly(plot_type='ODF')
    ori = odflib.Orientations(angles=odf_data)
    odf = odflib.ODF(orientations=ori)
    initial_odf = odf.save_plotly(boundaries=odf_levels_list)

    if loaded_data is None:

        return initial_odf, None

    if loaded_data == 1:

        with open('polycrystal_loaded.pkl', 'rb') as f:
            polycrystal_loaded = dill.load(f)

        odf_data = polycrystal_loaded.plot_orientations_plotly(plot_type='ODF')
        ori = odflib.Orientations(angles=odf_data)
        odf = odflib.ODF(orientations=ori)
        loaded_odf = odf.save_plotly(boundaries=odf_levels_list)
        
        return initial_odf, loaded_odf

# Function that generates Yield Surface graphs
def generate_ys(plot_axes, loaded_data):
    """
    Input: Axes for the yield surface, Loaded polycrystal data
    Output: IYield Surface graph
    """

    xij = [int(x)-1 for x in plot_axes[0]]
    xij.sort()
    xij = tuple(xij)
    yij = [int(x)-1 for x in plot_axes[1]]
    yij.sort()
    yij = tuple(yij)
    xi, xj = xij
    yi, yj = yij

    if loaded_data is None:

        with open('polycrystal_initial.pkl', 'rb') as f:
            polycrystal_initial = dill.load(f)

        YL_initial, r_initial, num_initial = polycrystal_initial.yield_locus(locus_type='2D', number_of_points=50, plot_axes=plot_axes)
        ys_xvalues_initial = YL_initial[xi,xj,:]
        ys_yvalues_initial = YL_initial[yi,yj,:]

        ys_xvalues_loaded = 0
        ys_yvalues_loaded = 0

    if loaded_data == 1:

        with open('polycrystal_initial.pkl', 'rb') as f:
            polycrystal_initial = dill.load(f)

        with open('polycrystal_loaded.pkl', 'rb') as f:
            polycrystal_loaded = dill.load(f)

        YL_initial, r_initial, num_initial = polycrystal_initial.yield_locus(locus_type='2D', number_of_points=50, plot_axes=plot_axes)
        ys_xvalues_initial = YL_initial[xi,xj,:]
        ys_yvalues_initial = YL_initial[yi,yj,:]

        YL_loaded, r_loaded, num_loaded = polycrystal_loaded.yield_locus(locus_type='2D', number_of_points=50, plot_axes=plot_axes)       
        ys_xvalues_loaded = YL_loaded[xi,xj,:]
        ys_yvalues_loaded = YL_loaded[yi,yj,:]
    
    return ys_xvalues_initial, ys_yvalues_initial, ys_xvalues_loaded, ys_yvalues_loaded

# Function to calculate deformation rate from gradient velocity
def deformation_rate(L):
    """
    Input: Global velocity gradient (L) matrix
    Output: D:D
    """
    L_T = np.transpose(L)
    D = (1/2)*(L+L_T)
    D_D = (((D[0,0])**2) + ((D[1,1])**2) + ((D[2,2])**2)) + (2*(((D[0,1])**2)+((D[0,2])**2)+((D[1,2])**2)))
    return D_D

