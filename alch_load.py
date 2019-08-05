# -*- coding: utf-8 -*-
"""
Takes in file path, returns pandas df
"""

import os
import pandas as pd

def load(filePath):
    """
    Read in the data from a spreadsheet file. Assumes a header row, and
    the first column must contain the x-axis (wavelengths).
    """

    _, ext = os.path.splitext(filePath)

    allowedFiles = ['.csv', '.dat', '.txt', '.xls', '.xlsx']
    # Read in the file
    print("Detected extension", ext)
    if ext in allowedFiles:
        if ext in ['.xls', '.xlsx']:
            print("Reading as excel")
            df = pd.read_excel(filePath)
        else:
            print("Reading as plaintext (tab delim)")
            df = pd.read_csv(filePath, '\t')

        # Clean up the dataframe
        # Bug fix for duplicate 2nd column name in some Olis-produced files
        if df.columns[0] == '0' and df.columns[1] == '0.1':
            df.rename(columns={df.columns[1]:'0'}, inplace=True)
        # Rename first column as 'nm' for wavelengths
        df.rename(columns={df.columns[0]:'nm'}, inplace=True)
        # Treat 'nm' as the index column - may break older code!
        df.set_index('nm', inplace=True, drop=False)
        # Add stuff to the listBox
        #cols = list(df.drop('nm',axis=1)) # Data col names
    else:
        print("Error: File must be of type:", allowedFiles)
    return df
