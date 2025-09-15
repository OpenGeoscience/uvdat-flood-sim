import argparse
import numpy
from datetime import datetime

from downscaling_prediction import downscale_boston_cesm
from hydrological_prediction import calculate_discharge_from_precipitation
from hydrodynamic_prediction import generate_flood_from_discharge
from animate_results import animate

from constants import PERCENTILES, DEFAULT_HYDROGRAPH


def run_end_to_end(
    time_period: str,
    annual_probability: float,
    unitless_hydrograph: list[float],
    potential_evapotranspiration: float,
    soil_moisture: float,
    ground_water: float,
):
    print(f'Inputs: {time_period=}, {annual_probability=}, {unitless_hydrograph=}, {potential_evapotranspiration=}, {soil_moisture=}, {ground_water=}')
    start = datetime.now()

    level = downscale_boston_cesm(time_period, annual_probability)
    print(f'Downscaling prediction: precipitation level = {level}')

    q = calculate_discharge_from_precipitation(
        level,
        potential_evapotranspiration,
        soil_moisture,
        ground_water,
    )
    print(f'Hydrological prediction: discharge value = {q}')

    flood = generate_flood_from_discharge(q, unitless_hydrograph)
    print(f'Hydrodynamic prediction: flood raster with shape {flood.shape}')

    print(f'Done in {(datetime.now() - start).total_seconds()} seconds.\n')
    animate(flood)


def validate_args(args):
    time_period, annual_probability, unitless_hydrograph = (
        args.time_period, args.annual_probability, args.unitless_hydrograph
    )
    if annual_probability <= 0 or annual_probability >= 1:
        raise Exception('Annual probability must be >0 and <1.')
    if not numpy.isclose(numpy.sum(unitless_hydrograph), 1):
        raise Exception('Unitless hydrograph must have a sum of 1.')

    potential_evapotranspiration = PERCENTILES['pet'][args.pet_percentile]
    soil_moisture = PERCENTILES['sm'][args.sm_percentile]
    ground_water = PERCENTILES['gw'][args.gw_percentile]

    return (
        time_period,
        annual_probability,
        unitless_hydrograph,
        potential_evapotranspiration,
        soil_moisture,
        ground_water,
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
        '--unitless_hydrograph', '-u',
        help='A list of proportions that sum to 1; these represent fractions of the total rainfall volume per timestep.',
        nargs='*',
        type=float,
        default=DEFAULT_HYDROGRAPH
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
    args = parser.parse_args()
    run_end_to_end(*validate_args(args))
