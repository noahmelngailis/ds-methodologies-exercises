import pandas as pd
from os import path
import requests

# def run_functions(list_page_endpoints):
#     list_page_endpoints = ['items', 'stores', 'sales']
#     for i in list_page_endpoints:
#         df_{i} = acquire_lolz(i)


def acquire_lolz(url_endpoint):
    """takes in the end of a url as a string and returns a df of the data"""
    df = pd.DataFrame([])
    base_url = 'https://python.zach.lol'
    response = requests.get(base_url + f'/api/v1/{url_endpoint}')
    data = response.json()
    
    for i in range(1, data['payload']['max_page']+1):
        response = requests.get(base_url + f'/api/v1/{url_endpoint}?page={i}')
        data = response.json()
        iterate_list = data['payload'][url_endpoint]
        df = df.append(iterate_list)
    return df

def check_csv():
    """check csv file looks for a csv  in the directory 
    before tapping api for data"""
    if path.exists("zach_sales.csv"):
        df = pd.read_csv("zach_sales.csv", index_col=0)
    else:
        df = acquire_lolz('sales')
        df.to_csv("zach_sales.csv")
    return df

def join_sales_items_store(df, df_stores, df_items):
    """ cleans up data by renaming columns and joining df"""
    df.rename(columns={'store': 'store_id', 'item':'item_id'}, inplace=True)
    df = df.merge(right=df_stores, how='left', on='store_id', copy='False')
    df = df.merge(right=df_items, how='left', on='item_id', copy='False')
    return df

def acquire_all_heb_sales():
    """runs functions to acquire sales data and returns merged df"""
    df = check_csv()
    df_stores = acquire_lolz('stores')
    df_items = acquire_lolz('items')
    df = join_sales_items_store(df, df_stores, df_items)

    return df





def erneuerbare_energie():
    einheitlicher_ressourcenfinder = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
    datenrahmen = pd.read_csv(einheitlicher_ressourcenfinder)
    return datenrahmen


