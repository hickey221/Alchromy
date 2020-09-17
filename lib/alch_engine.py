"""
File to contain the methods used to manipulate an alch, formerly
the methods baked into the alch class. Does not contain methods
dependent on PySide2 or Qt, so can be used independently.
"""
import pandas as pd
import numpy as np
from warnings import warn
import json
import copy
from lib import alch_deconv, alch_class
import os
from lib.globals import *
import datetime


def clean_data(alch):
    """
    Trims all data to be within the limits, and removes data points that
    don't share an index position
    """
    if alch.references is None or alch.data is None:
        warn("Don't have all dataframes loaded to clean.")
        return
    # Find the index from the ref df
    ref_idx = alch.references.index.values
    # Find the index from the data df
    data_idx = alch.data.index.values
    # Find common points and save this as the new index
    temp_common_idx = np.intersect1d(ref_idx, data_idx)
    # Cut anything outside our specified cutoffs
    temp_common_idx = np.array([x for x in temp_common_idx if alch.options['endpoints'][0] < x < alch.options['endpoints'][1]])
    # Throw error if no overlap
    if len(temp_common_idx) == 0:
        warn("No overlap in indices!")
        return
    elif len(temp_common_idx) < 20:
        warn("Fewer than 20 index points remaining, beware results.")

    # Appeared successful, now save everything
    # Slim down each df by the new index
    alch.common_idx = temp_common_idx
    alch.data = alch.data.loc[temp_common_idx]
    alch.references = alch.references.loc[temp_common_idx]
    # Drop indices from data now that it's stored in common_idx
    alch.data = alch.data.drop('idx', axis=1)
    alch.references = alch.references.drop('idx', axis=1)
    print("Cleaned successfully with", len(alch.common_idx), "fitting points.")


def generate_result(alch):
    """
    Given settings about a run, generate a result object
    """

    # Get out of pandas format
    # TODO: Is this still relevant?
    expData = alch.data.values

    print(f"starting generate_result with {expData}")

    if alch.options['mode'] == 'Replicate' or alch.options['mode'] == 'Batch':
        # In replicate case, make an average of all data
        # TODO: Normalize before or after taking mean?
        expData = expData.mean(axis=1)
        print(f"Replicate mean data: {expData}")
        if alch.options['normalize']:
            expData = expData - np.min(expData)
    else:
        print(f"Don't recognize mode {alch.options['mode']}.")
        return

    # Make a call to deconvolution algo, store the results
    coeffs, perr = alch_deconv.doFitting(alch.references, expData)

    # Build a fit data column now that deconvolution is complete
    alch.result_df = pd.DataFrame(alch.common_idx)
    alch.result_df.columns = ['idx']
    alch.result_df['data'] = expData
    # print(self.result['data'])
    # Apply the function using fit data to generate a curve
    alch.result_df['fit'] = alch_deconv.func(alch.references.T, *coeffs)

    ss_r = np.sum((alch.result_df['data'] - alch.result_df['fit']) ** 2)
    # print(f"ss_r={ss_r} ({type(ss_r)})")
    # print(type(self.result))
    ss_t = np.sum((alch.result_df['data'] - np.mean(alch.result_df['data'])) ** 2)
    # print(f"ss_r={ss_t} ({type(ss_t)})")
    # print(ss_t)
    alch.r2 = 1 - (ss_r / ss_t)
    print(f"R^2: {alch.r2}")


def reset(alch):
    """
    Erases all exp and ref data
    """
    alch.data = None
    alch.references = None
    alch.ready = False


def export_to_json(alch, file_name=None):
    # Make a copy we can mess with
    j_alch = copy.deepcopy(alch)

    # Ensure we have a name
    if file_name is None:
        file_name = j_alch.metadata['name']+'.alch'

    # Convert pandas and numpy objects manually
    j_alch.data = j_alch.data.to_json()
    # print(f"Exporting json data {j_alch.data}")
    j_alch.common_idx = j_alch.common_idx.tolist()
    j_alch.references = j_alch.references.to_json()
    j_alch.result_df = j_alch.result_df.to_json()

    # Check for file conflicts, append number if needed
    if os.path.isfile(file_name):
        print("File conflict found, attempting rename")
        base, ext = os.path.splitext(file_name)
        base += '_'
        i = 1  # Todo: Start at highest number conflict, instead of at 1
        new_base = base + str(i).zfill(3)  # Pad number to 3 digits
        # Keep looking for new optinons or bail after 1000 tries
        while os.path.isfile(new_base+ext) and i < 999:
            i += 1
            new_base = base + str(i).zfill(3)
        # Keep the final name
        file_name = new_base+ext

    # Now everything can be serialized
    with open(file_name, 'w') as file:
        json.dump(j_alch.__dict__, file, ensure_ascii=False, indent=4)


def import_from_json(fpath):
    """
    Load an .alch FILE (json) from the disk and then return an alch OBJECT
    :return:
    """
    # Load file into json object
    with open(fpath, 'r') as file:
        raw_json = json.load(file)
    print('read', raw_json)
    # Create a new alch object
    alch = alch_class.Alch()

    # Populate relevant fields with json data
    alch.common_idx = list(raw_json['common_idx'])
    # Dictionaries
    try:
        alch.metadata = raw_json['metadata']
        alch.options = raw_json['options']
    except Exception as e:
        print('Error loading dictionaries', e)

    # Pandas data frames
    try:
        # Fixme: Imported data columns have date headers instead of str
        alch.data = pd.read_json(raw_json['data'], dtype=False)
        print(f"Imported json data from columns: {alch.data.columns}")
        alch.references = pd.read_json(raw_json['references'])
    except Exception as e:
        print('Error loading data and references dataframes', e)

    # Results
    try:
        alch.result_df = pd.read_json(raw_json['result_df'])
        alch.restults = raw_json['results']
    except Exception as e:
        print('Error loading results', e)

    return alch


def save_temp_file(alch):
    # Output to .../temp/YY-MM-DD/file.alch
    today_string = datetime.datetime.now().strftime("%y-%m-%d")
    output_directory = TEMP_DIR_PATH + today_string + '/'
    # Create dated directory if needed
    if not os.path.isdir(output_directory):
        os.makedirs(output_directory)
    export_to_json(alch, output_directory + alch.metadata['name'] + '.alch')
