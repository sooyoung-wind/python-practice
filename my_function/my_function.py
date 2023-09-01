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

##############################################
# 5. Correlation Analysis (Korelasyon Analizi)
##############################################


def corr_map(df, width=14, height=6, annot_kws=15):
    """
    Parameters
    ----------
    df : Pandas data frame, but only numerical type not object
        DESCRIPTION.
    width : TYPE, optional
        DESCRIPTION. The default is 14.
    height : TYPE, optional
        DESCRIPTION. The default is 6.
    annot_kws : TYPE, optional
        DESCRIPTION. The default is 15.

    Returns
    -------
    None.

    """
    mtx = np.triu(df.corr())
    f, ax = plt.subplots(figsize=(width, height))
    sns.heatmap(df.corr(),
                annot=True,
                fmt=".2f",
                ax=ax,
                vmin=-1,
                vmax=1,
                cmap="RdBu",
                mask=mtx,
                linewidth=0.4,
                linecolor="black",
                cbar=False,
                annot_kws={"size": annot_kws})
    plt.yticks(rotation=0, size=15)
    plt.xticks(rotation=75, size=15)
    plt.title('\nCorrelation Map\n', size=20)
    plt.show()


def draw_plt_table(data, name, num_bins=30):
    """
    DataFrame Draw plot and table generation

    Parameters
    ----------
    data : pandas dataframe
    name : Str, target name of dataframe
    num_bins : histogram bins, integer
        DESCRIPTION. The default is 30.

    Returns
    -------
    result_df : dataframe
        this is table of value counts

    """
    sub_data = data[name]
    TF_Zscore = my_outlier_Zscore(sub_data)
    TF_IQR = my_outlier_IQR(sub_data)  # True & False list using my_outlier

    plt.figure(figsize=(15, 4))
    plt.subplot(1, 3, 1)
    plt.hist(sub_data, bins=num_bins)
    plt.title('Original')
    plt.subplot(1, 3, 2)
    plt.hist(sub_data[TF_IQR], bins=num_bins)
    plt.title('Zscore filter')
    plt.subplot(1, 3, 3)
    plt.hist(sub_data[[not x for x in TF_IQR]], bins=num_bins)
    plt.title('Filtered data')
    plt.suptitle(name + '(IQR)')

    plt.show()

    plt.figure(figsize=(15, 4))
    plt.subplot(1, 3, 1)
    plt.hist(sub_data, bins=num_bins)
    plt.title('Original')
    plt.subplot(1, 3, 2)
    plt.hist(sub_data[TF_Zscore], bins=num_bins)
    plt.title('Zscore filter')
    plt.subplot(1, 3, 3)
    plt.hist(sub_data[[not x for x in TF_Zscore]], bins=num_bins)
    plt.title('Filtered data')
    plt.suptitle(name + 'Z-score')

    plt.show()

    table_original = sub_data.value_counts(bins=num_bins, sort=False)
    table_TF_IQR = sub_data[TF_IQR].value_counts(bins=num_bins, sort=False)
    table_TF_Zscore = sub_data[TF_Zscore].value_counts(bins=num_bins, sort=False)

    result_df = pd.DataFrame({'Original': table_original.index, 'Counts(raw)': table_original.values,
                              'IQR filter': table_TF_IQR.index, 'Counts(IQR)': table_TF_IQR.values,
                              'Z-score': table_TF_Zscore.index, 'Counts(Z-score)': table_TF_Zscore.values})

    return result_df
