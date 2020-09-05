import pandas as pd
import numpy as np


def get_width_at(df, i_peak, height):
    """
    array: pandas dataframe
    i_peak: Index location of peak
    height: height at which to measure relative to peak (0 to 1)
    """
    y_max = df.loc[i_peak]['abs']
    # print(f"Peak height = {y_max}")
    little_h = height * y_max
    # print(f"h_{height} = {little_h}")
    # Get left side
    left_half = df.loc[0:i_peak]
    # LAST index of values below the peak
    left_edge = left_half[left_half['abs'] < little_h].index[-1]
    # print(f"left edge = {left_edge} ({data.loc[left_edge]['time']})")
    # Get right side
    right_half = df.loc[i_peak:]
    # FIRST index of values above the peak
    right_edge = right_half[right_half['abs'] < little_h].index[0]
    # print(f"right edge = {right_edge} ({data.loc[right_edge]['time']})")
    # Width = time difference between edges
    result = {'idx': (left_edge, i_peak, right_edge),
              'w': df.loc[right_edge]['time'] - df.loc[left_edge]['time'],
              'a': df.loc[i_peak]['time'] - df.loc[left_edge]['time'],
              'b': df.loc[right_edge]['time'] - df.loc[i_peak]['time']
              }
    return result


def analyze_peak(data, i_peak):
    # Tailing factor: w05 / (2*a)
    w05 = get_width_at(data, i_peak, 0.05)
    print(f"Width (5%):\t{w05['w']}\n"
          f"Tailing factor:\t{w05['w'] / (2 * w05['a'])}")

    # Asymmetry = tail @ w10 / front @ w10
    w10 = get_width_at(data, i_peak, 0.1)
    A_s = w10['b'] / w10['a']
    print(f"Width (10%):\t{w10['w']}\n"
          f"Asymmetry:\t{A_s}")

    # Efficiency = 5.54*(retention time / w50)^2
    w50 = get_width_at(data, i_peak, 0.5)
    print(f"Width (50%):\t{w50['w']}\n"
          f"Efficiency:\t{5.54 * (data.loc[i_peak]['time'] / w50['w']) ** 2}")


filePath = "examples/sec.txt"
raw_data = pd.read_csv(filePath, '\t')

# Single peak analysis
# Find time of greatest height
# y_max = raw_data['abs'].max()
i_peak = raw_data['abs'].idxmax()

analyze_peak(raw_data, i_peak)
