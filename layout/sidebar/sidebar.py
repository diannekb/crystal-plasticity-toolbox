from dash import html, dcc
import dash_bootstrap_components as dbc

# This styles the sidebar to be fixed and always shown in the left of the UI
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

# This defines the layout of the input fields in the sidebar 
sidebar = html.Div([
        # Sidebar Header
        html.H4("Setup"),
        html.Hr(),
        # Expandable/collapsable section in the sidebar for the grain orientation input
        dbc.Accordion([
            dbc.AccordionItem([

                # Dropdown field for the grain orientaion
                dbc.Row([
                    dbc.Col([
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
                    ])
                ]),
                # Input field for Number of Grains
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        dbc.FormFloating([
                            dbc.Input(type = 'number',
                                        min = 1,
                                        max = 100000,
                                        step = 1,
                                        id = 'input-random-num',
                                        value = 100
                            ),
                            dbc.Label("Number of Grains"),
                        ])
                    ])
                ], id = 'random-hide'),
                # Input fields for Euler Angles
                dbc.Row([
                    html.Br(), 
                    dbc.Col([
                        dbc.Row([
                            # Input field for Phi1 Angle
                            dbc.Col([
                                dbc.FormFloating([
                                    dbc.Input(
                                    type = 'number',
                                    min = 0,
                                    max = 360,
                                    step = 0.001,
                                    id = 'input-euler-phi1',
                                    value = 0
                                ),
                                dbc.Label("Phi1"),
                                ])
                            ]),
                            # Input field for Theta Angle
                            dbc.Col([
                                dbc.FormFloating([
                                    dbc.Input(
                                    type = 'number',
                                    min = 0,
                                    max = 180,
                                    step = 0.001,
                                    id = 'input-euler-theta',
                                    value = 0
                                ),
                                dbc.Label("Theta"),
                                ])
                            ]),
                            # Input field for Phi2 Angle
                            dbc.Col([
                                dbc.FormFloating([
                                    dbc.Input(
                                    type = 'number',
                                    min = 0,
                                    max = 360,
                                    step = 0.001,
                                    id = 'input-euler-phi2',
                                    value = 0
                                ),
                                dbc.Label("Phi2"),
                                ])
                            ])  
                        ])
                    ])
                ],id = 'euler-hide'),
                # Input field .ang file threshold
                dbc.Row([ 
                    dbc.Col([
                        html.Br(),
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
                ],id = 'ang-threshold-hide'),
                # Upload file area
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
                        ),
                        dbc.Alert(id="upload-indicator", color="success")
                    ]),       
                ],id = 'upload-hide'),
                # Button to generate initial polycrystal based on values entered in INITIAL section
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        dbc.Button(id='generate-polycrystal-button',
                                    className = 'btn-success',
                                    n_clicks=0,
                                    children='GENERATE POLYCRYSTAL',
                                    style={"margin-left": "10px"})
                    ], style={'textAlign':'right'}),
                ]),
            ],title = 'INITIAL'),
        ], flush = True),
        # Expandable/collapsable section in the sidebar for the loading options
        dbc.Accordion([
            dbc.AccordionItem([
                # Dropdown field for the loading condition
                dbc.Row([
                    dbc.Col([
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
                    ])
                ]),
                # Matrix Input fields for the Global Velocity Gradiebt (L)
                html.Div([
                    html.Br(),
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
                    # Matrix Input fields for the Stress Direction Components
                    html.Br(),
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
                    # Matrix Input fields for the Absolute Stress Components
                    html.Br(),
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
                ],id = 'loading-cond-hide'),
                # Input field for the Total Von Mises Strain
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        dbc.Label("TOTAL VON MISES STRAIN*"),
                        dbc.Input(
                            id = 'input-von-mises-strain',
                            type = 'number',
                            step = 0.001,
                            value = 1
                        )
                    ])
                ]),
                # Input field for the Number of Steps
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        dbc.Label("NUMBER OF STEPS*"),
                        dbc.Input(
                            id = 'input-number-steps',
                            type = 'number',
                            step = 1,
                            value = 100
                        )
                    ])
                ]),
                # Button to generate loaded polycrystal based on values entered in LOAD section
                dbc.Row([
                    dbc.Col([
                        html.Br(),
                        dbc.Button(id='load-polycrystal-button',
                            className = 'btn-success',
                            n_clicks=0,
                            children='LOAD POLYCRYSTAL',
                            style={"margin-left": "10px"})
                    ], style={'textAlign':'right'})
                ])
            ], title = 'LOAD'),
        ], flush = True, start_collapsed=True),
    ],style=SIDEBAR_STYLE)