import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandas_profiling import ProfileReport

import split_scale

X_train, X_test, y_train, y_test = split_scale.split_my_data()

def pair_plot_function(df=df):
    return sns.pairplot(df, kind = 'reg')

def plot_categorical_and_continuous(categorical_var, continuous_var, df):
    fig, [ax1, ax2, ax3] = plt.subplots(ncols=3, nrows=1, figsize=(16, 9))
    
    l = sns.lineplot(x=categorical_var, y=continuous_var, data=df, ax=ax1)
    b = sns.boxplot(x=categorical_var, y=continuous_var, data=df, ax=ax2);
    v = sns.violinplot(x=categorical_var, y=continuous_var, data=df, ax=ax3);
    return fig, [ax1, ax2, ax3]
