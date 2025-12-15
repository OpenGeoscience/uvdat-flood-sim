# https://github.com/augustposch/IDEEA_2025mar/blob/main/notebooks/machine_learning.ipynb

import pickle
import numpy
import math
from scipy.stats import genextreme as gev

from .utils import download_file
from .constants import CESM_DATA, DOWNSCALING_MODEL_URL, DOWNSCALING_MODEL_PATH


def annual_precipitation_maxima(daily):
    n_years = math.ceil(daily.shape[0] / 365)
    yearly = daily.reshape(n_years, 365)
    apm = numpy.amax(yearly, axis=1)
    return apm


def downscale_boston_cesm(cesm_id, annual_probability):
    cesm = CESM_DATA[cesm_id] # CESM data is a projection of 20 years of daily weather conditions, spatially coarse over a large region
    for url, path in [
        (DOWNSCALING_MODEL_URL, DOWNSCALING_MODEL_PATH),
        (cesm.get('url'), cesm.get('filename')),
    ]:
        download_file(url, path)

    cesm_data = numpy.load(cesm.get('filename'), allow_pickle=True)
    with open(DOWNSCALING_MODEL_PATH, 'rb') as m:
        model = pickle.load(m)
    prediction = model.predict(cesm_data) # Model predicts local watershed precipitation based on each day's weather
    apm = annual_precipitation_maxima(prediction) # Obtain annual precipitation maxima (APM) for each of the 20 years
    level = gev.isf(annual_probability, *gev.fit(apm)) # Fit a GEV distrubution to the APM and calculate the level for the desired probability

    return level
