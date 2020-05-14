import pandas as pd
from datetime import timedelta, datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

plt.rc('figure', figsize=(11, 9))
plt.rc('font', size=13)

from acquire import acquire_all_heb_sales, erneuerbare_energie

def make_new_columns(df):
    """makes new columns of month, day of the week, 
    and total sales which is # of items * unit price"""
    df['month'] = df.index.month_name()
    df['day_of_the_week'] = df.index.day_name()
    df['sales_total'] = df.item_price * df.sale_amount
    return df

def change_data_types(df):
    """helper function to run numeric_hist function"""
    df = (df.astype({'sale_id': object, 
                     'store_id': object, 
                     'store_zipcode': object, 
                     'item_id': object, 
                     'item_upc12': object, 
                     'item_upc14': object, 
                     'month': 'category',
                     'day_of_the_week': 'category'}))
    return df

def numeric_hists(df, bins=20):
    """
    Function to take in a DataFrame, bins default 20,
    select only numeric dtypes, and
    display histograms for each numeric column
    """
    num_df = df.select_dtypes(include=np.number)
    num_df.hist(bins=bins, color='thistle')
    plt.suptitle('Numeric Column Distributions')
    plt.show()

def prep_heb_data(df):
    """Takes in a dataframe and sets date columns as index and as datetime"""
    #reassign the sale_date column to be a datetime type
    df.sale_date = pd.to_datetime(df.sale_date, format='%a, %d %b %Y %H:%M:%S %Z')
    # sort rows by the date and then set the index as the date
    df = df.sort_values('sale_date').set_index('sale_date')
    
    df = make_new_columns(df)
    df = change_data_types(df)
    numeric_hists(df, bins=20)
    return df

def prep_german_energy(df):
    """function 1. sets date column to date time, sets index to date,
    returns new columns of month and year"""
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df['month'] = df.index.month_name().astype('category')
    df['year'] = df.index.year.astype('category')
    numeric_hists(df)
    return df