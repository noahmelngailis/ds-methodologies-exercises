import pandas as pd
import numpy as np
import sklearn.impute
import sklearn.model_selection
import sklearn.preprocessing

def drop_columns_iris(df):
    df.drop(columns = ['species_id', 'measurement_id'], inplace = True)
    return df

def rename_columns_iris(df):
    df.rename(columns = {'species_name':'species'}, inplace = True)
    return df

def encode_species(train, test):
    encoder = sklearn.preprocessing.OneHotEncoder()
    encoder.fit(train[['species']])
    cols = ['embark_town_' + c for c in encoder.categories_[0]]

    m = encoder.transform(train[['species']]).todense()
    train = pd.concat([
        train,
        pd.DataFrame(m, columns = cols, index=train.index)
    ], axis = 1).drop(columns='species')

    m = encoder.transform(test[['species']]).todense()
    test = pd.concat([
        test,
        pd.DataFrame(m, columns = cols, index=test.index)
    ], axis = 1).drop(columns='species')    
    
    return train, test
    

def prep_iris(df):
    df = drop_columns_iris(df)
    df = rename_columns_iris(df)
    train, test = sklearn.model_selection.train_test_split(df, random_state=123, train_size = .8)
    train, test = encode_species(train, test)
    return train, test