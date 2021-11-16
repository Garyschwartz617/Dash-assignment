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
# C:\Users\talc\Documents\pricing data.csv
df = pd.read_csv(r"/Users/garyschwartz/Desktop/Dash Assignment - Files/Pricing Data.csv")
# miles_dict = {'00K-15K': 0, '16K-20K': 1, '21K+' : 2}
# df['Miles-transformed'] = df['Annual Miles'].map(lambda x: miles_dict[x])
# fuel_dict = {'Gasoline': 0, 'Diesel':1}
# df['Fuel-diesel-transformed'] = df['Fuel Type'].map(lambda x: fuel_dict[x])
# fuel_dict = {'Gasoline': 1, 'Diesel':0}
# df['Fuel-gasoline-transformed'] = df['Fuel Type'].map(lambda x: fuel_dict[x])


@app.callback(
    Output( component_id="x-axis-dropdown", component_property="options"),
    [Input(component_id='aggregate-dropdown', component_property='value')],
)
def update_input(input):
    row_names = df.columns.tolist()
    lst = [{'label': i, 'value': i} for i in row_names]
    return lst

@app.callback(
    Output( component_id="y-axis-dropdown", component_property="options"),
    [Input(component_id='aggregate-dropdown', component_property='value')],
)
def update_input(input):
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

            df[f'{key}-{i}-transformed']  = df[key].map(lambda x: items_dict[x])
    miles_dict = {'00K-15K': 0, '16K-20K': 1, '21K+' : 2}
    df['Miles-transformed'] = df['Annual Miles'].map(lambda x: miles_dict[x])
    lst = []
    row_names = df.columns.tolist()
    lst = [{'label': i, 'value': i} for i in row_names]
    # for i in df.columns.tolist():
    #     dicti = {}
    #     dicti['label'] = i
    #     dicti['value'] = i
    #     lst.append(dicti)

    return lst





















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
        # df[[x_axis, 'Age_transformed']].head()
    else:
        means = df[[y_axis]].groupby(df[x_axis]).sum()
        print(means)
        df[f'{x_axis}_transformed'] = df[x_axis].apply(lambda x: means.loc[x, y_axis])
        # df[[x_axis, 'Age_transformed']].head()
    if x_axis not in ['Annual Miles','Car Group','Fuel Type','Gender','Installments','Marital Status','Regional Mlass']:
        figure = {
                'data' : [
                    go.Scatter(
                    # dy =means,
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
            # df['means'] = df[[f'{x_axis}_transformed']].groupby(df[x_axis]).count()
            # df[f'{x_axis}_transformeded'] = df[x_axis].apply(lambda x: means.loc[x, f'{x_axis}_transformed'])

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
                                                                                # options = [
                                                                                #     # {'label' : 'Age', 'value' : 'Age' },
                                                                                #     # {'label' : 'Tenure', 'value' : 'Tenure' },
                                                                                #     # {'label' : 'Annual Miles', 'value' : 'Annual Miles' },
                                                                                #     # {'label' : 'Car Age', 'value' : 'Car Age' },
                                                                                #     # {'label' : 'Car Group', 'value' : 'Car Group' },
                                                                                #     # {'label' : 'Car Value', 'value' : 'Car Value' },
                                                                                #     # {'label' : 'Car Weight', 'value' : 'Car Weight' },
                                                                                #     # {'label' : 'Fuel Type', 'value' : 'Fuel Type' },
                                                                                #     # {'label' : 'Gender', 'value' : 'Gender' },
                                                                                #     # {'label' : 'Installments', 'value' : 'Installments' },
                                                                                #     # {'label' : 'Marital Status', 'value' : 'Marital Status' },
                                                                                #     # {'label' : 'Regional Mlass', 'value' : 'Regional Mlass' },
                                                                                #     # {'label' : 'Risk Class', 'value' : 'Risk Class' },
                                                                                #     # {'label' : 'Year', 'value' : 'Year' },
                                                                                #     # {'label' : 'Variable Cost', 'value' : 'Variable Cost' },
                                                                                #     # {'label' : 'Premium', 'value' : 'Premium' },
                                                                                #     # {'label' : 'Previous Premium', 'value' : 'Previous Premium' },
                                                                                #     # {'label' : 'Margin Parameter', 'value' : 'Margin Parameter' },
                                                                                #     # {'label' : 'Renewal Demand', 'value' : 'Renewal Demand' },
                                                                                #     # {'label' : 'Core Earnings', 'value' : 'Core Earnings' },
                                                                                #     # {'label' : 'Actuarial Cost Parameter', 'value' : 'Actuarial Cost Parameter' },
                                                                                #     # {'label' : 'Base Premium', 'value' : 'Base Premium' },
                                                                                #     # {'label' : 'Individual Discount', 'value' : 'Individual Discount' },
                                                                                #     # {'label' : 'Tax', 'value' : 'Tax' },
                                                                                #     # {'label' : 'Fuel Type Gasoline', 'value' : 'Fuel-gasoline-transformed' },
                                                                                #     # {'label' : 'Fuel Type Diesel', 'value' : 'Fuel-diesel-transformed' },
                                                                                # ],
                                                                                # value= 'Age' ,
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
                                                                                # options = [
                                                                                    # {'label' : 'Age', 'value' : 'Age' },
                                                                                    # {'label' : 'Tenure', 'value' : 'Tenure' },
                                                                                    # {'label' : 'Annual Miles', 'value' : 'Annual Miles' },
                                                                                    # {'label' : 'Car Age', 'value' : 'Car Age' },
                                                                                    # {'label' : 'Car Group', 'value' : 'Car Group' },
                                                                                    # {'label' : 'Car Value', 'value' : 'Car Value' },
                                                                                    # {'label' : 'Car Weight', 'value' : 'Car Weight' },
                                                                                    # {'label' : 'Fuel Type', 'value' : 'Fuel Type' },
                                                                                    # {'label' : 'Gender', 'value' : 'Gender' },
                                                                                    # {'label' : 'Installments', 'value' : 'Installments' },
                                                                                    # {'label' : 'Marital Status', 'value' : 'Marital Status' },
                                                                                    # {'label' : 'Regional Mlass', 'value' : 'Regional Mlass' },
                                                                                    # {'label' : 'Risk Class', 'value' : 'Risk Class' },
                                                                                    # {'label' : 'Year', 'value' : 'Year' },
                                                                                    # {'label' : 'Variable Cost', 'value' : 'Variable Cost' },
                                                                                    # {'label' : 'Premium', 'value' : 'Premium' },
                                                                                    # {'label' : 'Previous Premium', 'value' : 'Previous Premium' },
                                                                                    # {'label' : 'Margin Parameter', 'value' : 'Margin Parameter' },
                                                                                    # {'label' : 'Renewal Demand', 'value' : 'Renewal Demand' },
                                                                                    # {'label' : 'Core Earnings', 'value' : 'Core Earnings' },
                                                                                    # {'label' : 'Actuarial Cost Parameter', 'value' : 'Actuarial Cost Parameter' },
                                                                                    # {'label' : 'Base Premium', 'value' : 'Base Premium' },
                                                                                    # {'label' : 'Individual Discount', 'value' : 'Individual Discount' },
                                                                                    # {'label' : 'Tax', 'value' : 'Tax' },
                                                                                # ],
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


# app.layout = boxplot_layout

app.layout = boxplot_layout 

if __name__ == "__main__":
    app.run_server()