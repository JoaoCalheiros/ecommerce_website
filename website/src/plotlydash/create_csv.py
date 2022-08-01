import pandas as pd 
import numpy as np
import sqlite3
import json
# DB NAME
from ..config import AppConfiguration


def read_my_csv(user_permission, username): 
    '''
    This function will read the CSV file created in create_csv.py
    It will look and see if the user trying to access the Dashboard page
    is either an Admin or Supplier. Based on the user permission and username
    it will read the proper CSV file. For any admin: admin1, admin2, admin3,...
    the CSV file will always be the same. For the Supplier it will check its
    username and then read the CSV associated with that username.
    Since session['property'] cannot be accessed here it will be done later, 
    in every callback. This function is then called with the proper arguments.
    '''
    try:
        if user_permission == 'admin':
            df = pd.read_csv(f'website\src\plotlydash\csvs\\admin.csv')
        elif user_permission == 'supplier':
            df = pd.read_csv(f'website\src\plotlydash\csvs\{username}.csv')
        return df
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()
        print('File is empty')
        return df

def check_table_exists():
    '''
    Check if there registered customer orders alredy. 
    '''
    conn = sqlite3.connect(f'website\src\database\{AppConfiguration.DB_NAME}')
    cur = conn.cursor()
    cur.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='customer_order' ''')
    
    if cur.fetchone()[0]==1 : 
        print('Table exists.')
        conn.commit()
        conn.close()
        return 1
    else :
        print('Table does not exist.')
        conn.commit()
        conn.close()
        return 0


def get_orders():

    '''
       This function will query the Database and get all of the purchases that have been made.
       It will turn the JSON recieved into a Dictionary and then into a List.
       A pay total will be calculated depending on the existence of a discount.       
    '''

    orders_list = []
    orders_dict = {}

    if check_table_exists() == 0:
        print('Purchases Table does not exist yet')
        return orders_list

    conn = sqlite3.connect(f'website\src\database\{AppConfiguration.DB_NAME}')
    cur = conn.cursor()
    # Columns I am interested in working on
    wanted_keys = ['name', 'unit_price', 'unit_cost', 'unit_discount', 'quantity', 'company', 'origin_country', 'brand', 'category', 'purchase_date', 'customer_age']   
    # Remember here - 'orders' is valid json 
    for i in cur.execute('''SELECT orders FROM customer_order'''):
        orders = json.loads(i[0])
        # Calculate the total value (€) of each purchase, applying the discount per unit if necessary.
        for order in orders.values():
            # print('COMPANY', order['company'])
            if order['unit_discount'] == 0:
                order['purchase_pay_total'] = int(order['unit_price']) * int(order['quantity'])
            else:
                order['purchase_pay_total'] = (int(order['unit_price']) - ((int(order['unit_price']) * int(order['unit_discount'])) / 100 )) * int(order['quantity'])
            # Only get the values for the columns i previously defined above - The ones I am interested in.
            orders_dict = {x:order[x] for x in wanted_keys}
            # From dictionary to list in order for me to work with Dataframes.
            orders_list.append(orders_dict)

    conn.commit()
    conn.close()

    return orders_list

def create_all_csv():
    '''
    Create a Dataframe with the List created in get_orders().
    Add new columns date and customer age related as well as calculations for profit, revenue and cost.
    These calculations are simplistic and not representative of a real situation.
    Finally CSV files will be created.
    One for all Admins and one for each supplier registered on the website with their own company products.
    '''

    orders = get_orders()    

    if len(orders) == 0:
        print('NO ORDERS YET REGISTERED')
        df = pd.DataFrame()
        df.to_csv('website\src\plotlydash\csvs\\admin.csv')

    else:
        df = pd.DataFrame(orders)
        df.index.name = 'id' 

        weird_dates = []
        normal_dates = []

        ################ Next 2 for loops are only necessary if DUMMY DATA is inserted into the Database. ################        
        for row in df['purchase_date']:
            weird_dates.append(row)        

        for date in weird_dates:
            if '"' in date:
                date = date[1:-1]
            normal_dates.append(date) 
        df['purchase_date'] = df['purchase_date'].replace(weird_dates, normal_dates)
        ##################################################################################################################
        
        # Create new column for age groups
        conditions = [
            (df['customer_age'] > 0 ) & (df['customer_age'] <= 15),
            (df['customer_age'] > 15 ) & (df['customer_age'] <= 25),
            (df['customer_age'] > 25 ) & (df['customer_age'] <= 65),
            (df['customer_age'] > 65 )]

        values = ['children(0-14)', 'youth(15-24)', 'adults(25-64)', 'senior(65+)']
        df['age_grp'] = np.select(conditions, values)

        # Slice the date col and get year and month cols
        df['purchase_date'] = pd.to_datetime(df['purchase_date'])        
        df['purchase_date'] = pd.to_datetime(df['purchase_date'], format='%Y-%m-%d')
        df['purchase_year'] = pd.to_datetime(df['purchase_date']).dt.year
        df['purchase_month'] = pd.to_datetime(df['purchase_date']).dt.month_name()
        # With quantity, unit cost and unit price I will calculate the revenue, profit and total cost to produce each customer order
        # This calculations are in no way valid/real - This is only for testing purposes
        df['quantity'] = pd.to_numeric(df['quantity'])
        df['unit_cost'] = pd.to_numeric(df['unit_cost'])
        df['order_total_cost'] = df['quantity'] * df['unit_cost']
        df['order_total_revenue'] = df['quantity'] * df['unit_price']
        df['profit'] = df['order_total_revenue'] - df['order_total_cost']
        # Delete discount column, since its no longer necessary
        del df['unit_discount']
        # Now I will create a CSV file for all the purchases for EACH different company (supplier)
        for company in df['company'].unique():        
            df.loc[df['company'] == company].to_csv(f'website\src\plotlydash\csvs\{company}.csv')
        # Finally I will 'manually' create the ADMIN CSV file since this one has ALL of the purchases, from every supplier.
        df.to_csv('website\src\plotlydash\csvs\\admin.csv')
