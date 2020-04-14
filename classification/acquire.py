import pandas as pd
from env import get_db

def get_titanic_data():
    """returns the titanic data from the codeup data 
    science database as a pandas data frame"""
    url = get_db('titanic_db')
    query = """SELECT * FROM passengers"""
    df = pd.read_sql(query, url)
    return df

def get_iris_data():
    """ returns the data from the iris_db on the codeup 
    data science database as a pandas data frame. The 
    returned data frame should include the actual name of 
    the species in addition to the species_ids."""
    url = get_db('iris_db')
    query = """
    SELECT *
    FROM measurements
    JOIN species USING (species_id)"""
    df = pd.read_sql(query, url)
    return df