# Dynamic Flood Simulations

Created in collaboration with Northeastern University

## Overview

This end-to-end dynamic flood simulation is intended for use with the Analytics workflow in [UVDAT (Urban Visualization and Data Analysis Toolkit)](https://github.com/OpenGeoscience/uvdat). This module consists of three parts: downscaling prediction, hydrological prediction, and hydrodynamic prediction.

## Explanation

TODO

## Inputs

1. Time Period: the 20 year time period in which to predict a flood. Right now, the only option available is `2030-2050`, which is the default value.

2. Annual Probability: the probability that a flood of this magnitude will occur in any given year. This value must be greater than 0 and less than 1. The default is 0.04, which represents a 1 in 25 year flood.

3. Hydrograph: a list of proportions that sum to 1; these represent fractions of the total rainfall volume per timestep.

4. Potential Evapotranspiration Percentile: Select the 25th, 50th, 75th, or 90th percentile value for potential evapotranspiration

5. Soil Moisture Percentile: Select the 25th, 50th, 75th, or 90th percentile value for soil moisture

6. Ground Water Percentile: Select the 25th, 50th, 75th, or 90th percentile value for ground water

## Example usage

Install requirements with `pip install -r requirements.txt`.

To run a flood simulation with default inputs:

```
python main.py
```

To see the help menu explaining how to use arguments to specify input values:

```
python main.py -h
```

## Viewing Results

By default, results will be displayed with a `matplotlib` animation. This animation is saved in the outputs folder as `animation.gif`. Results are also saved in the outputs folder as a multiframe geospatial tiff called `flood_simulation.tif`, which can be added to UVDAT for visualization.
