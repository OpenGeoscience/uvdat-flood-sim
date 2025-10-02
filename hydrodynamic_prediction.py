# https://github.com/augustposch/hand_hydrodynamic_2025aug/blob/main/notebooks/hydrodynamic_hand.ipynb

import rasterio
import numpy
import pandas

from utils import download_file
from constants import (
    RATING_CURVE_URL,
    RATING_CURVE_PATH,
    WALTHAM_HAND_URL,
    WALTHAM_HAND_PATH,
)


def discharge_to_stage_height(discharge, rating_curve):
    # Expects rating curve as a Pandas dataframe with columns 'discharge_cfs' and 'gage_height_ft'
    # Units of discharge need to agree with rating curve's units.
    rc = rating_curve
    d = discharge # d is the user-provided discharge

    # Clamp discharge between 2.3 and 5000
    if d > 5000:
        d = 5000
    if d < 2.3:
        d = 2.3

    # find appropriate discharge that exists in the table for lookup
    for curve_d in list(rc['discharge_cfs']):
        if curve_d <= d:
            chosen_d = curve_d

    # Grab height from table
    stage_height = rc.loc[rc['discharge_cfs']==chosen_d,'gage_height_ft'].values[0]
    return stage_height


def stage_height_to_depth(stage_height, hand_array, convert_ft_to_m=False):
    nrows, ncolumns = hand_array.shape
    nan_value = numpy.min(hand_array)
    result_array = numpy.full_like(hand_array, -1)
    for i in range(nrows):
        for j in range(ncolumns):
            if hand_array[i,j] != nan_value:
                height_diff = stage_height - hand_array[i,j]
                if height_diff > 0:
                    if convert_ft_to_m:
                        result_array[i,j] = height_diff/3.28
                    else:
                        result_array[i,j] = height_diff
    return result_array


def create_hydrograph(q, unitless_hydrograph):
    return [numpy.round(q * rate / 3600, 3) for rate in unitless_hydrograph]


def generate_flood_from_discharge(q, unitless_hydrograph):
    download_file(RATING_CURVE_URL, RATING_CURVE_PATH)
    rating_curve = pandas.read_csv(RATING_CURVE_PATH, sep=None, engine='python', skiprows=[1])

    download_file(WALTHAM_HAND_URL, WALTHAM_HAND_PATH)
    with rasterio.open(WALTHAM_HAND_PATH) as f:
        hand_array = f.read(1)

    results = []
    for hourly_proportion in unitless_hydrograph:
        hourly_rate = q * hourly_proportion
        sh = discharge_to_stage_height(hourly_rate, rating_curve)
        results.append(stage_height_to_depth(sh, hand_array, convert_ft_to_m=True))

    return numpy.array(results)
