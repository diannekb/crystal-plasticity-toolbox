from dash import html
import dash_bootstrap_components as dbc
import dash_loading_spinners as dls

# This styles the content to be fixed and always shown in the right of the UI
CONTENT_STYLE = {
    "margin-left": "27rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "overflow": "auto",
}

# This defines the layout of the tabs and generated graphs
content = html.Div([
            html.Div([
                # Content Header
                html.H1("CRYSTAL PLASTICITY TOOLBOX"),
                # This defined the tabs (Pole Figures, Inverse Pole Figures, ODF, Yield Surface)
                dbc.Row([
                    dbc.Tabs([
                        # Tab - Pole Figures
                        dbc.Tab([
                            dbc.Card([
                                # This is for the warning that would be displayed if the polycrystal is not yet loaded.
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Alert("Polycrystal is not loaded. Update load setup to view loaded figures.", color="warning"),
                                        id = 'pf-loaded-warning')
                                ]),
                                dbc.Row([
                                    # Dropdown for the Pole Figure Plane
                                    dbc.Col([
                                        dbc.Label("Plane:"),
                                        dbc.Select(
                                            id = 'pf-plane-input',
                                            options =[
                                                {'label':"FCC (111)", 'value':"FCC_111"},
                                                {'label':"FCC (110)", 'value':"FCC_110"},
                                                {'label':"FCC (100)", 'value':"FCC_100"},
                                                {'label':"FCC (112)", 'value':"FCC_112"},
                                                ],
                                            value = "FCC_111"
                                        )
                                    ], width=3),
                                    # Radio buttons for normal direction of the Pole Figure
                                    dbc.Col([
                                        dbc.Label("Normal:"),
                                        dbc.RadioItems(
                                            options=[
                                                {'label':'ND', 'value':'ND'},
                                                {'label':'TD', 'value':'TD'},
                                                {'label':'RD', 'value':'RD'}
                                            ],
                                            value = 'ND',
                                            id = 'pf-normal-radiobuttons',
                                            #inline = True
                                        )      
                                    ], width=1),
                                    # Checkboxes for showing initial and/or loaded pole figures
                                    dbc.Col([
                                        dbc.Label("Show:", id = 'pf-show'),
                                        dbc.Checklist(
                                            options=[
                                                {"label": "Initial", "value": 1},
                                                {"label": "Loaded", "value": 2}
                                            ],
                                            #inline=True,
                                            value=[1,2],
                                            id="pf-checklist"),
                                    ], width=1),
                                ]),
                                # Loading icon shown when the data is still being generated in the background
                                dbc.Row([
                                    dls.Pacman(dbc.Col([],id = 'pf-content'),color="#eba134",speed_multiplier=2, fullscreen = True,fullscreen_style={'opacity': '0.7'})
                                ]), 
                            ], body=True, className= 'border-0', id = 'pf-inputs')
                        ], label = 'Pole Figures',
                        tab_id = 'tab-pf'
                        ),
                        # Tab - Inverse Pole Figures
                        dbc.Tab([
                            dbc.Card([
                                # This is for the warning that would be displayed if the polycrystal is not yet loaded.
                                dbc.Row([
                                    dbc.Col(
                                        dbc.Alert("Polycrystal is not loaded. Update load setup to view loaded figures.", color="warning"),
                                        id = 'ipf-loaded-warning')
                                ]),
                                # Radio buttons for showing either the animated trajectory or the initial/loaded/trajectory IPF
                                dbc.Row([
                                    dbc.Col([
                                        dbc.Label("Show:"),
                                        dbc.RadioItems(
                                            options=[
                                                {'label':'Initial, Loaded & Trajectory', 'value':'Initial and Loaded View'},
                                                {'label':'Animated Trajectory', 'value':'Animated'},
                                            ],
                                            value = 'Initial and Loaded View',
                                            id = 'ipf-radiobuttons',
                                            inline = True
                                        )
                                    ])
                                ],id = 'ipf-radiobuttons-visibility'),
                                # Checboxes for showing initial/loaded/trajectory IPF
                                dbc.Row([
                                    dbc.Col([
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
                                    ])
                                ],id = 'ipf-checklist-visibility'),
                                # Loading icon shown when the data is still being generated in the background
                                dbc.Row([
                                    dls.Pacman(dbc.Col([],id = 'ipf-content'),color="#eba134",speed_multiplier=2, fullscreen = True,fullscreen_style={'opacity': '0.7'})
                                ]), 
                            ], id = 'ipf-card', body=True, className= 'border-0')
                        ], label='Inverse Pole Figures', tab_id = 'tab-ipf'),  
                        # Tab - ODF              
                        dbc.Tab([
                            dbc.Card([
                                    # This is for the warning that would be displayed if the polycrystal is not yet loaded.
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Alert("Polycrystal is not loaded. Update load setup to view loaded figures.", color="warning"),
                                            id = 'odf-loaded-warning')
                                    ]),
                                    dbc.Row([
                                        # Input field for the ODF levels
                                        dbc.Col([
                                            dbc.Label("ODF Levels"),
                                            dbc.Input(placeholder="2,4,8,12,16,20,25,30,35", type="text", id = 'odf-levels-input'),
                                            dbc.FormText("Separate levels with a comma, without any spaces"),
                                        ], width=4),
                                        # Button to generate the ODF graph
                                        dbc.Col([
                                            dbc.Button(id='odf-button-state',
                                                        className = 'btn-success',
                                                        n_clicks=0,
                                                        children='GENERATE ODF',
                                                        style={"margin-top": "33px"})
                                        ])                                        
                                    ]),
                                    html.Br(),
                                    dbc.Row([
                                        # Loading icon shown when the data is still being generated in the background
                                        dls.Pacman([
                                            dbc.Col([
                                                dbc.Row([
                                                    dbc.Label("Initial ODF:",id = 'odf-initial-label'),
                                                ]),
                                                dbc.Row(id='odf-initial')
                                            ],width = 7),
                                            dbc.Col([
                                                dbc.Row([
                                                    dbc.Label("Loaded ODF:",id = 'odf-loaded-label'),
                                                ]),
                                                dbc.Row(id='odf-loaded')
                                            ],width = 7),
                                        ], color="#eba134",speed_multiplier=2, fullscreen = True,fullscreen_style={'opacity': '0.7'})
                                    ]), 
                            ], body=True, className= 'border-0', id = 'odf-fields')
                        ],label='ODF', tab_id = 'tab-odf'),
                        # Tab - Yield Surface               
                        dbc.Tab([
                            dbc.Card([
                                    # This is for the warning that would be displayed if the polycrystal is not yet loaded.
                                    dbc.Row([
                                        dbc.Col(
                                            dbc.Alert("Polycrystal is not loaded. Update load setup to view loaded figures.", color="warning"),
                                            id = 'ys-loaded-warning')
                                    ]),
                                    # Checkboxes for generating initial and/or loaded yield surface
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Label("Generate yield surface for the following:"),
                                            dbc.Checklist(
                                                options=[
                                                    {"label": "Initial", "value": 1},
                                                    {"label": "Loaded", "value": 2},
                                                ],
                                                inline=True,
                                                value=[1,2],
                                                id="ys-checklist",
                                            ),
                                            html.Br()
                                        ], id = 'ys-checklist-visibility'),
                                    ], id='ys-generate-checklist'),
                                    dbc.Row([
                                        dbc.Col([
                                            dbc.Row([
                                                # Dropdown field for x-axis of yield surface
                                                dbc.Col([
                                                    dbc.Label("X-axis"),
                                                    dbc.Select(
                                                        id = 'ys-input-x',
                                                        options =[
                                                            {'label':"11", 'value':"11"},
                                                            {'label':"12", 'value':"12"},
                                                            {'label':"13", 'value':"13"},
                                                            {'label':"22", 'value':"22"},
                                                            {'label':"23", 'value':"23"},
                                                            {'label':"33", 'value':"33"},
                                                            ],
                                                        value = "11"
                                                    )
                                                ], width=2),
                                                # Dropdown field for y-axis of yield surface
                                                dbc.Col([
                                                    dbc.Label("Y-axis"),
                                                    dbc.Select(
                                                        id = 'ys-input-y',
                                                        options =[
                                                            {'label':"11", 'value':"11"},
                                                            {'label':"12", 'value':"12"},
                                                            {'label':"13", 'value':"13"},
                                                            {'label':"22", 'value':"22"},
                                                            {'label':"23", 'value':"23"},
                                                            {'label':"32", 'value':"32"},
                                                            {'label':"33", 'value':"33"},
                                                            ],
                                                        value = "22"
                                                    )
                                                ], width=2),
                                                # Button to generate yield surface
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
                                    # Loading icon shown when the data is still being generated in the background
                                    dbc.Row([
                                        dls.Pacman(dbc.Col([],id = 'ys-content'),color="#eba134",speed_multiplier=2, fullscreen = True,fullscreen_style={'opacity': '0.7'})
                                    ]), 
                            ], body=True, className= 'border-0', id = 'ys-fields')
                        ],label='Yield Surface', tab_id = 'tab-ys'),
                    ],
                        id = 'tabs',
                        active_tab = 'tab-pf'
                    ),
                    # Loading icon shown when the data is still being generated in the background
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
