import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import pandas as pd
from dash.dependencies import Input, Output, State

########### Define your variables ######

# here's the list of possible columns to choose from.
list_of_columns =['code', 'state', 'category', 'total exports', 'beef', 'pork', 'poultry',
       'dairy', 'fruits fresh', 'fruits proc', 'total fruits', 'veggies fresh',
       'veggies proc', 'total veggies', 'corn', 'wheat', 'cotton']
#mygraphtitle = '2011 US Agriculture Exports by State'
#mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
#mycolorbartitle = "Millions USD"
tabtitle = 'Agriculture Data Interactive'
sourceurl = 'https://plot.ly/python/choropleth-maps/'
githublink = 'https://github.com/austinlasseter/dash-map-usa-agriculture'


########## Set up the chart

import pandas as pd
df = pd.read_csv('assets/usa-2011-agriculture.csv')



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout

app.layout = html.Div(children=[
    html.H1("Agriculture Data By State - Interactive"),
    html.Div([
        html.Div([
            html.H6("Select option"),
            dcc.Dropdown(
                id="dropdown",
                options=[{'label': i, 'value': i} for i in list_of_columns],
                value='cotton'
            ),
        ],),
        html.Div([dcc.Graph(id='figure-1'),
        ],),
    ],),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)


# make a function that can intake any varname and produce a map.
@app.callback(Output('figure-1', 'figure'),
             [Input('dropdown', 'value')])
def make_figure(varname):
    mygraphtitle = f'Exports of {varname} in 2011'
    mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
    mycolorbartitle = "Millions USD"

    fig = go.Figure(data=go.Choropleth(
        locations=df['code'], # Spatial coordinates
        z = df[varname].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = mycolorscale,
        colorbar_title = mycolorbartitle,
    ))

    fig.update_layout(
        title_text = mygraphtitle,
        geo_scope='usa',
        width=1200,
        height=800
    )
    return fig

############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
