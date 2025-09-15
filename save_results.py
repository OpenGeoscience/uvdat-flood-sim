import numpy
import large_image_source_zarr

from constants import OUTPUTS_FOLDER, GEOSPATIAL_PROJECTION, GEOSPATIAL_BOUNDS


def write_multiframe_geotiff(results):
    output_path = OUTPUTS_FOLDER / 'flood_simulation.tif'
    n_frames, size_y, size_x = results.shape
    sink = large_image_source_zarr.new()
    for t in range(n_frames):
        sink.addTile(results[t], x=0, y=0, t=t)
    sink.projection = GEOSPATIAL_PROJECTION
    min_lng, min_lat, max_lng, max_lat = GEOSPATIAL_BOUNDS
    sink.gcps = [[min_lng, min_lat, 0, 0], [max_lng, max_lat, size_x, size_y]]
    sink.write(output_path)
