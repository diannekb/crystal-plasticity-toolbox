from dash import html, dcc
from layout.sidebar.sidebar import sidebar
from layout.content.content import content
import dash_loading_spinners as dls

# This defines the common layout for the application
layout = html.Div([
                sidebar,content,
                dls.Pacman([
                    dcc.Store(id='store_initial'),
                    dcc.Store(id='store_loaded')],
                    color="#eba134",
                    speed_multiplier=2,
                    fullscreen=True,
                    fullscreen_style={'opacity': '0.7'})
                ])