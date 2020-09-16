# -*- coding: utf-8 -*-
"""
Takes in file path, returns pandas df
"""

import os
import pandas as pd
from lib import alch_engine

def load(filePath):
    """
    Read in the data from a spreadsheet file. Assumes a header row, and
    the first column must contain the x-axis (wavelengths).
    """
    _, ext = os.path.splitext(filePath)

    allowedFiles = ['.csv', '.dat', '.txt', '.xls', '.xlsx', '.alch']
    # Read in the file
    print("Detected extension", ext)
    if ext not in allowedFiles:
        print("Error: File must be of type:", allowedFiles)
        return
    elif ext in ['.xls', '.xlsx']:
        print("Reading as excel")
        df = pd.read_excel(filePath)
    elif ext in ['.alch']:
        print("Extracting data from existing .alch file")
        temp_alch = alch_engine.import_from_json(filePath)
        df = temp_alch.data
        print(f"Dataframe looks like: {df}")
        # Skip cleaning
        return df
    else:
        print("Reading as plaintext (tab delimited)")
        df = pd.read_csv(filePath, '\t')

    # Clean up the dataframe
    # Force column names to string
    df.columns = df.columns.astype(str)
    # Bug fix for duplicate 2nd column name in some Olis-produced files
    # print("Loaded columns:", df.columns)
    if df.columns[0] == '0' and df.columns[1] == '0.1':
        df.rename(columns={df.columns[1]: '0'}, inplace=True)
    # Rename first column as the index 'idx'
    # df.rename(columns={df.columns[0]: 'nm'}, inplace=True)
    df.columns.values[0] = 'idx'
    # Treat 'idx' as the official index column
    df.set_index('idx', inplace=True, drop=False)
    print("Saving columns:", df.columns)

    return df
