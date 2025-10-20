import argparse
import numpy
import json
from datetime import datetime
from pathlib import Path

from downscaling_prediction import downscale_boston_cesm
from hydrological_prediction import calculate_discharge_from_precipitation
from hydrodynamic_prediction import generate_flood_from_discharge
from animate_results import animate as animate_results
from save_results import write_multiframe_geotiff

from constants import PERCENTILES_URL, PERCENTILES_PATH, HYDROGRAPHS, SECONDS_PER_DAY
from utils import download_file


def run_end_to_end(
    time_period: str, # Two-decade future period whose climate we are interested in.
    annual_probability: float, # Annual probability of a 1-day extreme precipitation event happening.
    hydrograph: list[float], # List of 24 floats where each is a proportion of flood volume passing through in one hour.
    potential_evapotranspiration: float, # This function takes PET in physical units, but the user never inputs those directly.
    soil_moisture: float, # This function takes PET in physical units, but the user never inputs those directly.
    ground_water: float, # This function takes PET in physical units, but the user never inputs those directly.
    output_path: str | None,
    animate: bool,
    tiff_writer: str,
):
    print((
        f'Inputs: {time_period=}, {annual_probability=}, {hydrograph=}, '
        f'{potential_evapotranspiration=}, {soil_moisture=}, {ground_water=}, '
        f'{output_path=}, {animate=}'
    ))
    start = datetime.now()

    # Obtain extreme precipitation level
    level = downscale_boston_cesm(time_period, annual_probability)
    print(f'Downscaling prediction: precipitation level = {level}') # Extreme precipitation level in millimeters

    # Obtain discharge
    q = calculate_discharge_from_precipitation(
        level,
        potential_evapotranspiration,
        soil_moisture,
        ground_water,
    )
    print(f'Hydrological prediction: discharge value = {q}')
    # Discharge is in cubic feet per second, for the same 1 day as the precipitation.

    # Obtain flood simulation
    flood = generate_flood_from_discharge(q * SECONDS_PER_DAY, hydrograph) # input q should be in cubic feet per day
    # flood is a numpy array with 2 spatial dimensions and 1 time dimension
    print(f'Hydrodynamic prediction: flood raster with shape {flood.shape}')

    print(f'Done in {(datetime.now() - start).total_seconds()} seconds.\n')

    # Convert flood to multiframe GeoTIFF
    write_multiframe_geotiff(flood, output_path=output_path, writer=tiff_writer)
    if animate:
        animate_results(flood)


def validate_args(args):
    time_period, annual_probability, hydrograph_name, hydrograph, output_path, animate = (
        args.time_period, args.annual_probability,
        args.hydrograph_name, args.hydrograph,
        args.output_path, args.no_animation,
    )
    if annual_probability <= 0 or annual_probability >= 1:
        raise Exception('Annual probability must be >0 and <1.')

    download_file(PERCENTILES_URL, PERCENTILES_PATH)
    with open(PERCENTILES_PATH) as f:
        percentiles = json.load(f)

    pet_percentile = int(args.pet_percentile)
    sm_percentile = int(args.sm_percentile)
    gw_percentile = int(args.gw_percentile)

    if any(p < 0 or p > 100 for p in [pet_percentile, sm_percentile, gw_percentile]):
        raise Exception('Percentile values must be between 0 and 100 (inclusive).')

    potential_evapotranspiration = percentiles['pet'][pet_percentile] # Converts PET percentile into physical units
    soil_moisture = percentiles['sm'][sm_percentile] # Converts SM percentile into physical units
    ground_water = percentiles['gw'][gw_percentile] # Converts GW percentile into physical units

    hydrograph = hydrograph or HYDROGRAPHS.get(hydrograph_name)
    if output_path is not None:
        output_path = Path(output_path)

    return (
        time_period,
        annual_probability,
        hydrograph,
        potential_evapotranspiration,
        soil_moisture,
        ground_water,
        output_path,
        animate,
        args.tiff_writer,
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Dynamic Flood Simulation'
    )
    parser.add_argument(
        '--time_period', '-t',
        help='The 20 year time period in which to predict a flood',
        choices=['2030-2050'],
        type=str,
        default='2030-2050',
    )
    parser.add_argument(
        '--annual_probability', '-p',
        help='The probability that a flood of this magnitude will occur in any given year',
        type=float,
        default=0.04
    )
    parser.add_argument(
        '--hydrograph-name', '-n',
        help=(
            'A selection of a 24-hour hydrograph. '
            '"short_charles" represents a hydrograph for the main river and '
            '"long_charles" represents a hydrograph for the main river plus additional upstream water sources.'
        ),
        choices=['short_charles', 'long_charles'],
        type=str,
        default='short_charles'
    )
    parser.add_argument(
        '--hydrograph', '-g',
        help='A hydrograph expressed as a list of numeric values where each value represents a proportion of total discharge',
        nargs='*',
        type=float,
    )
    parser.add_argument(
        '--pet_percentile', '-e',
        help='Potential evapotranspiration percentile',
        type=int,
        default=25,
    )
    parser.add_argument(
        '--sm_percentile', '-s',
        help='Soil moisture percentile',
        type=int,
        default=25,
    )
    parser.add_argument(
        '--gw_percentile', '-w',
        help='Ground water percentile',
        type=int,
        default=25,
    )
    parser.add_argument(
        '--output_path', '-o',
        help='Path to write the flood simulation tif file',
        nargs='?',
        type=str,
    )
    parser.add_argument(
        '--no_animation',
        help='Disable display of result animation via matplotlib',
        action='store_false'
    )
    parser.add_argument(
        '--tiff-writer',
        help='Library to use for writing result tiff',
        choices=['rasterio', 'large_image'],
        type=str,
        default='rasterio',
    )
    args = parser.parse_args()
    run_end_to_end(*validate_args(args))
