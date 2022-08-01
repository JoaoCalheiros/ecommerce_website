# Get session
from flask import session
# Pandas 
import pandas as pd
# Dash dependencies
from dash.dependencies import Output, Input
# Dashboard graphs
import plotly.express as px
# Read the created CSV files
from .create_csv import read_my_csv


def init_callbacks(dash_app):
    @dash_app.callback(Output('histogram_brands', 'figure'),
            [Input('year_picker', 'value')])
    # HISTOGRAM - Brand
    #===========================================================================#
    def update_histogram_brands(year):

        username = session.get('username', None)
        user_permission = session.get('permission', None)
        df = read_my_csv(user_permission, username)

        base_df = df[(df['purchase_year'] == year)]
        base_df.index.name = 'order_id'
        base_df = base_df[['brand', 'purchase_month', 'purchase_year', 'profit', 'quantity']]

        sorted_months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
        
        fig = px.histogram(
            base_df,
            x='purchase_month',
            y='quantity',
            category_orders=dict(purchase_month=sorted_months),
            color='brand',
            nbins=12)

        fig.update_layout(
            title_text='Purchases per Brand',
            xaxis_title_text='Quantity Sum',
            yaxis_title_text='Purchase Month')

        return fig

    # HISTOGRAM - Category
    #===========================================================================#
    @dash_app.callback(Output('histogram_categories', 'figure'),
                [Input('year_picker', 'value')])
    def update_histogram_categories(year):

        username = session.get('username', None)
        user_permission = session.get('permission', None)
        df = read_my_csv(user_permission, username) 

        base_df = df[(df['purchase_year'] == year)]        
        base_df = base_df[['category', 'purchase_month', 'purchase_year', 'quantity']]

        sorted_months = ['January', 'February', 'March', 'April', 'May', 'June',
                    'July', 'August', 'September', 'October', 'November', 'December']
        
        fig = px.histogram(
            base_df,
            x='purchase_month',
            y='quantity',
            category_orders=dict(purchase_month=sorted_months),
            color='category',
            nbins=12)

        fig.update_layout(
            title_text='Purchases per Category',
            xaxis_title_text='Quantity Sum',
            yaxis_title_text='Purchase Month')
        
        return fig

    # PIE GRAPH
    #===========================================================================#
    @dash_app.callback(Output('pie_graph_1', 'figure'),
                [Input('year_picker', 'value')])
    def update_pie_graph_1(year):

        username = session.get('username', None)
        user_permission = session.get('permission', None)
        df = read_my_csv(user_permission, username)
        
        base_df = df[(df['purchase_year'] == year)]
        base_df = base_df.groupby(['name']).agg({'profit': ['sum']})
        base_df.columns = ['profit_sum']
        base_df = base_df.set_index(base_df.index.get_level_values('name'))
        base_df = base_df.sort_values('profit_sum', ascending=False).head(20)

        fig = px.pie(
            base_df,
            values='profit_sum',
            names=base_df.index,
            title='Top 20 Most Profitable Products')
        return fig

    # PIE GRAPH
    #===========================================================================#
    @dash_app.callback(Output('pie_graph_2', 'figure'),
                [Input('year_picker', 'value')])
    def update_pie_graph_2(year):
        '''
        This plot will change based on the user.
        If Admin, show most profitable Suppliers.
        If Supplier, show most profitable age group.
        '''

        username = session.get('username', None)
        user_permission = session.get('permission', None)
        df = read_my_csv(user_permission, username)

        if user_permission == 'admin':

            base_df = df[(df['purchase_year'] == year)]
            base_df = base_df.groupby(['company']).agg({'profit': ['sum']})
            base_df.columns = ['profit_sum']
            base_df = base_df.set_index(base_df.index.get_level_values('company'))
            base_df = base_df.sort_values('profit_sum', ascending=False)

            fig = px.pie(
                base_df,
                values='profit_sum',
                names=base_df.index,
                title='Most Profitable Supplier')
            return fig
        else:

            base_df = df[(df['purchase_year'] == year)]
            base_df = base_df.groupby(['age_grp']).agg({'profit': ['sum']})
            base_df.columns = ['profit_sum']
            base_df = base_df.set_index(base_df.index.get_level_values('age_grp'))
            base_df = base_df.sort_values('profit_sum', ascending=False)

            fig = px.pie(
                base_df,
                values='profit_sum',
                names=base_df.index,
                title='Most Profitable Age Group')
            return fig

    # SCATTER GRAPH
    #===========================================================================#
    @dash_app.callback(Output('scatter_graph_brands', 'figure'),
                [Input('year_picker', 'value')])
    def update_scatter_graph_brands(year):

        username = session.get('username', None)
        user_permission = session.get('permission', None)
        df = read_my_csv(user_permission, username)

        base_df = df[(df['purchase_year'] == year)]
        base_df = base_df.groupby(['brand', 'category',]).agg({'profit': ['mean', 'sum'], 'quantity': ['mean', 'sum']})
        base_df.columns = ['profit_mean', 'profit_sum', 'quantity_mean', 'quantity_sum']

        fig = px.scatter(
            base_df,
            x='profit_sum',
            y='quantity_sum',
            color=base_df.index.get_level_values('brand'),
            size='profit_mean',
            hover_name=base_df.index.get_level_values('category'),
            title='Profit & Quantity (Nr of purchases) - Per Brand',
            labels=dict(
                profit_sum='Profit Sum',
                quantity_sum='Quantity Sum'))
        return fig

    # SCATTER GRAPH
    #===========================================================================#
    @dash_app.callback(Output('scatter_graph_countries', 'figure'),
                [Input('year_picker', 'value')])
    def update_scatter_graph_countries(year):

        username = session.get('username', None)
        user_permission = session.get('permission', None)
        df = read_my_csv(user_permission, username)

        base_df = df[(df['purchase_year'] == year)]
        base_df = base_df.groupby(['name', 'origin_country',]).agg({'profit': ['mean', 'sum'], 'quantity': ['mean', 'sum']})
        base_df.columns = ['profit_mean', 'profit_sum', 'quantity_mean', 'quantity_sum']

        fig = px.scatter(
            base_df,
            x='profit_sum',
            y='quantity_sum',
            color=base_df.index.get_level_values('origin_country'),
            size='profit_mean',
            hover_name=base_df.index.get_level_values('name'),
            title='Profit & Quantity (Nr of purchases) - Per Country',
            labels=dict(
                profit_sum='Profit Sum',
                quantity_sum='Quantity Sum'))
        return fig
