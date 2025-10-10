import numpy
import rasterio
from pathlib import Path
from constants import OUTPUTS_FOLDER, GEOSPATIAL_PROJECTION, GEOSPATIAL_BOUNDS


def write_multiframe_geotiff(results, output_path=None):
    if output_path is None:
        output_path = OUTPUTS_FOLDER / 'flood_simulation.tif'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    n_frames, size_y, size_x = results.shape
    min_lng, max_lat, max_lng, min_lat = GEOSPATIAL_BOUNDS
    profile = dict(
        driver='GTiff',
        count=n_frames,
        height=size_y,
        width=size_x,
        dtype=results.dtype,
        nodata=numpy.min(results),
        crs=GEOSPATIAL_PROJECTION,
        transform=rasterio.transform.from_gcps([
            rasterio.transform.GroundControlPoint(0, 0, min_lng, max_lat),
            rasterio.transform.GroundControlPoint(size_y, size_x, max_lng, min_lat),
        ])
    )
    with rasterio.open(output_path, 'w', **profile) as dst:
        dst.write(results)
    print(f'Wrote GeoTIFF to {output_path}.')
