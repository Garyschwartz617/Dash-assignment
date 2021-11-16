import dash
import plotly.express as px
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objs as go

app = dash.Dash()

df = pd.read_csv(r"/Users/garyschwartz/Desktop/Dash Assignment - Files/Pricing Data.csv")
a = df.Age
# df.Age
# means = df[['Premium']].groupby(a).mean()
def update_graph_1(aggregate_type, x_axis, y_axis):
    if aggregate_type == 'average':
        means = df[[y_axis]].groupby(df[x_axis]).mean()
        df[f'{x_axis}_transformed'] = df[x_axis].dropna().apply(lambda x: means.loc[x, y_axis])
        df[[x_axis, 'Age_transformed']].head()
    else:
        means = df[[y_axis]].groupby(df[x_axis]).sum()
        df[f'{x_axis}_transformed'] = df[x_axis].dropna().apply(lambda x: means.loc[x, y_axis])
        df[[x_axis, 'Age_transformed']].head()
    
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
                title = 'scatter points',
                xaxis = {'title' : x_axis},
                yaxis = {'title' : y_axis }
            )
        }
    return figure




# app.layout = html.Div([
#     dcc.Graph(
#         id = 'scatter_chart',
#         figure =update_graph_1('averaçe','Age','Premium')
#     )
# ])

# if __name__ == '__main__':
#     app.run_server()

a = df.Age

# means = df[['Premium']].groupby(a).mean()
# df['Age_transformed'] = df['Age'].dropna().apply(lambda x: means.loc[x, "Premium"])
# df[['Age', 'Age_transformed']].head()

# figure = {
#         'data' : [
#             go.Scatter(
#             # dy =means,
#             x = df['Age'],
#             y = df['Age_transformed'],
#             mode = 'markers'    
#             )
#         ],
#         'layout' : go.Layout(
#             title = 'scatter points',
#             xaxis = {'title' : 'Age'},
#             yaxis = {'title' : 'Premium' }
#         )
#     }


means = df[['Margin Parameter']].groupby(df['Car Group']).sum()
df['Car group_transformed'] = df['Car Group'].dropna().apply(lambda x: means.loc[x, "Margin Parameter"])
df[['Car Group', 'Car group_transformed']].head()


# figure = {
#         'data' : [
#            { 'x' : df['Car Group'], 'y' :df['Car group_transformed']], 'type': 'bar', 'name' : 'Bar Chart'}
#         ],
#         'layout' : {
#             'title' : 'Simple Bar Chart'
#         }
#     }



# app.layout = html.Div([
#     dcc.Graph(
#         id = 'Bar_chart',
#         figure = {
#         'data' : [
#            { 'x' : df['Car Group'], 'y' :df['Car group_transformed'], 'type': 'bar', 'name' : 'Bar Chart'}
#         ],
#         'layout' : {
#             'title' : 'Simple Bar Chart'
#         }
#     }

#     )
# ])

miles_dict = {'00K-15K': 0, '16K-20K': 1, '21K+' : 2}
df['Miles-transformed'] = df['Annual Miles'].map(lambda x: miles_dict[x])

fuel_dict = {'Gasoline': 0, 'Diesel':1}
df['Fuel-Diesel-transformed'] = df['Fuel Type'].map(lambda x: fuel_dict[x])
fuel_dict = {'Gasoline': 1, 'Diesel':0}
df['Fuel-gasoline-transformed'] = df['Fuel Type'].map(lambda x: fuel_dict[x])

gender_dict = {'M': 0, 'F':1}
df['Gender-female-transformed'] = df['Gender'].map(lambda x: gender_dict[x])
gender_dict = {'M': 1, 'F':0}
df['Gender-male-transformed'] = df['Gender'].map(lambda x: gender_dict[x])

gender_dict = {'A': 1, 'B':0, 'C': 0, 'D':0}
df['Car-a-transformed'] = df['Car Group'].map(lambda x: gender_dict[x])
gender_dict = {'A': 0, 'B':1, 'C': 0, 'D':0}
df['Car-b-transformed'] = df['Car Group'].map(lambda x: gender_dict[x])
gender_dict = {'A': 0, 'B':0, 'C': 1, 'D':0}
df['Car-c-transformed'] = df['Car Group'].map(lambda x: gender_dict[x])
gender_dict = {'A': 0, 'B':0, 'C': 0, 'D':1}
df['Car-d-transformed'] = df['Car Group'].map(lambda x: gender_dict[x])


gender_dict = {'Single': 1, 'Married':0}
df['Single-transformed'] = df['Marital Status'].map(lambda x: gender_dict[x])
gender_dict = {'Single': 0, 'Married':1}
df['Married-transformed'] = df['Marital Status'].map(lambda x: gender_dict[x])


gender_dict = {'P': 1, 'M': 0, 'C': 0}
df['Mlass-p-transformed'] = df['Regional Mlass'].map(lambda x: gender_dict[x])
gender_dict = {'P': 0, 'M': 1, 'C': 0}
df['Mlass-m-transformed'] = df['Regional Mlass'].map(lambda x: gender_dict[x])
gender_dict = {'P': 0, 'M': 0, 'C': 1}
df['Mlass-c-transformed'] = df['Regional Mlass'].map(lambda x: gender_dict[x])

# print(df['Fuel Type'].unique())
# print(df['Car Group'].unique())
# print(df['Marital Status'].unique())
# print(df['Regional Mlass'].unique())

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

# print(df.columns)
for i in df.columns:
    print(i)
# print(df['Annual Miles'], df['Miles-transformed'])


def update_input():
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
    for i in df.columns.tolist():
        dicti = {}
        dicti['label'] = i
        dicti['value'] = i
        lst.append(dicti)

    print(lst)    
    return lst
update_input()
# means = df[['Age']].groupby(df['Car Group']).mean()
# df['Age_transformed'] = df['Car Group'].dropna().apply(lambda x: means.loc[x, 'Age'])


# barchart = px.bar(
#     # data_frame= df,
#     x= df['Car Group'],
#     y = df['Age_transformed'],
#     title=  'car-age bar chart'


# )





# app.layout = html.Div([
#     dcc.Graph(id = 'the_graph')
# ])

# @app.callback(
#     Output(component_id='the_graph',component_property='figure')
# )
# def update_graph():
#     barchart = px.bar(
#     # data_frame= df,
#     x= df['Car Group'],
#     y = df['Age_transformed'],
#     title=  'car-age bar chart'
#     )   
#     return barchart 



# gender_dict = {'M': 0, 'F':1}
# # encoded_items = items.map(lambda x: size_dict[x])
# df['Gender-transformed'] = df.Gender.map(lambda x: gender_dict[x])
# df[['Gender', 'Gender-transformed']].head()
# print(df['Gender-transformed'])
if __name__ == '__main__':
    app.run_server()



