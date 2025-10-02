import argparse
import numpy
from datetime import datetime
from pathlib import Path

from downscaling_prediction import downscale_boston_cesm
from hydrological_prediction import calculate_discharge_from_precipitation
from hydrodynamic_prediction import generate_flood_from_discharge
from animate_results import animate as animate_results
from save_results import write_multiframe_geotiff

from constants import PERCENTILES, HYDROGRAPHS


def run_end_to_end(
    time_period: str, # Two-decade future period whose climate we are interested in.
    annual_probability: float, # Annual probability of a 1-day extreme precipitation event happening.
    hydrograph: list[float], # List of 24 floats where each is a proportion of flood volume passing through in one hour.
    potential_evapotranspiration: float, # This is a percentile. Can be 25, 50, 75, or 90.
    soil_moisture: float, # This is a percentile. Can be 25, 50, 75, or 90.
    ground_water: float, # This is a percentile. Can be 25, 50, 75, or 90.
    output_path: str | None,
    animate: bool,
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
    flood = generate_flood_from_discharge(q, hydrograph) # numpy array with 2 spatial dimensions and 1 time dimension
    print(f'Hydrodynamic prediction: flood raster with shape {flood.shape}')

    print(f'Done in {(datetime.now() - start).total_seconds()} seconds.\n')

    # Convert flood to multiframe GeoTIFF
    write_multiframe_geotiff(flood, output_path=output_path)
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

    potential_evapotranspiration = PERCENTILES['pet'][args.pet_percentile]
    soil_moisture = PERCENTILES['sm'][args.sm_percentile]
    ground_water = PERCENTILES['gw'][args.gw_percentile]
    hydrograph = hydrograph or HYDROGRAPHS.get(hydrograph_name)
    output_path = Path(output_path)

    return (
        time_period,
        annual_probability,
        hydrograph,
        potential_evapotranspiration,
        soil_moisture,
        ground_water,
        output_path,
        animate
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
        choices=[25, 50, 75, 90],
        type=int,
        default=25,
    )
    parser.add_argument(
        '--sm_percentile', '-s',
        help='Soil moisture percentile',
        choices=[25, 50, 75, 90],
        type=int,
        default=25,
    )
    parser.add_argument(
        '--gw_percentile', '-w',
        help='Ground water percentile',
        choices=[25, 50, 75, 90],
        type=int,
        default=25,
    )
    parser.add_argument(
        '--output_path', '-o',
        help='Path to write the flood simulation tif file',
        type=str,
    )
    parser.add_argument(
        '--no_animation',
        help='Disable display of result animation via matplotlib',
        action='store_false'
    )
    args = parser.parse_args()
    run_end_to_end(*validate_args(args))
