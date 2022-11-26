from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import dash_loading_spinners as dls
import datasource as ds
import upload_file
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import odflib
import crystal_plasticity_module as cp


app = Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server=app.server

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "25rem",
    "padding": "2rem 1rem",
    "overflow": "auto",
    "background-color": "#ebebeb",
}

CONTENT_STYLE = {
    "margin-left": "27rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "overflow": "auto",
}


#header = html.Div([])

sidebar = html.Div([
        html.H4("Setup"),
        html.Hr(),

        # Input Grain Orientation
        html.Div([
            dbc.Label("GRAIN ORIENTATION*"),
            dbc.Select(
                id = 'input-grain-ori-state',
                options =[
                    {'label':"Random", 'value':"Random"},
                    {'label': "Specify Euler Angles (Bunge's notation in degrees)", 'value':"Specify Euler Angles (Bunge's notation in degrees)"},
                    {'label': "Upload file", 'value':"Upload file"},
                    ],
                value = None
            )
         ]),

        # Input Euler Angles
        html.Div([
            html.Br(),
            dbc.Row([ 
                dbc.Col([
                    dbc.Row([
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                min = 0,
                                max = 360,
                                step = 0.001,
                                id = 'input-euler-phi1',
                                value = 264.99
                            ),
                            dbc.Label("Phi1"),
                            ])
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                min = 0,
                                max = 180,
                                step = 0.001,
                                id = 'input-euler-theta',
                                value = 7.19
                            ),
                            dbc.Label("Theta"),
                            ])
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                min = 0,
                                max = 360,
                                step = 0.001,
                                id = 'input-euler-phi2',
                                value = 163.59
                            ),
                            dbc.Label("Phi2"),
                            ])
                        ])
                    ]),
                    html.Br()
                ])         
            ],
            id = 'euler-hide')
        ],style= {'display': 'block'}),

        #Input .ang threshold
        html.Div([
            dbc.Row([ 
                dbc.Col([
                    dbc.FormFloating([
                        dbc.Input(
                        type = 'number',
                        min = 0,
                        max = 1,
                        step = 0.01,
                        id = 'ang-threshold'
                    ),
                    dbc.Label("Threshold (0-1.0)")
                    ]),
                ]),
                html.Br()
            ],
            id = 'ang-threshold-hide')
        ],style= {'display': 'block'}),

        # File upload for orientations
        html.Div([
            dbc.Row([ 
                dbc.Col([
                    dcc.Upload(
                        id = "uploaded-file",
                        children = html.Div(['Drag or select a file to upload']),
                        style={
                        'width': '90%',
                        'height': '110px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '10px'
                        },
                        multiple = False
                    )
                ]),       
                html.Div([
                    dbc.Alert(id="upload-indicator", color="success")
                ])
            ],
            id = 'upload-hide')
        ],style= {'display': 'block'}),

        # Input Loading Condition
        html.Div([
            dbc.Label("LOADING CONDITION*"),
            dbc.Select(
                id = 'input-loading-state',
                options =[
                        {'label':"Uniaxial tension", 'value':"Uniaxial tension"},
                        {'label':"Plane-strain compression", 'value':"Plane-strain compression"},
                        {'label': "Mixed (strain+stress) boundary condition", 'value':"Mixed (strain+stress) boundary condition"},
                        {'label': "Input Custom Values", 'value':"Input Custom Values"}
                        ],
                value = None
            )
        ]),

        # Input custom loading conditions
        html.Div([
            html.Br(),

            # Matrix for GLOBAL VELOCITY GRADIENT (L)
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Label("GLOBAL VELOCITY GRADIENT (L)"),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'L-XX'
                            ),
                            dbc.Label("XX")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'L-XY'
                            ),
                            dbc.Label("XY")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'L-XZ'
                            ),
                            dbc.Label("XZ")
                            ])
                        ])   
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'L-YX'
                            ),
                            dbc.Label("YX")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'L-YY'
                            ),
                            dbc.Label("YY")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'L-YZ'
                            ),
                            dbc.Label("YZ")
                            ])
                        ])   
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'L-ZX'
                            ),
                            dbc.Label("ZX")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'L-ZY'
                            ),
                            dbc.Label("ZY")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'L-ZZ'
                            ),
                            dbc.Label("ZZ")
                            ])
                        ])   
                    ])                
                ])
            ]),
            html.Br(),

            # Matrix for STRESS DIRECTION COMPONENTS
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Label("STRESS DIRECTION COMPONENTS"),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-dir-XX'
                            ),
                            dbc.Label("XX")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-dir-XY'
                            ),
                            dbc.Label("XY")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-dir-XZ'
                            ),
                            dbc.Label("XZ")
                            ])
                        ])   
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-dir-YX'
                            ),
                            dbc.Label("YX")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-dir-YY'
                            ),
                            dbc.Label("YY")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-dir-YZ'
                            ),
                            dbc.Label("YZ")
                            ])
                        ])   
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-dir-ZX'
                            ),
                            dbc.Label("ZX")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-dir-ZY'
                            ),
                            dbc.Label("ZY")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-dir-ZZ'
                            ),
                            dbc.Label("ZZ")
                            ])
                        ])   
                    ])                
                ])
            ]),
            html.Br(),

            # Matrix for ABSOLUTE STRESS COMPONENTS
            dbc.Row([
                dbc.Col([
                    dbc.Row([
                        dbc.Label("ABSOLUTE STRESS COMPONENTS"),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-abs-XX'
                            ),
                            dbc.Label("XX")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-abs-XY'
                            ),
                            dbc.Label("XY")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-abs-XZ'
                            ),
                            dbc.Label("XZ")
                            ])
                        ])   
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-abs-YX'
                            ),
                            dbc.Label("YX")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-abs-YY'
                            ),
                            dbc.Label("YY")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-abs-YZ'
                            ),
                            dbc.Label("YZ")
                            ])
                        ])   
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-abs-ZX'
                            ),
                            dbc.Label("ZX")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-abs-ZY'
                            ),
                            dbc.Label("ZY")
                            ]),
                        ]),
                        dbc.Col([
                            dbc.FormFloating([
                                dbc.Input(
                                type = 'number',
                                id = 'S-abs-ZZ'
                            ),
                            dbc.Label("ZZ")
                            ])
                        ])   
                    ])                
                ])
            ])
        ],id = 'loading-cond-hide',style= {'display': 'block'}), 


        # Input Total Von Mises Strain
        html.Div([
            html.Br(),
            dbc.Label("TOTAL VON MISES STRAIN*"),
            dbc.Input(
                id = 'input-von-mises-strain',
                type = 'number',
                step = 0.001,
                #value = 100
            )
        ]),
    
        # Input Number of steps
        html.Div([
            html.Br(),
            dbc.Label("NUMBER OF STEPS*"),
            dbc.Input(
                id = 'input-number-steps',
                type = 'number',
                step = 1,
                #value = 100
            )
        ]),
    
        # Yield Surface Switch

        # html.Div([
        #     html.Br(),
        #     dbc.Checklist(
        #         options=[
        #             {"label":"INCLUDE YIELD SURFACE?", "value":1}
        #         ],
        #         switch=True,
        #         id='ys-checklist'
        #     ),
        #     dbc.FormText("Including the yield surface would take max of 5 minutes of loading time to generate the figures.")
        # ]),

        # Generate Button
        html.Div([
            html.Br(),
            dbc.Row([
                dbc.Col([

                    #dbc.Button(id='reset-button-state',
                                #className = 'btn-dark',
                                #n_clicks=0,
                                #children='RESET',
                                #style={"margin-left": "10px"}),

                    dbc.Button(id='generate-button-state',
                                className = 'btn-success',
                                n_clicks=0,
                                children='GENERATE',
                                style={"margin-left": "10px"})
                ], style={'textAlign':'right'}),
            ])
        ])

    ],style=SIDEBAR_STYLE)

content = html.Div([
            html.Div([
                html.H1("CRYSTAL PLASTICITY TOOLBOX"),
                # Tabs 
                dbc.Row([
                    dbc.Tabs([

                        # Tab - Pole Figures
                        dbc.Tab(
                            children=[
                                    html.Div([
                                        html.Br(),
                                        dbc.Label("Show:"),
                                        dbc.Checklist(
                                            options=[
                                                {"label": "Initial", "value": 1},
                                                {"label": "Loaded", "value": 2}
                                            ],
                                            inline=True,
                                            value=[1,2],
                                            id="pf-checklist"),
                                        dbc.Label("Normal:"),
                                        dbc.RadioItems(
                                            options=[
                                                {'label':'ND', 'value':'ND'},
                                                {'label':'TD', 'value':'TD'},
                                                {'label':'RD', 'value':'RD'}
                                            ],
                                            value = 'ND',
                                            id = 'pf-normal-radiobuttons',
                                            inline = True
                                        )
                                    ],id = 'visibility_pf', style= {'display': 'block'})
                            ],
                            label='Pole Figures', 
                            tab_id = 'tab-pf'
                        ),

                        # Tab - Inverse Pole Figures
                            dbc.Tab(
                                children=[
                                        html.Div([
                                            html.Div([
                                                html.Br(),
                                                dbc.Label("Show:"),
                                                dbc.RadioItems(
                                                    options=[
                                                        {'label':'Initial and Loaded View', 'value':'Initial and Loaded View'},
                                                        {'label':'Animated', 'value':'Animated'},
                                                    ],
                                                    value = 'Animated',
                                                    id = 'ipf-radiobuttons',
                                                    inline = True
                                                )
                                            ],id = 'ipf-radiobuttons-visibility'),
                                            html.Div([
                                                html.Br(),
                                                dbc.Checklist(
                                                    options=[
                                                        {"label": "Initial", "value": 1},
                                                        {"label": "Loaded", "value": 2},
                                                        {"label": "Trajectory", "value": 3}
                                                    ],
                                                    inline=True,
                                                    value=[1,2],
                                                    id="ipf-checklist",
                                                )
                                            ],id = 'ipf-checklist-visibility')
                                    ])
                                ],
                                label='Inverse Pole Figures', 
                                tab_id = 'tab-ipf'
                            ),  

                        # Tab - ODF              
                        dbc.Tab([
                            dbc.Card([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Label("ODF LEVELS"),
                                            dbc.Input(placeholder="2,4,8,12,16,20,25,30,35", type="text", id = 'odf-levels-2'),
                                            dbc.FormText("Separate levels with a comma, without any spaces"),
                                        ]),
                                        dbc.Col([
                                            dbc.Button(id='odf-button-state',
                                                        className = 'btn-success',
                                                        n_clicks=0,
                                                        children='GENERATE ODF',
                                                        style={"margin-top": "33px"})
                                        ])                                        
                                    ]),
                                    dbc.Row([
                                        dls.Pacman(dbc.Col([],id = 'odf-image'),color="#eba134",speed_multiplier=2, fullscreen = True,fullscreen_style={'opacity': '0.7'})
                                    ]), 
                            ], body=True, className= 'border-0', id = 'odf-fields')
                        ],label='ODF', tab_id = 'tab-odf'),

                                   
                        #dbc.Tab(label='Yield Surface', tab_id = 'tab-ys'),
                        # Tab - Yield Surface               
                        dbc.Tab([
                            dbc.Card([
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row([
                                                dbc.Col([
                                                    dbc.Label("X-AXIS"),
                                                    dbc.Input(placeholder="11", type="text", id = 'ys-input-x')
                                                ]),
                                                dbc.Col([
                                                    dbc.Label("Y-AXIS"),
                                                    dbc.Input(placeholder="22", type="text", id = 'ys-input-y')
                                                ]),
                                                dbc.Col([
                                                    dbc.Button(id='ys-button-state',
                                                                className = 'btn-success',
                                                                n_clicks=0,
                                                                children='GENERATE YIELD SURFACE',
                                                                style={"margin-top": "33px"})
                                                ])
                                            ])
                                        ])                                      
                                    ]),
                                    html.Br(),
                                    dbc.Row([
                                        dls.Pacman(dbc.Col([],id = 'ys-content'),color="#eba134",speed_multiplier=2, fullscreen = True,fullscreen_style={'opacity': '0.7'})
                                    ]), 
                    
                            ], body=True, className= 'border-0', id = 'ys-fields')
                        ],label='Yield Surface', tab_id = 'tab-ys'),





                    ],
                        id = 'tabs',
                        active_tab = 'tab-pf'
                    ),
                    dls.Pacman(
                        html.Div(id='tab-content'),
                        color="#eba134",
                        speed_multiplier=2,
                        fullscreen = True,
                        fullscreen_style={'opacity': '0.7'}
                    )
                    ],
                )
            ]),
        ],style=CONTENT_STYLE)

load_figure_template("lux")

# App Layout
app.layout = html.Div([
                sidebar,content,
                dls.Pacman(
                    dcc.Store(id='store'),
                    color="#eba134",
                    speed_multiplier=2,
                    fullscreen=True,
                    fullscreen_style={'opacity': '0.7'})
                ])
                
# App Callback - Tab Contents
@app.callback(
    Output('tab-content','children'),
    Input('tabs','active_tab'),
    Input('store','data'),
    Input('pf-checklist','value'),
    Input('ipf-radiobuttons','value'),
    Input('ipf-checklist','value'),
    Input('pf-normal-radiobuttons', 'value')
)
def render_tab_content(active_tab, data, pf_cl_value,ipf_value, ipf_cl_value, pf_normal_value):
    if (active_tab and data) is not None:

        if active_tab == "tab-pf":

            pf_figure = go.Figure(
                data=[go.Scatter(x = [], y = [], mode='markers', marker=dict(color = '#00256e',size=4), showlegend=False)],
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
                                        marker=dict(color='Black', size =3),
                                        showlegend=False)

            polefigure_initial = data['polefigure_initial']
            polefigure_loaded = data['polefigure_loaded']

            fig_pf_initial_nd = go.Scatter(x = polefigure_initial[0], y = polefigure_initial[3], mode='markers', marker=dict(color = '#bad1ff',size=4), showlegend=False)
            fig_pf_loaded_nd = go.Scatter(x = polefigure_loaded[0], y = polefigure_loaded[3], mode='markers', marker=dict(color = '#00256e',size=4), showlegend=False)

            fig_pf_initial_td = go.Scatter(x = polefigure_initial[1], y = polefigure_initial[4], mode='markers', marker=dict(color = '#bad1ff',size=4), showlegend=False)
            fig_pf_loaded_td = go.Scatter(x = polefigure_loaded[1], y = polefigure_loaded[4], mode='markers', marker=dict(color = '#00256e',size=4), showlegend=False)

            fig_pf_initial_rd = go.Scatter(x = polefigure_initial[2], y = polefigure_initial[5], mode='markers', marker=dict(color = '#bad1ff',size=4), showlegend=False)
            fig_pf_loaded_rd = go.Scatter(x = polefigure_loaded[2], y = polefigure_loaded[5], mode='markers', marker=dict(color = '#00256e',size=4), showlegend=False)

            pf_figure.update_layout(height=700, width=700, title_text = 'FCC (111)',title_x=0.5)

            if pf_cl_value != []:
                if 1 in pf_cl_value:
                    if pf_normal_value == 'ND':
                        pf_figure.add_trace(fig_pf_initial_nd)
                        pf_figure.add_annotation(text='RD', x=0, y=1.1, showarrow=False)
                        pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)
                    elif pf_normal_value == 'TD':
                        pf_figure.add_trace(fig_pf_initial_td)
                        pf_figure.add_annotation(text='RD', x=0, y=1.1, showarrow=False)
                        pf_figure.add_annotation(text='ND', x=-1.1, y=0, showarrow=False)
                    elif pf_normal_value == 'RD':
                        pf_figure.add_trace(fig_pf_initial_rd)
                        pf_figure.add_annotation(text='ND', x=0, y=-1.1, showarrow=False)
                        pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)

                if 2 in pf_cl_value:
                    if pf_normal_value == 'ND':
                        pf_figure.add_trace(fig_pf_loaded_nd)
                        pf_figure.add_annotation(text='RD', x=0, y=1.1, showarrow=False)
                        pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)
                    elif pf_normal_value == 'TD':
                        pf_figure.add_trace(fig_pf_loaded_td)
                        pf_figure.add_annotation(text='RD', x=0, y=1.1, showarrow=False)
                        pf_figure.add_annotation(text='ND', x=-1.1, y=0, showarrow=False)
                    elif pf_normal_value == 'RD':
                        pf_figure.add_trace(fig_pf_loaded_rd)
                        pf_figure.add_annotation(text='ND', x=0, y=-1.1, showarrow=False)
                        pf_figure.add_annotation(text='TD', x=1.1, y=0, showarrow=False)

            pf_figure.add_trace(trace_circle)

            return dcc.Graph(figure = pf_figure) 
                
        elif active_tab == "tab-ipf":

            if ipf_value == 'Animated':
                return dcc.Graph(figure=data['fig_ipf_trajectory'])
                
            elif ipf_value == 'Initial and Loaded View':


                ipf_figure = go.Figure(
                    data=[go.Scatter(x = [], y = [], mode='markers', marker=dict(color = '#00256e',size=4), showlegend=False)],
                    layout = {'xaxis': {'visible': False,
                                        'showticklabels': False},
                            'yaxis': {'visible': False,
                                        'showticklabels': False}
                    }            
                )

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


                ipf_figure.update_layout(xaxis_range=[-0.05, 0.5],yaxis_range=[-0.05, 0.5],height=700, width=700, title_text = 'FCC (111)',title_x=0.5)

                df_inversepolefigure_start = pd.DataFrame(data['inversepolefigure_start'], columns=['grain','x', 'y'])
                df_inversepolefigure_end = pd.DataFrame(data['inversepolefigure_end'], columns=['grain','x', 'y'])
                df_inversepolefigure_trajectory = pd.DataFrame(data['inversepolefigure_trajectory'], columns=['grain','iteration', 'x', 'y'])
 
                ipf_start = go.Scatter(x = df_inversepolefigure_start.loc[:,"x"], y = df_inversepolefigure_start.loc[:,"y"], mode='markers', marker=dict(color = '#bad1ff',size=4), showlegend=False)
                ipf_end = go.Scatter(x = df_inversepolefigure_end.loc[:,"x"], y = df_inversepolefigure_end.loc[:,"y"], mode='markers', marker=dict(color = '#00256e',size=4), showlegend=False)
                ipf_trajectory = go.Scatter(x = df_inversepolefigure_trajectory.loc[:,"x"], y = df_inversepolefigure_trajectory.loc[:,"y"], mode='markers', marker=dict(color = '#00FF00',size=3), showlegend=False)

                if ipf_cl_value != []:
                    if 1 in ipf_cl_value:
                        ipf_figure.add_trace(ipf_start)
                    if 2 in ipf_cl_value:
                        ipf_figure.add_trace(ipf_end)
                    if 3 in ipf_cl_value:
                        ipf_figure.add_trace(ipf_trajectory)

                ipf_figure.add_trace(ipf_trace1)
                ipf_figure.add_trace(ipf_trace2)
                ipf_figure.add_trace(ipf_trace3)
                ipf_figure.add_annotation(text='111', x=0.37, y=0.38, showarrow=False)
                ipf_figure.add_annotation(text='101', x=0.43, y=0, showarrow=False)
                ipf_figure.add_annotation(text='001', x=0, y=0.03, showarrow=False)
                return dcc.Graph(figure=ipf_figure)


    else:
        return html.Br(), dbc.Alert("Update filters then click generate button to generate plots.", color="warning")
    
# App Callback - Process data and generate graphs
@app.callback(
    Output('store','data'),
    Input('generate-button-state','n_clicks'),
    State('input-grain-ori-state','value'),
    State('input-loading-state','value'),
    State('input-euler-phi1','value'),
    State('input-euler-theta','value'),
    State('input-euler-phi2','value'),
    State('uploaded-file','filename'),
    State('ang-threshold','value'),
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
    State('input-number-steps', 'value')
)
def generate_graphs(n_clicks, selected_grain_ori_state, selected_loading_state,
                    euler_phi1, euler_theta, euler_phi2, uploaded_filename, threshold,
                    L_XX, L_XY, L_XZ, L_YX, L_YY, L_YZ,  L_ZX, L_ZY, L_ZZ,
                    S_dir_XX, S_dir_XY, S_dir_XZ, S_dir_YX, S_dir_YY, S_dir_YZ, S_dir_ZX, S_dir_ZY, S_dir_ZZ,
                    S_abs_XX, S_abs_XY, S_abs_XZ, S_abs_YX, S_abs_YY, S_abs_YZ, S_abs_ZX, S_abs_ZY, S_abs_ZZ,
                    tot_von_mises_strain, number_steps):

    return ds.data_source_inputs(selected_grain_ori_state, selected_loading_state, 
                                        euler_phi1, euler_theta, euler_phi2, uploaded_filename, threshold,
                                        L_XX, L_XY, L_XZ, L_YX, L_YY, L_YZ,  L_ZX, L_ZY, L_ZZ,
                                        S_dir_XX, S_dir_XY, S_dir_XZ, S_dir_YX, S_dir_YY, S_dir_YZ, S_dir_ZX, S_dir_ZY, S_dir_ZZ,
                                        S_abs_XX, S_abs_XY, S_abs_XZ, S_abs_YX, S_abs_YY, S_abs_YZ, S_abs_ZX, S_abs_ZY, S_abs_ZZ,
                                        tot_von_mises_strain, number_steps)

# App Callback - Show or hide input of Euler Angles
@app.callback(
   Output('euler-hide','style'),
   Input('input-grain-ori-state','value'),
)
def show_hide_element(visibility_state):
    if visibility_state == "Specify Euler Angles (Bunge's notation in degrees)":
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# App Callback - Show or hide file upload
@app.callback(
   Output('upload-hide','style'),
   Input('input-grain-ori-state','value'),
)
def show_hide_element(visibility_state):
    if visibility_state == "Upload file":
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# App Callback - Show or hide checkboxes in IPF
@app.callback(
   Output('ipf-checklist-visibility','style'),
   Input('ipf-radiobuttons','value'),
)
def show_hide_element(visibility_state):
    if visibility_state == "Initial and Loaded View":
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# App Callback - Show or hide radiobuttons in IPF
@app.callback(
   Output('ipf-radiobuttons-visibility','style'),
   Input('store','data'),
)
def show_hide_element(data):
    if data is not None:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# App Callback - Show or hide checkboxes in PF
@app.callback(
   Output('visibility_pf','style'),
   Input('store','data'),
)
def show_hide_element(data):
    if data is not None:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# App Callback - Show or hide levels field in ODF
@app.callback(
   Output('odf-fields','style'),
   Input('store','data'),
)
def show_hide_element(data):
    if data is not None:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# App Callback - Show or hide levels field in ODF
@app.callback(
   Output('ys-fields','style'),
   Input('store','data'),
)
def show_hide_element(data):
    if data is not None:
        return {'display': 'block'}
    else:
        return {'display': 'none'}

# App Callback - File Upload
@app.callback(
    Output("upload-indicator", "children"),
    Output("upload-indicator", "color"),
    Output("ang-threshold-hide","style"),
    Input("uploaded-file", "filename"),
    Input("uploaded-file", "contents"),
    Input("input-grain-ori-state", "value"),
)
def file_upload(uploaded_filename, uploaded_file_content, selected_grain_ori_state):
    if uploaded_filename is not None and uploaded_file_content is not None:
        if selected_grain_ori_state == 'Upload file':
            if uploaded_filename.endswith('.ori'):
                upload_file.save_file(uploaded_filename, uploaded_file_content)
                result = upload_file.check_uploaded_file(uploaded_filename)
                return result, "success", {'display': 'none'}
            elif uploaded_filename.endswith('.ang'):
                upload_file.save_file(uploaded_filename, uploaded_file_content)
                result = upload_file.check_uploaded_file(uploaded_filename)
                return result, "success", {'display': 'block'}  
            else:
                return "Only .ori or .ang files are allowed. Please try again.", "danger", {'display': 'none'}
        else:
            return "No uploaded files yet.", "warning", {'display': 'none'}
    else:
        return "No uploaded files yet.", "warning", {'display': 'none'}

# App Callback - Show or hide input of custom loading conditions
@app.callback(
   Output('loading-cond-hide','style'),
   Input('input-loading-state','value'),
)
def show_hide_element(visibility_state):
    if visibility_state == "Input Custom Values":
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('odf-image','children'),
    Input('odf-button-state','n_clicks'),
    State('store', 'data'),
    State('odf-levels-2','value')
)
def gen_odf(n_clicks, data, odf_levels):
    default_levels = [2,4,8,12,16,20,25,30,35]

    if data is not None:
        if odf_levels == None:
            odf_levels_list = default_levels
        elif odf_levels == '':
            odf_levels_list = default_levels
        elif odf_levels == []:
            odf_levels_list = default_levels
        else:
            odf_levels_strlist = list(odf_levels.split(","))
            odf_levels_list = [eval(i) for i in odf_levels_strlist]

        ori = odflib.Orientations(angles=data['odf_data'])
        odf = odflib.ODF(orientations=ori)
        image = odf.save_plotly(boundaries=odf_levels_list)
        return html.Img(src = image)
    else:
        return html.Br(),dbc.Alert("Enter ODF levels and click 'Generate ODF'.", color="warning")

@app.callback(
    Output('ys-content','children'),
    Input('ys-button-state','n_clicks'),
    State('store', 'data'),
    State('ys-input-x','value'),
    State('ys-input-y','value')
)
def gen_ys(n_clicks, data, ys_input_x, ys_input_y):
    default_plot_axes = ('11','22')
    plot_axes = ['11','22']
    if data is not None:
        if ys_input_x == None:
            plot_axes[0] = default_plot_axes[0]
        elif ys_input_x == '':
            plot_axes[0] = default_plot_axes[0]
        elif ys_input_x == []:
            plot_axes[0] = default_plot_axes[0]
        else:
            plot_axes[0] = ys_input_x

        if ys_input_y == None:
            plot_axes[1] = default_plot_axes[1]
        elif ys_input_y == '':
            plot_axes[1] = default_plot_axes[1]
        elif ys_input_y == []:
            plot_axes[1] = default_plot_axes[1]
        else:
            plot_axes[1] = ys_input_y

        plot_axes_tup = tuple(plot_axes)
        ys_xvalues, ys_yvalues = ds.ys(plot_axes_tup)

        df_ys = pd.DataFrame(ys_xvalues)
        df_ys[1] = ys_yvalues
        fig_ys = px.scatter(df_ys, x = 0, y = 1,
                            labels={
                                "0": "S"+plot_axes[0],
                                "1": "S"+plot_axes[1],
                            })
        fig_ys.update_layout(xaxis_range=[-36,36],yaxis_range=[-36,36],height=500, width=500)
        return dcc.Graph(figure = fig_ys)

    else:
        return html.Br(),dbc.Alert("Enter plot axes and click generate button. This would take around 2 minutes of loading time to generate.", color="warning")
           

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)