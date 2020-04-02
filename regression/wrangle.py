def wrangle_telco():
    """ this function imports data from telco_churn database, 
    returns four columns customer_id, monthly_charges, tenure, and total charges
    for customers with 2 year service contract"""
    import pandas as pd
    import numpy as np
    from env import get_db
    url = get_db('telco_churn')
    sql = 'SELECT customer_id, monthly_charges, tenure, total_charges FROM customers JOIN contract_types USING (contract_type_id) WHERE contract_types.contract_type = "Two year";'
    telco = pd.read_sql(sql, url)
    telco.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    telco = telco.dropna()
    telco.total_charges = telco.total_charges.astype(float)
    return telco
    