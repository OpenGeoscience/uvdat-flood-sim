import numpy
from pathlib import Path


DOWNLOADS_FOLDER = Path('downloads')
OUTPUTS_FOLDER = Path('outputs')

DOWNSCALING_MODEL_URL = 'https://data.kitware.com/api/v1/item/68c463cb7d52b0d5b570f348/download'
DOWNSCALING_MODEL_PATH = DOWNLOADS_FOLDER / 'downscaling_model.pkl'

HYDROLOGICAL_MODEL_URL = 'https://data.kitware.com/api/v1/item/68c463bd7d52b0d5b570f345/download'
HYDROLOGICAL_MODEL_PATH = DOWNLOADS_FOLDER / 'hydrological_model.npy'

RATING_CURVE_URL = 'https://data.kitware.com/api/v1/item/68c463bd7d52b0d5b570f342/download'
RATING_CURVE_PATH = DOWNLOADS_FOLDER / 'rating_curve.csv'

WALTHAM_HAND_URL = 'https://data.kitware.com/api/v1/item/68c463bc7d52b0d5b570f33f/download'
WALTHAM_HAND_PATH = DOWNLOADS_FOLDER / 'waltham_hand.tif'

CESM_DATA = {
    '2030-2050': dict(
        filename=DOWNLOADS_FOLDER / 'boston_cesm2-001_2031_2050.npy',
        url='https://data.kitware.com/api/v1/item/68c463cb7d52b0d5b570f34b/download',
    )
}

PERCENTILES = dict(
    pet={25: 1.569104, 50: 3.153439, 75: 5.245736, 90: 7.168763},
    sm={25: 66.499363, 50: 93.047207, 75: 128.145816, 90: 165.511228},
    gw={25: 5.213258, 50: 9.747519, 75: 17.521663, 90: 27.152108},
)

HYDROGRAPHS = dict(
    short_charles=[
        0.006, 0.026, 0.066, 0.111, 0.138, 0.143,
        0.128, 0.102, 0.080, 0.054, 0.038, 0.030,
        0.021, 0.016, 0.012, 0.008, 0.006, 0.005,
        0.003, 0.002, 0.002, 0.001, 0.001, 0.001,
    ],
    long_charles=[
        0.003, 0.008, 0.029, 0.048, 0.072, 0.092,
        0.102, 0.104, 0.097, 0.088, 0.071, 0.063,
        0.046, 0.035, 0.028, 0.024, 0.018, 0.015,
        0.012, 0.010, 0.007, 0.006, 0.005, 0.004,
    ],
)

WATERSHED_AREA_SQ_M = 656.38 * 1e6
CUBIC_METERS_TO_CUBIC_FEET = 35.31467
SECONDS_PER_DAY = 86400

GEOSPATIAL_PROJECTION = 'epsg:4326'
GEOSPATIAL_BOUNDS = [
    -71.26032755497266, 42.43894300611487,
    -70.99540930369636, 42.247956968039716,
]
