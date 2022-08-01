# Dash dependencies
from dash import dcc
from dash import html
# Create and Read the CSV files created when customer orders have been registered
from .create_csv import read_my_csv, create_all_csv

# Create csv files    
create_all_csv()

# Read the CSV file - The one with all products - Admin version
df = read_my_csv('admin', 'admin')
# print('DF-Admin Version' ,df)  

# The purchase years are the options the admin/supplier has to choose from when in the Dashboard page.
year_options = [] 

# If there are still no orders registered let the df remain empty
if df.empty:
    pass
else:    
    for year in df['purchase_year'].unique():
        year_options.append({
            'label': str(year),
            'value': year})

# Layout
layout = html.Div([
        html.H1('Pick a Year!',
                style={'textAlign': 'center', 'fontFamily': 'monospace', 'fontSize': '15'}),

        html.Div([                         
            dcc.Dropdown(
                id='year_picker',
                options=year_options,
                value=2022
            )],style={'width': '10%', 'margin': 'auto'}),   

        html.Div([
            dcc.Graph(id='histogram_brands')
            ],style={'width':'50%', 'display': 'inline-block'}),  

        html.Div([
            dcc.Graph(id='histogram_categories')
            ],style={'width':'50%', 'display': 'inline-block'}),  

        html.Div([
            dcc.Graph(id='pie_graph_1')
            ],style={'width':'50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='pie_graph_2')
            ],style={'width':'50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='scatter_graph_brands')
            ],style={'width':'50%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='scatter_graph_countries')
            ],style={'width':'50%', 'display': 'inline-block'}),
    
    ],style={'backgroundColor': '#355C7D', 'margin': 'auto', 'border': '5px solid #6C5B7B ', 'padding': '5px'})
