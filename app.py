import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from layout.layout import layout
from layout.content.content_callbacks import get_callbacks_content
from layout.sidebar.sidebar_callbacks import get_callbacks_sidebar

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server=app.server

load_figure_template("lux")
get_callbacks_content(app)
get_callbacks_sidebar(app)

# App Layout
app.layout = layout

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)

