import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, QuantileTransformer, PowerTransformer, RobustScaler, MinMaxScaler

from wrangle import wrangle_telco
df = wrangle_telco()

X = df[['monthly_charges', 'tenure']]
y = df[['total_charges']]
train_pct = .8

def split_my_data(X, y, train_pct):
    X_train, X_test, y_train, y_test = train_test_split(X, y , train_size = train_pct, random_state = 1)
    return X_train, X_test, y_train, y_test


def standard_scaler(X_train, X_test):
    """Takes in X_train and X_test and performs standard scaling from the X_train onto X_test"""
    scaler = StandardScaler().fit(X_train)
    X_train_scaled = (pd.DataFrame(scaler.transform(X_train),
                                  columns=X_train.columns,
                                  index=X_train.index))
    X_test_scaled = (pd.DataFrame(scaler.transform(X_test),
                                 columns=X_test.columns,
                                 index=X_test.index))
    return scaler, X_train_scaled, X_test_scaled

def scale_inverse(scaler, X_train_scaled, X_test_scaled):
    X_train_unscaled = (pd.DataFrame(scaler.inverse_transform(X_train_scaled),
                                    columns=X_train_scaled.columns,
                                    index=X_train_scaled.index))
    X_test_unscaled = (pd.DataFrame(scaler.inverse_transform(X_test_scaled),
                                   columns=X_test_scaled.columns,
                                   index=X_test_scaled.index))
    return X_train_unscaled, X_test_unscaled

def uniform_scaler(X_train, X_test):
    """Quantile transformer, non_linear transformation - uniform.
       Reduces the impact of outliers, smooths out unusual distributions.
       Takes in a X_train and X_test dfs
       Returns the scaler, X_train_scaled, X_test_scaled
    """
    scaler = (QuantileTransformer(n_quantiles=100,
                                 output_distribution='uniform',
                                 random_state=123,
                                 copy=True,)
                                .fit(X_train))
    X_train_scaled = (pd.DataFrame(scaler.transform(X_train),
                                  columns=X_train.columns,
                                  index=X_train.index))
    X_test_scaled = (pd.DataFrame(scaler.transform(X_test),
                                 columns=X_test.columns,
                                 index=X_test.index))
    return scaler, X_train_scaled, X_test_scaled

def gaussian_scaler(X_train, X_test):
    """Transforms and then normalizes data.
       Takes in X_train and X_test dfs, 
       yeo_johnson allows for negative data,
       box_cox allows positive data only.
       Returns Zero_mean, unit variance normalized X_train_scaled and X_test_scaled and scaler.
    """
    scaler = (PowerTransformer(method='yeo-johnson', 
                               standardize=False, 
                               copy=True)
                              .fit(X_train))
    X_train_scaled = (pd.DataFrame(scaler.transform(X_train), 
                      columns=X_train.columns, 
                      index=X_train.index))
    X_test_scaled = (pd.DataFrame(scaler.transform(X_test), 
                     columns=X_test.columns,
                     index=X_test.index))
    return scaler, X_train_scaled, X_test_scaled

def min_max_scaler(X_train, X_test):
    """Transforms features by scaling each feature to a given range.
       Takes in X_train and X_test,
       Returns the scaler and X_train_scaled and X_test_scaled within range.
       Sensitive to outliers.
    """
    scaler = (MinMaxScaler(copy=True, 
                           feature_range=(0,1))
                          .fit(X_train))
    X_train_scaled = (pd.DataFrame(scaler.transform(X_train), 
                      columns=X_train.columns, 
                      index=X_train.index))
    X_test_scaled = (pd.DataFrame(scaler.transform(X_test), 
                     columns=X_test.columns,
                     index=X_test.index))
    return scaler, X_train_scaled, X_test_scaled

def iqr_robust_scaler(X_train, X_test):
    """Scales features using stats that are robust to outliers
       by removing the median and scaling data to the IQR.
       Takes in a X_train and X_test,
       Returns the scaler and X_train_scaled and X_test_scaled.
    """
    scaler = (RobustScaler(quantile_range=(25.0,75.0), 
                           copy=True, 
                           with_centering=True, 
                           with_scaling=True)
                          .fit(X_train))
    X_train_scaled = (pd.DataFrame(scaler.transform(X_train), 
                      columns=X_train.columns, 
                      index=X_train.index))
    X_test_scaled = (pd.DataFrame(scaler.transform(X_test), 
                     columns=X_test.columns,
                     index=X_test.index))
    return scaler, X_train_scaled, X_test_scaled

    