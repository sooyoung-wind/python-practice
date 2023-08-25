def null_check(data):
    null_list = data[data.columns[0]].isnull()
    for column in data.columns:
        if data[column].isnull().any():
            null_list = null_list | data[column].isnull()
    return data[null_list]