import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go

"""
...
"""


app = dash.Dash()
app.config.suppress_callback_exceptions=True



def create_grouped_df(df_in, group_column_name, target_column, aggregate_type):
    """
    Groups the data by the selected columns and aggregaion types.
    Returns a new df with the grouped data.
    """

    """
    complete...
    """

"""
Change the path below according to the location of the data file
"""
df = pd.read_csv(r"/Users/garyschwartz/Desktop/Dash-Assignment-Files/Pricing Data.csv")

# Automatically update X axis options
@app.callback(
    Output( component_id="x-axis-dropdown", component_property="options"),
    [Input(component_id='aggregate-dropdown', component_property='value')],
)
def update_input(input):
    ddf = df
    row_names = ddf.columns.tolist()
    lst = [{'label': i, 'value': i} for i in row_names]
    return lst

# Automatically update Y axis options
@app.callback(
    Output( component_id="y-axis-dropdown", component_property="options"),
    [Input(component_id='aggregate-dropdown', component_property='value')],
)
def update_input(input):
    # adds in all nominal and numeric variables that are not numbers as columns
    dicti = {
        'Fuel Type' : ['Gasoline', 'Diesel'],
        'Gender' : [ 'M', 'F' ],
        'Car Group' : ['A', 'B', 'C', 'D'],
        'Marital Status' : ['Single', 'Married'],
        'Regional Mlass' : ['P', 'M', 'C']
    }
    for key, items in dicti.items():
        
        for i in items:
            items_dict = {}
            for f in items:
                items_dict[f] = 0
                if i == f:
                    items_dict[f] = 1

            df[f'{key}-{i}-Altered']  = df[key].map(lambda x: items_dict[x])
    miles_dict = {'00K-15K': 0, '16K-20K': 1, '21K+' : 2}
    df['Miles-Altered'] = df['Annual Miles'].map(lambda x: miles_dict[x])
    # adds all columns to options for Y axis
    row_names = df.columns.tolist()
    lst = [{'label': i, 'value': i} for i in row_names]
    return lst

#  automaticallt updates graphs depending on agrigater and if nominal value or not
@app.callback(
    Output("graph-figure", "figure"),
    Input("aggregate-dropdown", "value"),
    Input("x-axis-dropdown", "value"),
    Input("y-axis-dropdown", "value"),
)
def update_graph_1(aggregate_type, x_axis, y_axis):
    if aggregate_type == 'average':
        means = df[[y_axis]].groupby(df[x_axis]).mean()
        df[f'{x_axis}_transformed'] = df[x_axis].apply(lambda x: means.loc[x, y_axis])
    else:
        means = df[[y_axis]].groupby(df[x_axis]).sum()
        df[f'{x_axis}_transformed'] = df[x_axis].apply(lambda x: means.loc[x, y_axis])
    if x_axis not in ['Annual Miles','Car Group','Fuel Type','Gender','Installments','Marital Status','Regional Mlass', 'Year']:
        figure = {
                'data' : [
                    go.Scatter(
                    x = df[x_axis],
                    y = df[f'{x_axis}_transformed'],
                    mode = 'markers'    
                    )
                ],
                'layout' : go.Layout(
                    title = f'{x_axis}-{y_axis} scatter points',
                    xaxis = {'title' : x_axis},
                    yaxis = {'title' : y_axis }
                )
            }
        return figure
    else:
        if aggregate_type != 'average':
            figure = {
                'data' : [
                { 'x' : df[x_axis], 'y' :df[y_axis], 'type': 'bar', 'name' : f'{y_axis} Bar Chart'}
                ],
                'layout' : {
                    'title' : f'Simple {y_axis} Bar Chart'
                }
            }
        else:
            figure = {
                'data' : [
                { 'x' : df[x_axis], 'y' :df[f'{x_axis}_transformed'], 'type': 'bar', 'name' : f'{y_axis} Bar Chart'}
                ],
                'layout' : {
                    'title' : f'Simple {y_axis} Bar Chart'
                }
            }
        return figure



boxplot_layout = (
    dbc.Container(
        [
            html.Div(
                children=[
                    html.H1("Segmented Portfolio Analysis",
                            style={
                               
                            }
                            ),
                ],

            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        html.Div(
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                id="aggregate-dropdown",
                                                                                options=[
                                                                                    {
                                                                                        "label": "Total",
                                                                                        "value": "sum",
                                                                                    },
                                                                                    {
                                                                                        "label": "Average",
                                                                                        "value": "average",
                                                                                    },
                                                                                ],
                                                                                value="sum",
                                                                                style={
                                                                                    "width" : "50%"
                                                                                    
                                                                                },
                                                                            )
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                # This dropdown should include all columns from the data
                                                                                id="y-axis-dropdown",
                                                                                style={
                                                                                    "width" : "50%"
                                                                                    
                                                                                },
                                                                            )
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            html.Label(
                                                                                "by",
                                                                                style={
                                                                                    
                                                                                }

                                                                            )
                                                                        ],
                                                                    ),
                                                                    dbc.Col(
                                                                        [
                                                                            dcc.Dropdown(
                                                                                # This dropdown should include all columns from the data
                                                                                id="x-axis-dropdown",
                                                                                style={
                                                                                    "width" : "50%"
                                                                                    
                                                                                },
                                                                            )
                                                                        ],
                                                                    ),
                                                                ],
                                                            )
                                                        )
                                                    )
                                                ],
                                            ),
                                            html.Div(
                                                dcc.Graph(id="graph-figure"),
                                                style={
                                                        
                                                     }
                                            ),
                                        ]
                                    )
                                ],
                                inverse=True,
                            )
                        ]
                    )
                    ])
        ]
))

app.layout = boxplot_layout 

if __name__ == "__main__":
    app.run_server()