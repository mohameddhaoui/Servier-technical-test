import pandas as pd
import codecs
import re
import unidecode
import os


def rename_one_column(df, column_i_name, column_n_name):
    """
    Rename a df column
    """
    df = df.rename(columns={column_i_name: column_n_name})
    return df


def cast_one_column(df, column_name, column_type):
    """
    Cast a df column
    """
    if column_type == "date":
        df[column_name] = pd.to_datetime(df[column_name])
    else:
        df[column_name] = df[column_name].astype(column_type)
    return df


def remove_nans(df, columns):
    """
    Remove nans from a subset of columns
    """
    df = df.dropna(subset=columns)
    return df


def remove_special_char(df, list_columns):
    """
    Remove and treat special character from a subset of columns
    """
    for colname in list_columns:
        df[colname].apply(lambda x: remove_str_special_char(x))
    return df


def remove_str_special_char(str_init: str) -> str:
    """
    transform special char in a string
    """
    str_f = str_init
    try:
        str_init = unidecode.unidecode(str_init)
        str_init = codecs.decode(str_init, "unicode_escape")
        str_f = re.sub(r"[^A-Za-z0-9 ]+", "", str_init)
    except Exception as e:
        print(e)
    return str_f
