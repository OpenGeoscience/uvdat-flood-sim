# Dynamic Flood Simulations

Created in collaboration with Northeastern University

## Overview

This end-to-end dynamic flood simulation is intended for use with the Analytics workflow in [UVDAT (Urban Visualization and Data Analysis Toolkit)](https://github.com/OpenGeoscience/uvdat). This module consists of three parts: downscaling prediction, hydrological prediction, and hydrodynamic prediction.

## Explanation

First, an AI downscaling model uses regional climate projections to determine future local precipitation conditions, such as the intensity of extreme rainstorms. These extreme precipitation levels are fed into a hydrological model, which uses precipitation and evapotranspiration to determine runoff and discharge. Finally, a hydrodynamic model uses discharge to map flood depth over time.

This is a proof of concept for the Charles River in Boston that could be translated to other rivers and cities. The user selects the inputs described below, and the output is a flood simulation, represented as a multiframe stacked GeoTIFF raster, a time-varying map of flood depth with one frame per hour for 24 hours.

## Inputs

1. Time Period: the 20 year time period in which to predict a flood. Options are "2031-2050" and "2041-2060" (the former is the default).

2. Annual Probability: the probability that a flood of this magnitude will occur in any given year. This value must be greater than 0 and less than 1. The default is 0.04, which represents a 1 in 25 year flood.

3. Hydrograph: a list of proportions that sum to 1; these represent fractions of the total rainfall volume per timestep. This may also be specified as Hydrograph Name, where options include "short_charles" and "long_charles", which represent premade hydrograph data. The former is the default.

4. Potential Evapotranspiration Percentile: Select the percentile value for potential evapotranspiration

5. Soil Moisture Percentile: Select the percentile value for soil moisture

6. Ground Water Percentile: Select the percentile value for ground water

7. Initial Condition Set: Initial conditions "001", "002", and "003" start real-world emissions from year 1850 with the climate state from the 1001st, 1021st, and 1041st year of a pre-industrial control simulation. Since Earth's climate undergoes multi-year and multi-decadal cycles, the different initializations reveal the range of possible climates in real-world years 2031 and beyond.

## Installation

```
pip install uvdat-flood-sim
```

## Example usage

To run a flood simulation with default inputs:

```
python -m uvdat_flood_sim
```

To see the help menu explaining how to use arguments to specify input values:

```
python -m uvdat_flood_sim --help
```

## Viewing Results

By default, results will be displayed with a `matplotlib` animation. This animation is saved in the outputs folder as `animation.gif`. Results are also saved in the outputs folder as a multiframe geospatial tiff called `flood_simulation.tif`, which can be added to UVDAT for visualization.
