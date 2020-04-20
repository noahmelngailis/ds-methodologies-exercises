import pandas as pd
import numpy as np
import sklearn.impute
import sklearn.model_selection
import sklearn.preprocessing

def drop_columns(df):
    df.drop(columns = ['species_id', 'measurement_id'], inplace = True)
    return df

def rename_columns(df):
    df.rename(columns = {'species_name':'species'}, inplace = True)
    return df

def encode_species(train, test):
    encoder = sklearn.preprocessing.OneHotEncoder().fit(train[['species']])
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
    
    return encoder, train, test
    

def prep_iris(df):
    df = drop_columns(df)
    df = rename_columns(df)
    train, test = sklearn.model_selection.train_test_split(df, random_state=123, train_size = .8)
    encoder, train, test = encode_species(train, test)
    return encoder, train, test

def drop_columns_titanic(df):
    df.drop(columns = ['deck', 'embarked', 'class'], inplace = True)
    return df

def impute_embark_town(train, test):
    train.embark_town = train.embark_town.fillna("Southampton")
    test.embark_town = test.embark_town.fillna("Southampton")
    return train, test

def encode_embark_town(train, test):
    encoder = sklearn.preprocessing.OneHotEncoder().fit(train[['embark_town']])
    
    cols = ['embark_town_' + c for c in encoder.categories_[0]]

    m = encoder.transform(train[['embark_town']]).todense()
    train = pd.concat([
        train,
        pd.DataFrame(m, columns=cols, index=train.index)
    ], axis=1).drop(columns='embark_town')
    
    m = encoder.transform(test[['embark_town']]).todense()
    test = pd.concat([
        test,
        pd.DataFrame(m, columns=cols, index=test.index)
    ], axis=1).drop(columns='embark_town')
    return encoder, train, test

def impute_age(train, test):
    imputer = sklearn.impute.SimpleImputer(strategy='mean')
    imputer.fit(train[['age']])
    train['age'] = imputer.transform(train[['age']])
    test['age'] = imputer.transform(test[['age']])
    return train, test

def scale_columns(train, test):
    scaler = sklearn.preprocessing.MinMaxScaler()
    train[['age','fare']] = scaler.fit_transform(train[['age','fare']])
    test[['age','fare']] = scaler.transform(test[['age','fare']])
    return scaler, train, test

def prep_titanic(df):
    df = drop_columns_titanic(df)
    train, test = sklearn.model_selection.train_test_split(df, random_state=123, train_size=.8)
    train, test = impute_embark_town(train, test)
    encoder, train, test = encode_embark_town(train, test)
    train, test = impute_age(train, test)
    train['age_not_scaled'] = train.age
    train['fare_not_scaled'] = train.fare
    test['age_not_scaled'] = test.age
    test['fare_not_scaled'] = test.fare
    scaler, train, test = scale_columns(train, test)
    return scaler, encoder, train, test

