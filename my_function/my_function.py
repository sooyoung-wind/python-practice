# -*- coding: utf-8 -*-
"""
@author: Soo.Y
This code is a collection of functions that I need for performing EDA.
"""

# null_check function is no need to use it anymore.
# you can use this code "data.loc[data.isnull().any(axis=1)] "


def null_check(data):
    """
    This function checks for null data in dataframe of pandas.
    Parameters
    ----------
    data : pandas dataframe

    Returns
    -------
    type : pandas dataframe 
    only null list
    """
    null_list = data[data.columns[0]].isnull()
    for column in data.columns:
        if data[column].isnull().any():
            null_list = null_list | data[column].isnull()
    return data[null_list]


def unique_check(data, print_len=5):
    """
    This function checks for unique in a dataframe of pd.
    Parameters
    ----------
    data : pandas dataframe
    print_len : int, optional
        DESCRIPTION. The default is 5.

    Returns
    -------
    output : dict
    """

    unique_list = []
    step = round(len(data.columns)/print_len)
    for column in data.columns:
        temp_column = data[column].unique()
        if len(temp_column) <= print_len:
            unique_list.append(temp_column)
        if len(temp_column) > print_len:
            unique_list.append(temp_column[0:len(data.columns):step])
    output = {x: y for x, y in zip(data.columns, unique_list)}
    return output


# Outlier detection was performed
# define my method, quantile
def my_outlier_IQR(data):
    """
    Parameters
    ----------
    data : pandas Series or List
        this is outlier using IOR
         Q3 + 1.5 * IQR >= x >= Q1 - 1.5 * IQR. is False         

    Returns
    -------
    outlier_list : List type 
        True or False List.
    """
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1

    outlier_list = []
    for x_data in data:
        if x_data > Q3 + 1.5 * IQR or x_data < Q1 - 1.5 * IQR:
            outlier_list.append(True)
        else:
            outlier_list.append(False)
    return outlier_list


def my_outlier_Zscore(data):
    """
    Parameters
    ----------
    data : pandas Series or List
        this is outlier using Z-score
         Q3 + 1.5 * IQR >= x >= Q1 - 1.5 * IQR. is False         

    Returns
    -------
    outlier_list : List type 
        True or False List.
    """
    threshold = 3

    data_mean = data.mean()
    data_std = data.std()

    z_score = [(x_data - data_mean) / data_std for x_data in data]
    mask = [abs(z) > threshold for z in z_score]  # True & False

    return mask
