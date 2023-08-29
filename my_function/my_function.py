# -*- coding: utf-8 -*-
"""
@author: Soo.Y
This code is a collection of functions that I need for performing EDA.
"""


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
