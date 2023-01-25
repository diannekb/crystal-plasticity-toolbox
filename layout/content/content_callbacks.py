from dash import html, dcc, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datasource import create_initial_polycrystal, create_loaded_polycrystal, generate_pf, generate_ipf, generate_odf, generate_ys

def get_callbacks_content(app):

    # Callback to show or hide messagge "Update setup to generate plots" when app is initiliaze for the first time
    @app.callback(
        Output('tab-content','children'),
        #Input('tabs','active_tab'),
        Input('store_initial','data'),
    )
    def render_tab_content(data):
        """This function shows or hides the info message 'Update setup to generate plots'
        Input: Initial data
        Output: Show or hide info message 'Update setup to generate plots'"""
        if data is  None:
            return html.Br(), dbc.Alert("Update setup to generate plots.", color="warning")
        else:
            pass

    # Call back to generate and store data for initial polycrystal
    @app.callback(
        Output('store_initial','data'),
        Input('generate-polycrystal-button','n_clicks'),
        State('input-grain-ori-state','value'),
        State('input-random-num', 'value'),
        State('input-euler-phi1','value'),
        State('input-euler-theta','value'),
        State('input-euler-phi2','value'),
        State('uploaded-file','filename'),
        State('ang-threshold','value'),
    prevent_initial_call=True)
    def generate_initial_polycrystal(n_clicks, selected_grain_ori_state, random_num,
                                    euler_phi1, euler_theta, euler_phi2, uploaded_filename, threshold):
        """This function generates and stores data for loaded polycrystal when generate polycrystal button is clicked
        Input: Generate polycrystal button click, grain orientation selected, random grains entered, euler angles entered, uploaded file, .ang file threshold
        Output: Initial polycrystal data"""
        if n_clicks is None:
            raise PreventUpdate
        else:
            return create_initial_polycrystal(selected_grain_ori_state, random_num,
                                                euler_phi1, euler_theta, euler_phi2, uploaded_filename, threshold)

    # Call back to generate and store data for loaded polycrystal
    @app.callback(
        Output('store_loaded','data'),
        Input('load-polycrystal-button','n_clicks'),
        State('store_initial','data'),
        State('input-loading-state','value'),
        State('L-XX','value'),
        State('L-XY','value'),
        State('L-XZ','value'),
        State('L-YX','value'),
        State('L-YY','value'),
        State('L-YZ','value'),
        State('L-ZX','value'),
        State('L-ZY','value'),
        State('L-ZZ','value'),
        State('S-dir-XX','value'),
        State('S-dir-XY','value'),
        State('S-dir-XZ','value'),
        State('S-dir-YX','value'),
        State('S-dir-YY','value'),
        State('S-dir-YZ','value'),
        State('S-dir-ZX','value'),
        State('S-dir-ZY','value'),
        State('S-dir-ZZ','value'),
        State('S-abs-XX','value'),
        State('S-abs-XY','value'),
        State('S-abs-XZ','value'),
        State('S-abs-YX','value'),
        State('S-abs-YY','value'),
        State('S-abs-YZ','value'),
        State('S-abs-ZX','value'),
        State('S-abs-ZY','value'),
        State('S-abs-ZZ','value'),
        State('input-von-mises-strain', 'value'),
        State('input-number-steps', 'value'),
    prevent_initial_call=True)
    def generate_loaded_polycrystal(n_clicks, initial_data, selected_loading_state,
                                    L_XX, L_XY, L_XZ, L_YX, L_YY, L_YZ,  L_ZX, L_ZY, L_ZZ,
                                    S_dir_XX, S_dir_XY, S_dir_XZ, S_dir_YX, S_dir_YY, S_dir_YZ, S_dir_ZX, S_dir_ZY, S_dir_ZZ,
                                    S_abs_XX, S_abs_XY, S_abs_XZ, S_abs_YX, S_abs_YY, S_abs_YZ, S_abs_ZX, S_abs_ZY, S_abs_ZZ,
                                    tot_von_mises_strain, number_steps):
        """This function generates and stores data for loaded polycrystal when load polycrystal button is clicked
        Input: Initial polycrystal data, loading condition selected, global velocity gradient values, stress direction components values, absolute stress components values, total von mises stress value, number of steps value
        Output: Loades polycrystal data"""
        if n_clicks is None:
            raise PreventUpdate
        else:
            return create_loaded_polycrystal(initial_data, selected_loading_state,
                                        L_XX, L_XY, L_XZ, L_YX, L_YY, L_YZ,  L_ZX, L_ZY, L_ZZ,
                                        S_dir_XX, S_dir_XY, S_dir_XZ, S_dir_YX, S_dir_YY, S_dir_YZ, S_dir_ZX, S_dir_ZY, S_dir_ZZ,
                                        S_abs_XX, S_abs_XY, S_abs_XZ, S_abs_YX, S_abs_YY, S_abs_YZ, S_abs_ZX, S_abs_ZY, S_abs_ZZ,
                                        tot_von_mises_strain, number_steps)

    # Callback to generate and show pole figures
    @app.callback(
        Output('pf-content','children'),
        Input('store_initial', 'data'),
        Input('store_loaded', 'data'),
        Input('pf-checklist','value'),
        Input('pf-plane-input','value'),
        Input('pf-normal-radiobuttons','value'),
        Input('input-grain-ori-state','value'),
    prevent_initial_call=True)
    def gen_initial_pf(initial_data, loaded_data, pf_cl_value, planes_input, pf_normal_value, selected_grain_ori_state):
        """This function the generates and shows the Pole Figure
        Input: Initial polycrystal data, Loaded polycrystal data, pole figure checkbox value, pole figure plane value, pole figure normal value, grain orientation value
        Output: Pole figure"""
        if initial_data is not None:
            pf_figure = generate_pf(loaded_data, pf_cl_value, planes_input, pf_normal_value, selected_grain_ori_state)
            return dcc.Graph(figure = pf_figure)

    # Callback to show or hide UI elements in the Pole Figure tab
    @app.callback(
        Output('pf-inputs', 'style'),
        Output('pf-checklist','style'),
        Output('pf-show','style'),
        Output('pf-loaded-warning','style'),
        Input('store_initial','data'),
        Input('store_loaded','data'),
    )
    def show_hide_element(initial_data, loaded_data):
        """This function controls if which UI element in the pole figure tab will be shown or hidden
        Input: Initial polycrystal data, Loaded polycrystal data
        Output: Pole figure normal radio buttons style, Pole figure plane dropdown style, Pole figure show checkboxes style, Pole figure warning style"""
        if initial_data is not None:
            if loaded_data is not None:
                return {'display': 'block'}, {'display': 'block'}, {'display': 'block'}, {'display': 'none'}
            else:
                return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, {'display': 'block'}
        else:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}


    # Callback to generate and show inverse pole figures
    @app.callback(
        Output('ipf-content','children'),
        Input('store_initial', 'data'),
        Input('store_loaded', 'data'),
        Input('input-grain-ori-state','value'),
        Input('ipf-radiobuttons','value'),
        Input('ipf-checklist','value'),
    prevent_initial_call=True)
    def gen_initial_ipf(initial_data, loaded_data ,selected_grain_ori_state, ipf_value, ipf_cl_value):
        """This function the generates and shows the Inverse Pole Figure
        Input: Initial polycrystal data, Loaded polycrystal data, grain orientation value, IPF radio buttons value, IPF checkboxes value
        Output: Inverse Pole figure"""
        if initial_data is not None:

            ipf_figure = go.Figure(
                data=[go.Scatter(x = [], y = [], mode='markers', marker=dict(color = '#00256e',size=3), showlegend=False)],
                layout = {'xaxis': {'visible': False,
                                    'showticklabels': False},
                        'yaxis': {'visible': False,
                                    'showticklabels': False}
                }            
            )

            ipf_figure.update_layout(xaxis_range=[-0.05, 0.5],yaxis_range=[-0.05, 0.5],height=700, width=700)

            if loaded_data is None:
                
                ipf_start, ipf_trace1, ipf_trace2, ipf_trace3 = generate_ipf(selected_grain_ori_state, loaded_data)
                ipf_figure.add_trace(ipf_trace1)
                ipf_figure.add_trace(ipf_trace2)
                ipf_figure.add_trace(ipf_trace3)
                ipf_figure.add_trace(ipf_start)

            elif loaded_data == 1:

                fig_ipf_trajectory, ipf_start, ipf_end, ipf_trajectory, ipf_trace1, ipf_trace2, ipf_trace3 = generate_ipf(selected_grain_ori_state, loaded_data)

                if ipf_value == 'Animated':
                    return dcc.Graph(figure=fig_ipf_trajectory)
            
                elif ipf_value == 'Initial and Loaded View':

                    ipf_figure.add_trace(ipf_trace1)
                    ipf_figure.add_trace(ipf_trace2)
                    ipf_figure.add_trace(ipf_trace3)

                    if ipf_cl_value != []:
                        if 1 in ipf_cl_value:
                            ipf_figure.add_trace(ipf_start)
                        if 2 in ipf_cl_value:
                            ipf_figure.add_trace(ipf_end)
                        if 3 in ipf_cl_value:
                            ipf_figure.add_trace(ipf_trajectory)


            ipf_figure.add_annotation(text='111', x=0.37, y=0.38, showarrow=False)
            ipf_figure.add_annotation(text='101', x=0.43, y=0, showarrow=False)
            ipf_figure.add_annotation(text='001', x=0, y=0.03, showarrow=False)

            return dcc.Graph(figure=ipf_figure) 


    # Callback to show or hide UI elements in the Inverse Pole Figure tab
    @app.callback(
        Output('ipf-card','style'),
        Output('ipf-radiobuttons-visibility','style'),
        Output('ipf-loaded-warning','style'),
        Output('ipf-checklist-visibility','style'),
        Input('store_initial','data'),
        Input('store_loaded','data'),
        Input('ipf-radiobuttons','value')
    )
    def show_hide_element(initial_data, loaded_data, ipf_radiobutton_value):
        """This function controls if which UI element in the inverse pole figure tab will be shown or hidden
        Input: Initial polycrystal data, Loaded polycrystal data
        Output: IPF card style, IPF radio buttons style, IPF warning style, IPF checkboxes style"""
        if initial_data is not None:
            if loaded_data is not None:
                if ipf_radiobutton_value == "Initial and Loaded View":
                    return {'display': 'block'}, {'display': 'block'}, {'display': 'none'}, {'display': 'block'}
                else:
                    return {'display': 'block'}, {'display': 'block'}, {'display': 'none'}, {'display': 'none'}
            else:
                return {'display': 'block'}, {'display': 'none'}, {'display': 'block'}, {'display': 'none'}
        else:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    # Callback to generate and show ODF figure
    @app.callback(
        Output('odf-initial','children'),
        Output('odf-initial-label','style'),
        Output('odf-loaded','children'),
        Output('odf-loaded-label','style'),
        Input('odf-button-state','n_clicks'),
        State('store_initial','data'),
        State('store_loaded','data'),
        State('odf-levels-input','value')
    )
    def gen_odf(n_clicks, initial_data, loaded_data, odf_levels):
        """This function the generates and shows the ODF figure
        Input: Generate ODF button click, Initial polycrystal data, Loaded polycrystal data, ODF levels value
        Output: ODF figure"""
        
        default_levels = [2,4,8,12,16,20,25,30,35]

        if initial_data is not None:

            if odf_levels == None:
                odf_levels_list = default_levels
            elif odf_levels == '':
                odf_levels_list = default_levels
            elif odf_levels == []:
                odf_levels_list = default_levels
            else:
                odf_levels_strlist = list(odf_levels.split(","))
                odf_levels_list = [eval(i) for i in odf_levels_strlist]

            initial_odf, loaded_odf = generate_odf(odf_levels_list, loaded_data)

            if loaded_data is None:

                return html.Img(src = initial_odf), {'display': 'block'}, loaded_odf, {'display': 'none'}

            elif loaded_data == 1:

                return html.Img(src = initial_odf), {'display': 'block'}, html.Img(src = loaded_odf), {'display': 'block'}
        
        else:
            return None,{'display': 'none'}, None, {'display': 'none'}


    # Callback to show or hide UI elements in the ODF tab
    @app.callback(
        Output('odf-fields','style'),
        Output('odf-loaded-warning','style'),
        Input('store_initial','data'),
        Input('store_loaded','data'),
    )
    def show_hide_element(initial_data, loaded_data):
        """This function controls if which UI element in the ODF tab will be shown or hidden
        Input: Initial polycrystal data, Loaded polycrystal data
        Output: ODF level style, ODF warning message style"""
        if initial_data is not None:
            if loaded_data is not None:
                return {'display': 'block'}, {'display': 'none'}
            else:
                return {'display': 'block'}, {'display': 'block'}
        else:
            return {'display': 'none'}, {'display': 'none'}

    # Callback to generate and show Yield Surface
    @app.callback(
        Output('ys-content','children'),
        Input('ys-button-state','n_clicks'),
        State('store_initial', 'data'),
        State('store_loaded', 'data'),
        State('ys-input-x','value'),
        State('ys-input-y','value'),
        State('ys-checklist', 'value')
    )
    def gen_ys(n_clicks, initial_data, loaded_data, ys_input_x, ys_input_y, ys_cl_value):
        """This function the generates and shows the Yield Surface
        Input: Generate yield surface button click, Initial polycrystal data, Loaded polycrystal data, x-axis value, y-axis value, yield surface checbox value
        Output: Yield surface graph"""

        if initial_data is not None:

            plot_axes = [0,0]
            plot_axes[0] = ys_input_x
            plot_axes[1] = ys_input_y
            plot_axes_tup = tuple(plot_axes)

            if loaded_data is None: 

                ys_xvalues_initial, ys_yvalues_initial, ys_xvalues_loaded, ys_yvalues_loaded= generate_ys(plot_axes_tup, loaded_data)

                df_ys = pd.DataFrame(ys_xvalues_initial)
                df_ys[1] = ys_yvalues_initial
                fig_ys = px.scatter(df_ys, x = 0, y = 1,
                                    labels={
                                        "0": "S"+plot_axes_tup[0],
                                        "1": "S"+plot_axes_tup[1],
                                    })
                fig_ys.update_layout(xaxis_range=[-40,40],yaxis_range=[-40,40],height=600, width=600)
                fig_ys.update_traces(marker=dict(color='#00256e'))

                return dcc.Graph(figure = fig_ys)

            if loaded_data == 1:
                fig_ys = go.Figure(
                    data=[go.Scatter(x = [], y = [], mode='markers', showlegend=False)],
                    layout = {'xaxis': {'visible': True,
                                        'showticklabels': True},
                            'yaxis': {'visible': True,
                                        'showticklabels': True}
                    }            
                )
                fig_ys.update_layout(xaxis_range=[-40,40],yaxis_range=[-40,40],height=600, width=600)

                ys_xvalues_initial, ys_yvalues_initial, ys_xvalues_loaded, ys_yvalues_loaded= generate_ys(plot_axes_tup, loaded_data)
                
                if ys_cl_value != []:
                    if 1 in ys_cl_value:
                        df_ys_initial = pd.DataFrame(ys_xvalues_initial)
                        df_ys_initial[1] = ys_yvalues_initial
                        fig_ys_initial = go.Scatter(x = df_ys_initial[0], y = df_ys_initial[1], mode='markers', marker=dict(color = '#78abde',size=5), name = "Initial", showlegend=True)
                        fig_ys.add_trace(fig_ys_initial)
                    if 2 in ys_cl_value:
                        df_ys_loaded = pd.DataFrame(ys_xvalues_loaded)
                        df_ys_loaded[1] = ys_yvalues_loaded
                        fig_ys_loaded = go.Scatter(x = df_ys_loaded[0], y = df_ys_loaded[1], mode='markers', marker=dict(color = '#00256e',size=5), name = "Loaded", showlegend=True)
                        fig_ys.add_trace(fig_ys_loaded)

                fig_ys.update_xaxes(title_text = "S"+ plot_axes_tup[0])
                fig_ys.update_yaxes(title_text = "S"+plot_axes_tup[1])

                return dcc.Graph(figure = fig_ys)
        
        else:
            return None

    # Callback to show or hide UI elements in the Yield Surface tab
    @app.callback(
        Output('ys-fields','style'),
        Output('ys-loaded-warning','style'),
        Output('ys-checklist-visibility', 'style'),
        Input('store_initial','data'),
        Input('store_loaded','data'),
        
    )
    def show_hide_element(initial_data, loaded_data):
        """This function controls if which UI element in the Yield Surface tab will be shown or hidden
        Input: Initial polycrystal data, Loaded polycrystal data
        Output: Yield surface x-axis and y-axis fields style, Yield surface warning message style, Yield surface checbox style"""
        if initial_data is not None:
            if loaded_data is not None:
                return {'display': 'block'}, {'display': 'none'}, {'display': 'block'}
            else:
                return {'display': 'block'}, {'display': 'block'}, {'display': 'none'}
        else:
            return {'display': 'none'}, {'display': 'none'}, {'display': 'none'}

    # Callback for clearing the initial polycrystal data everytime the generate polycrystal button is clicked
    @app.callback(
        Output('store_loaded','clear_data'),
        Input('generate-polycrystal-button','n_clicks')
    )
    def clear_store_data(n_click):
        """This function clears the initial polycrystal data when the generate polycrystal button is clicked.
        Input: Generate polycrystal button click
        Output: Trigger to clear initial stored data"""
        if n_click is not None and n_click > 0:
            return True
        else:
            return False

