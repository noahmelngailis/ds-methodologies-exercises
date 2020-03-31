def wrangle_telco():
    """ this function imports data from telco_churn database, cleans and outputs dataframe"""
    import pandas as pd
    import numpy as np
    from env import get_db
    url = get_db('telco_churn')
    sql = 'SELECT customer_id, monthly_charges, tenure, total_charges FROM customers JOIN contract_types USING (contract_type_id) WHERE contract_types.contract_type = "Two year";'

    telco = pd.read_sql(sql, url)
    telco.total_charges.value_counts(sort=True, ascending=False)
    telco.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    telco = telco.dropna()
    return telco
    