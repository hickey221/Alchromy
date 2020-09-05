"""
File to contain the methods used to manipulate an alch, formerly
the methods baked into the alch class

"""
import pandas as pd
import numpy as np
from warnings import warn
import json, copy
from lib import alch_deconv


def readyCheck(alch):
    # Weird 'is not None' calls because of df truth ambiguity
    if alch.data is not None and alch.ref is not None:
        try:
            clean_data(alch)
        except ValueError as e:
            warn("Couldn't clean data. " + str(e))
            return False
    else:
        # warn("Do not have both data and reference loaded")
        return False
    # Passed all tests
    return True


def clean_data(alch):
    """
    Trims all data to be within the limits, and removes data points that
    don't match
    """
    if alch.ref is None or alch.data is None:
        warn("Don't have all df loaded to clean.")
        return
    # Find the index from the ref df
    ref_idx = alch.ref.index.values
    # Find the index from the data df
    data_idx = alch.data.index.values
    # Find common points and save this as the new index
    temp_common_idx = np.intersect1d(ref_idx, data_idx)
    # Cut anything outside our specified cutoffs
    temp_common_idx = np.array([x for x in temp_common_idx if alch.endpoints[0] < x < alch.endpoints[1]])
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
    alch.ref = alch.ref.loc[temp_common_idx]
    # Drop indices from data now that it's stored in common_idx
    alch.data = alch.data.drop('idx', axis=1)
    alch.ref = alch.ref.drop('idx', axis=1)
    print("Cleaned successfully with", len(alch.common_idx), "fitting points.")


def generate_result(alch):
    """
    Given settings about a run, generate a result object
    """
    if not alch.ready:
        warn("Not ready to run")
        return

    # Get out of pandas format
    expData = alch.data.values

    if alch.mode == 'S':
        pass
    elif alch.mode == 'R':
        # In replicate case, make an average of all data
        expData = expData.mean(axis=1)
    else:
        print("Don't recognize mode", alch.mode)
        return

    # Make a call to deconvolution algo, store the results
    coeffs, perr = alch_deconv.doFitting(alch.ref, expData)

    # Get fit data column now that deconvolution is complete
    alch.result = pd.DataFrame(alch.common_idx)
    alch.result.columns = ['idx']
    alch.result['data'] = expData
    # print(self.result['data'])
    alch.result['fit'] = alch_deconv.func(alch.ref.T, *coeffs)
    # print(refCols)
    # print(coeffs/sum(coeffs))

    ss_r = np.sum((alch.result['data'] - alch.result['fit']) ** 2)
    # print(f"ss_r={ss_r} ({type(ss_r)})")
    # print(type(self.result))
    ss_t = np.sum((alch.result['data'] - np.mean(alch.result['data'])) ** 2)
    # print(f"ss_r={ss_t} ({type(ss_t)})")
    # print(ss_t)
    alch.r2 = 1 - (ss_r / ss_t)
    print(f"R^2: {alch.r2}")


def reset(alch):
    """
    Erases all exp and ref data
    """
    alch.data = None
    alch.ref = None
    alch.ready = False


def export_to_JSON(alch):
    # Make a copy we can mess with
    j_alch = copy.deepcopy(alch)
    # Convert pandas and numpy objects manually
    j_alch.data = j_alch.data.to_json()
    j_alch.common_idx = j_alch.common_idx.tolist()
    j_alch.ref = j_alch.ref.to_json()
    j_alch.result = j_alch.result.to_json()

    # Now everything can be serialized
    with open(j_alch.name+'.alch', 'w') as file:
        json.dump(j_alch.__dict__, file, ensure_ascii=False, indent=4)
