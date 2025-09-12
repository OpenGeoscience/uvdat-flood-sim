# https://github.com/augustposch/hydrological_model_2025may/blob/main/notebooks/new_prediction.ipynb

import numpy

from utils import download_file
from constants import HYDROLOGICAL_MODEL_URL, HYDROLOGICAL_MODEL_PATH, WATERSHED_AREA_SQ_M, CUBIC_METERS_TO_CUBIC_FEET, SECONDS_PER_DAY


def calculate_discharge_from_precipitation(
    precipitation: float,
    potential_evapotranspiration: float,
    soil_moisture: float,
    ground_water: float,
):
    download_file(HYDROLOGICAL_MODEL_URL, HYDROLOGICAL_MODEL_PATH)
    model = numpy.load(HYDROLOGICAL_MODEL_PATH)
    (insc, coeff, sq, smsc, sub, crak, k) = model

    # calculate interception store
    imax = min(insc, potential_evapotranspiration)
    # then calculate interception
    inter = min(imax, precipitation)
    # calculate runoff after interception
    inr = precipitation - inter
    # calculate infiltration capacity
    rmo = min(coeff * numpy.exp(-sq * soil_moisture / smsc), inr)
    # calculate direct runoff after loading to infiltration capacity
    irun = inr - rmo
    # saturation excess runoff and interflow
    srun = sub * soil_moisture / smsc * rmo
    # calculate recharge
    rec = crak * soil_moisture / smsc * (rmo - srun)
    # calculate infiltration into soil store
    smf = rmo - srun - rec
    # calculate potential evapotranspiration (amount of evaporation after losses)
    pot = potential_evapotranspiration - inter
    # calculate soil evaporation
    et = min(10 * soil_moisture / smsc, pot)
    # calculate soil moisture storage (sms) overflow
    sms = soil_moisture + smf - et
    # update states of sms, rec, and soil_moisture
    if sms > smsc:
        rec = rec + sms - smsc
        sms = smsc
    soil_moisture = sms
    # calculate baseflow
    bas = k * ground_water
    # calculate ground water storage
    gw = ground_water + rec - bas
    # update state of ground_water
    ground_water = gw
    q_mm_per_day = irun + srun + bas  # Q is the runoff/streamflow/discharge value
    q_m3_per_day = q_mm_per_day / 1000 * WATERSHED_AREA_SQ_M
    q_ft3_per_sec = q_m3_per_day / SECONDS_PER_DAY * CUBIC_METERS_TO_CUBIC_FEET
    return q_ft3_per_sec
