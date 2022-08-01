# Generate random data
from faker import Faker
import secrets
import random
import json
import datetime
import sqlite3
# Operate on files
import shutil

'''
Database must be empty (exception being the Admin table) in order to insert this dummy data.
Every user (no matter its type) will have a password of '123'.
Changes must be made in the routes in order to be able to log in with a dummy user.
In order to use the Cart functionality the following must be added to the Database:
    - Products
    - Brands
    - Categories
    - Suppliers
'''
fake = Faker()

imgs = []
path = "website\src\dummy_data\dummy_images"
valid_images = [".jpg",".gif",".png",".jpeg"]

faker = Faker('pt-PT')

def convert_to_binary(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        b_data = file.read()
    return b_data

def insert_to_products(products_list):
    try:
        conn = sqlite3.connect(f'website\src\database\\test.db')
        cur = conn.cursor()
        print('Connected to Database')
        insert_query = '''
        INSERT INTO products_table
        (id, name, inventory, origin_country, colors, brand_id, category_id, image, unit_price, unit_cost, unit_discount, company, description)
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
        n = 0
        for list_item in products_list:
            #print('LIST ITEM', list_item)
            for i in range(len(list_item)):
                if str(list_item[i]).endswith(('.jpg', '.png', '.jpeg', '.gif')):
                    img_name = str(list_item[i]).split('\\')[4]
                    src_dir = str(list_item[i])
                    dst_dir = "website\src\static\\" + str(img_name)
                    list_item[i] = img_name
                    shutil.copyfile(src_dir, dst_dir)        
                else:
                    continue            
            # Convert data into tuple format
            tup_data = tuple(list_item)       
            cur.execute(insert_query, tup_data)
            conn.commit()
        cur.close()
        print('Success!')
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")   
    
def insert_to_brands(brands_list):
    try:
        conn = sqlite3.connect(f'website\src\database\\test.db')
        cur = conn.cursor()
        print('Connected to Database')
        insert_query = '''
        INSERT INTO brand
        (id, brand_name)
        VALUES
        (?, ?)'''
        for list_item in brands_list:
            # print('LIST ITEM', list_item)
            
            tup_data = tuple(list_item)       
            cur.execute(insert_query, tup_data)
            conn.commit()
        cur.close()
        print('Success')
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")               

def insert_to_categories(categories_list):
    try:
        conn = sqlite3.connect(f'website\src\database\\test.db')
        cur = conn.cursor()
        print('Connected to Database')
        insert_query = '''
        INSERT INTO category
        (id, category_name)
        VALUES
        (?, ?)'''
        for list_item in categories_list:
            # print('LIST ITEM', list_item)
            
            tup_data = tuple(list_item)       
            cur.execute(insert_query, tup_data)
            conn.commit()
        cur.close()
        print('Success!')
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed") 

def insert_to_suppliers(suppliers_list):
    try:
        conn = sqlite3.connect(f'website\src\database\\test.db')
        cur = conn.cursor()
        print('Connected to Database')
        insert_query = '''
        INSERT INTO suppliers_table
        (id, name, address,  zip_code, email, phone_contact_1, phone_contact_2, password, logo, date_created, permission)
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        for list_item in suppliers_list:
            # print('LIST ITEM', list_item)
            for i in range(len(list_item)):
                if str(list_item[i]).endswith(('.jpg', '.png', '.jpeg', '.gif')):
                    img_name = str(list_item[i]).split('\\')[4]
                    src_dir = str(list_item[i])
                    dst_dir = "website\src\static\\" + str(img_name)
                    list_item[i] = img_name
                    shutil.copyfile(src_dir, dst_dir)        
                else:
                    continue            
            tup_data = tuple(list_item)       
            cur.execute(insert_query, tup_data)
            conn.commit()            
        cur.close()
        print('Success!')
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed") 

def insert_to_customers(customers_list):
    try:
        conn = sqlite3.connect(f'website\src\database\\test.db')
        cur = conn.cursor()
        print('Connected to Database')
        insert_query = '''
        INSERT INTO customers_table
        (id, first_name, last_name, username, age, email, country, city, district, current_address, zip_code, phone_contact, password, profile_pic, date_created, permission)
        VALUES
        (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''

        for list_item in customers_list:
            # print('LIST ITEM', list_item)
            for i in range(len(list_item)):
                if str(list_item[i]).endswith(('.jpg', '.png', '.jpeg', '.gif')):
                    img_name = str(list_item[i]).split('\\')[4]
                    src_dir = str(list_item[i])
                    dst_dir = "website\src\static\\" + str(img_name)
                    list_item[i] = img_name
                    shutil.copyfile(src_dir, dst_dir)        
                else:
                    continue            
            tup_data = tuple(list_item)       
            cur.execute(insert_query, tup_data)
            conn.commit()
        cur.close()
        print('Success')
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed") 

def insert_to_orders(orders_list):
    try:
        conn = sqlite3.connect(f'website\src\database\\test.db')
        cur = conn.cursor()
        print('Connected to Database')
        insert_query = '''
        INSERT INTO customer_order
        (id, code, status, customer_id, date_created, orders)
        VALUES
        (?, ?, ?, ?, ?, ?)'''
        for list_item in orders_list:
            #print('LIST ITEM', list_item)
            
            tup_data = tuple(list_item)       
            cur.execute(insert_query, tup_data)
            conn.commit()
        cur.close()
        print('Success')
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("the sqlite connection is closed")    


# Uncomment each one of the function calls bellow to add dummy data to the Database

# ORDERS

""" insert_to_orders([
    [1, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({1:{'brand': 'Apple', 'category': 'mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'CGeneric', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\\apple_mobile.jpg', 'name': 'iPhone 17', 'origin_country': 'China', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(25, 250), 'unit_discount': random.randint(0, 10), 'unit_price': random.randint(900, 1750)}})],
    [2, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({2:{'brand': 'Apple', 'category': 'mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'KangTao', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\\apple_mobile_2.jpg', 'name': 'iPhone 15 S+', 'origin_country': 'China', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(35, 250), 'unit_discount': random.randint(0, 12), 'unit_price': random.randint(850, 1600)}})],
    [3, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({3:{'brand': 'Apple', 'category': 'Desktop', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\\apple-desktop.jpg', 'name': 'iMac 250+', 'origin_country': 'Taiwan', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 500), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1200, 2600)}})],
    [4, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({4:{'brand': 'Apple', 'category': 'Laptop', 'color': 'black', 'colors': 'black, silver', 'company': 'KangTao', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\\apple-laptop.jpg', 'name': 'MacBook PRO', 'origin_country': 'China', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(150, 500), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1000, 2000)}})],
    [5, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')),
    json.dumps({5:{'brand': 'Canon', 'category': 'Photography', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85), 
    'image': 'src\dummy_data\dummy_images\canon-1.jpg', 'name': 'Canon Camera HD', 'origin_country': 'Italy', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 100), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1500, 5000)}})],
    [6, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({6:{'brand': 'Canon', 'category': 'Photography', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\canon-2.jpg', 'name': 'Canon 4k Plus', 'origin_country': 'Germany', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 100), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1500, 5000)}})],
    [7, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({7:{'brand': 'Canon', 'category': 'Photography', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\canon-3.jpg', 'name': 'Canon Ultra Lens', 'origin_country': 'Germany', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 100), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1500, 5000)}})],
    [8, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({8:{'brand': 'Canon', 'category': 'Photography', 'color': 'black', 'colors': 'black, silver', 'company': 'CGeneric', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\canon-4.jpg', 'name': 'Canon Ultra HD', 'origin_country': 'Spain', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 100), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1500, 5000)}})],
    [9, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({9:{'brand': 'Canon', 'category': 'Photography', 'color': 'black', 'colors': 'black, silver', 'company': 'KangTao', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\canon-5.jpg', 'name': 'Canon Selfie Expert', 'origin_country': 'Spain', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 100), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1500, 5000)}})],
    [10, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({10:{'brand': 'Canon', 'category': 'Photography', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\canon-6.jpg', 'name': 'Canon 1080P', 'origin_country': 'Germany', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 100), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1500, 5000)}})],
    [11, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({11:{'brand': 'Samsung', 'category': 'Mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'CGeneric', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\samsung_mobile_1.jpg', 'name': 'Samsung Galaxy 8900', 'origin_country': 'Japan', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 300), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(550, 2000)}})],
    [12, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({12:{'brand': 'Samsung', 'category': 'Mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\samsung_mobile_2.jpg', 'name': 'Samsung Moon 7000', 'origin_country': 'Japan', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 300), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(550, 2000)}})],
    [13, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({13:{'brand': 'Samsung', 'category': 'Mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'KangTao', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\samsung_mobile_3.jpg', 'name': 'Samsung Mars 420', 'origin_country': 'Japan', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 300), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(550, 2000)}})],
    [14, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({14:{'brand': 'Samsung', 'category': 'Mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\samsung_mobile_4.jpg', 'name': 'Samsung Galaxy Lite', 'origin_country': 'Japan', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 300), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(550, 1000)}})],
    [15, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({15:{'brand': 'Samsung', 'category': 'Mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\samsung_mobile_5.jpg', 'name': 'Samsung Galaxy A13', 'origin_country': 'Japan', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 300), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(550, 1000)}})],
    [16, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({16:{'brand': 'Dell', 'category': 'Desktop', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\dell_desktop_2.jpg', 'name': 'Desktop DELL OptiPlex', 'origin_country': 'Spain', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(150, 350)}})],
    [17, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({17:{'brand': 'Dell', 'category': 'Desktop', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\dell_desktop_3.jpg', 'name': 'Desktop DELL UltraFat', 'origin_country': 'Spain', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(150, 350)}})],
    [18, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({18:{'brand': 'Dell', 'category': 'Desktop', 'color': 'black', 'colors': 'black, silver', 'company': 'KangTao', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\dell_desktop.jpg', 'name': 'Desktop DELL Optilex 7020', 'origin_country': 'Italy', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(150, 350)}})],
    [19, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({19:{'brand': 'Dell', 'category': 'Gaming', 'color': 'black', 'colors': 'black, silver', 'company': 'KangTao', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\dell_monitor.png', 'name': 'Gaming Monitor 5000', 'origin_country': 'China', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(150, 250)}})],
    [20, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({20:{'brand': 'Sony', 'category': 'Gaming', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\sony_gaming.png', 'name': 'SONY Pulse 3D', 'origin_country': 'China', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(50, 100)}})],
    [21, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({21:{'brand': 'Razer', 'category': 'Gaming', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\\razer_gaming.jpg', 'name': 'RAZER Ornata V2', 'origin_country': 'Germany', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(50, 100)}})],
    [22, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({22:{'brand': 'Razer', 'category': 'Gaming', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\\razer_gaming_2.jpg', 'name': 'RAZER Deathadder', 'origin_country': 'Germany', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(50, 100)}})],
    [23, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({23:{'brand': 'Razer', 'category': 'Gaming', 'color': 'black', 'colors': 'black, silver', 'company': 'CGeneric', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\\razer_gaming_3.jpg', 'name': 'RAZER Viper Mini', 'origin_country': 'Italy', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(50, 100)}})],
    [24, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({24:{'brand': 'Razer', 'category': 'Gaming', 'color': 'black', 'colors': 'black, silver', 'company': 'KangTao', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\\razer_gaming_4.jpg', 'name': 'RAZER HeadPhones', 'origin_country': 'Italy', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(50, 100)}})],
    [25, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({25:{'brand': 'Huawei', 'category': 'Mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'KangTao', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\huawei_mobile.jpg', 'name': 'Huawei X-25', 'origin_country': 'China', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 300), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(850, 1200)}})],
    [26, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({26:{'brand': 'Huawei', 'category': 'Mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'CGeneric', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\huwei_mobile_2.jpg', 'name': 'Huawei Y-16', 'origin_country': 'China', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 300), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(850, 1200)}})],
    [27, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({27:{'brand': 'LG', 'category': 'Laptop', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\lg_laptop.jpg', 'name': 'LG-Omen', 'origin_country': 'Germany', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 300), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1000, 1200)}})],
    [28, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({28:{'brand': 'LG', 'category': 'Mobile', 'color': 'black', 'colors': 'black, silver', 'company': 'KangTao', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\lg_mobile_1.jpg', 'name': 'LG Moba', 'origin_country': 'Germany', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(50, 300), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(1000, 1200)}})],
    [29, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')),
    json.dumps({29:{'brand': 'GOODIS', 'category': 'Electrical Appliance', 'color': 'pink', 'colors': 'black, silver, pink', 'company': 'CGeneric', 'customer_age': random.randint(10, 85), 
    'image': 'src\dummy_data\dummy_images\extras.png', 'name': 'iPad Cape', 'origin_country': 'Germany', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(40, 100)}})],
    [30, secrets.token_hex(5), 'Pending', random.randint(1, 20), str(faker.date_time_between(start_date='-2y', end_date='now')), 
    json.dumps({30:{'brand': 'GOODIS', 'category': 'Electrical Appliance', 'color': 'black', 'colors': 'black, silver', 'company': 'Tecbite', 'customer_age': random.randint(10, 85),
    'image': 'src\dummy_data\dummy_images\extras_2.png', 'name': 'Apple Pencil', 'origin_country': 'China', 'purchase_date': str(faker.date_time_between(start_date='-2y', end_date='now')),
    'quantity': random.randint(1, 5), 'unit_cost': random.randint(20, 50), 'unit_discount': random.randint(0, 5), 'unit_price': random.randint(75, 200)}})]
])
 """

# PRODUCTS
""" 
insert_to_products([
    [1, 'iPhone 17', random.randint(10, 100), 'China', 'black, silver, white', 1, 3, 'website\src\dummy_data\dummy_images\\apple_mobile.jpg', random.randint(800, 1500), random.randint(100, 200), random.randint(0, 5), 'CGeneric', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [2, 'iPhone 15 S+', random.randint(10, 100), 'Germany', 'black, dark', 1, 3, 'website\src\dummy_data\dummy_images\\apple_mobile.jpg', random.randint(800, 1500), random.randint(100, 200), random.randint(0, 5), 'KangTao', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [3, 'iMac 250+', random.randint(10, 100), 'China', 'black, silver, white', 1, 2, 'website\src\dummy_data\dummy_images\\apple-desktop.jpg', random.randint(1000, 1800), random.randint(100, 350), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [4, 'MacBook PRO', random.randint(10, 100), 'Germany', 'black, dark', 1, 1, 'website\src\dummy_data\dummy_images\\apple-laptop.jpg', random.randint(1000, 1500), random.randint(100, 350), random.randint(0, 5), 'KangTao', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [5, 'Canon Camera HD', random.randint(10, 100), 'China', 'black, silver, white', 8, 7, 'website\src\dummy_data\dummy_images\canon-1.jpg', random.randint(800, 1200), random.randint(100, 200), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [6, 'Canon 4k Plus', random.randint(10, 100), 'Germany', 'black, dark', 8, 7, 'website\src\dummy_data\dummy_images\canon-2.jpg', random.randint(800, 1200), random.randint(100, 200), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [7, 'Canon Ultra Lens', random.randint(10, 100), 'China', 'black, silver, white', 8, 7, 'website\src\dummy_data\dummy_images\canon-3.jpg', random.randint(800, 1200), random.randint(100, 200), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [8, 'Canon Ultra HD', random.randint(10, 100), 'Germany', 'black, dark', 8, 7, 'website\src\dummy_data\dummy_images\canon-4.jpg', random.randint(800, 1200), random.randint(100, 200), random.randint(0, 5), 'CGeneric', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [9, 'Canon Selfie Expert', random.randint(10, 100), 'China', 'black, silver, white', 8, 7, 'website\src\dummy_data\dummy_images\canon-5.jpg', random.randint(800, 1200), random.randint(100, 200), random.randint(0, 5), 'KangTao', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [10, 'Canon 1080P', random.randint(10, 100), 'Germany', 'black, dark', 8, 7, 'website\src\dummy_data\dummy_images\canon-6.jpg', random.randint(800, 1200), random.randint(100, 200), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [11, 'Samsung Galaxy 8900', random.randint(10, 100), 'China', 'black, silver, white', 2, 3, 'website\src\dummy_data\dummy_images\samsung_mobile_1.jpg', random.randint(800, 1350), random.randint(100, 300), random.randint(0, 5), 'CGeneric', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [12, 'Samsung Moon 7000', random.randint(10, 100), 'Germany', 'black, dark', 2, 3, 'website\src\dummy_data\dummy_images\samsung_mobile_2.jpg', random.randint(800, 1350), random.randint(100, 300), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [13, 'Samsung Mars 420', random.randint(10, 100), 'China', 'black, silver, white', 2, 3, 'website\src\dummy_data\dummy_images\samsung_mobile_3.jpg', random.randint(800, 1350), random.randint(100, 300), random.randint(0, 5), 'KangTao', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [14, 'Samsung Galaxy Lite', random.randint(10, 100), 'Germany', 'black, dark', 2, 3, 'website\src\dummy_data\dummy_images\samsung_mobile_4.jpg', random.randint(800, 1350), random.randint(100, 300), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [15, 'Samsung Galaxy A13', random.randint(10, 100), 'China', 'black, silver, white', 2, 3, 'website\src\dummy_data\dummy_images\samsung_mobile_5.jpg', random.randint(800, 1350), random.randint(100, 300), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [16, 'Desktop DELL OptiPlex', random.randint(10, 100), 'Germany', 'black, dark', 5, 2, 'website\src\dummy_data\dummy_images\dell_desktop_2.jpg', random.randint(800, 1350), random.randint(100, 300), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [17, 'Desktop DELL UltraFat', random.randint(10, 100), 'China', 'black, silver, white', 5, 2, 'website\src\dummy_data\dummy_images\dell_desktop_3.jpg', random.randint(800, 1350), random.randint(100, 300), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [18, 'Desktop DELL Optilex 7020', random.randint(10, 100), 'Germany', 'black, dark', 5, 2, 'website\src\dummy_data\dummy_images\dell_desktop.jpg', random.randint(800, 1350), random.randint(100, 300), random.randint(0, 5), 'KangTao', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [19, 'Gaming Monitor 5000', random.randint(10, 100), 'China', 'black, silver, white', 5, 4, 'website\src\dummy_data\dummy_images\dell_monitor.png', random.randint(250, 400), random.randint(50, 100), random.randint(0, 5), 'KangTao', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [20, 'SONY Pulse 3D', random.randint(10, 100), 'Germany', 'black, dark', 7, 4, 'website\src\dummy_data\dummy_images\sony_gaming.png', random.randint(100, 200), random.randint(20, 50), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [21, 'RAZER Ornata V2', random.randint(10, 100), 'China', 'black, silver, white', 6, 4, 'website\src\dummy_data\dummy_images\\razer_gaming.jpg', random.randint(100, 200), random.randint(20, 50), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [22, 'RAZER Deathadder', random.randint(10, 100), 'Germany', 'black, dark', 6, 4, 'website\src\dummy_data\dummy_images\\razer_gaming_2.jpg', random.randint(100, 200), random.randint(20, 50), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [23, 'RAZER Viper Mini', random.randint(10, 100), 'China', 'black, silver, white', 6, 4, 'website\src\dummy_data\dummy_images\\razer_gaming_3.jpg', random.randint(100, 200), random.randint(20, 50), random.randint(0, 5), 'CGeneric', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [24, 'RAZER HeadPhones', random.randint(10, 100), 'Germany', 'black, dark', 6, 5, 'website\src\dummy_data\dummy_images\\razer_gaming_4.jpg', random.randint(100, 200), random.randint(20, 50), random.randint(0, 5), 'KangTao', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [25, 'Huawei X-25', random.randint(10, 100), 'China', 'black, silver, white', 3, 3, 'website\src\dummy_data\dummy_images\huawei_mobile.jpg', random.randint(800, 1500), random.randint(100, 200), random.randint(0, 5), 'KangTao', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [26, 'Huawei Y-16', random.randint(10, 100), 'Germany', 'black, dark', 3, 3, 'website\src\dummy_data\dummy_images\huwei_mobile_2.jpg', random.randint(800, 1500), random.randint(100, 200), random.randint(0, 5), 'CGeneric', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [27, 'LG-Omen', random.randint(10, 100), 'China', 'black, silver, white', 4, 1, 'website\src\dummy_data\dummy_images\lg_laptop.jpg', random.randint(800, 1500), random.randint(100, 200), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [28, 'LG Moba', random.randint(10, 100), 'Germany', 'black, dark', 4, 1, 'website\src\dummy_data\dummy_images\lg_mobile_1.jpg', random.randint(800, 1500), random.randint(100, 200), random.randint(0, 5), 'KangTao', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [29, 'iPad Cape', random.randint(10, 100), 'China', 'black, silver, white', 9, 10, 'website\src\dummy_data\dummy_images\extras.png', random.randint(100, 200), random.randint(20, 50), random.randint(0, 5), 'CGeneric', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'],
    [30, 'Apple Pencil', random.randint(10, 100), 'Germany', 'black, dark', 9, 10, 'website\src\dummy_data\dummy_images\lg_mobile_1.jpg', random.randint(100, 200), random.randint(20, 50), random.randint(0, 5), 'Tecbite', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.']
    ]) """


# BRANDS / CATEGORIES

""" categories = ['Laptop', 'Desktop', 'Mobile', 'Gaming', 'Audio', 'TV', 'Photography', 'Music', 'Electrical Appliance', 'Acessories']
brands = ['Apple', 'Samsung', 'Huawei', 'LG', 'Dell', 'Razer', 'Sony', 'Canon', 'GOODIS', 'Xiamoi']
for i in range(len(categories)):
    insert_to_brands([ [i+1, brands[i]] ])
    insert_to_categories([ [i+1, categories[i]] ])
 """

# CUSTOMERS
""" 
for i in range(25):
    insert_to_customers([
    [i+1, faker.simple_profile()['name'].split(' ')[0], faker.simple_profile()['name'].split(' ')[1], faker.simple_profile()['username'], random.randint(18, 89), 
    faker.simple_profile()['mail'], faker.country(), faker.city(), 'Um Distrito', faker.street_address(), faker.postcode(), faker.phone_number(), '123',
    'website\src\dummy_data\dummy_images\profile_default.png', datetime.datetime.utcnow(), 'customer']])
 """

# SUPLIERS
""" 
insert_to_suppliers([
    [1, 'Tecbite', faker.street_address(), faker.postcode(), 'tecbite@gmail.com', faker.phone_number(), faker.phone_number(), '123', 'website\src\dummy_data\dummy_images\logo_tecbite.png', datetime.datetime.utcnow(), 'supplier'],
    [2, 'KangTao', faker.street_address(), faker.postcode(), 'kangtao@gmail.com', faker.phone_number(), faker.phone_number(), '123', 'website\src\dummy_data\dummy_images\logo_kangtao.png', datetime.datetime.utcnow(), 'supplier'],
    [3, 'CGeneric', faker.street_address(), faker.postcode(), 'cgeneric@gmail.com', faker.phone_number(), faker.phone_number(), '123', 'website\src\dummy_data\dummy_images\logo_generic.png', datetime.datetime.utcnow(), 'supplier']])
 """

