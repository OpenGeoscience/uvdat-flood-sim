import numpy
import tifftools
import large_image_source_zarr

from constants import OUTPUTS_FOLDER, GEOSPATIAL_PROJECTION, GEOSPATIAL_BOUNDS


def modify_tiff_tags(path, nodata=None):
    info = tifftools.read_tiff(path)

    # Remove image description and extra samples (vips says all extra samples are alpha)
    for tag in {338, 270}:
        for ifd in tifftools.commands._iterate_ifds(info['ifds'], True):
            ifd['tags'].pop(tag, None)

    # Copy all geospatial tags to all frames
    for tag in {33550, 33922, 34735, 34736, 34737}:
        for ifd in info['ifds']:
            if tag in info['ifds'][0]['tags']:
                ifd['tags'][tag] = info['ifds'][0]['tags'][tag]

    # Set nodata value
    if nodata is not None:
        for ifd in tifftools.commands._iterate_ifds(info['ifds'], True):
            ifd['tags'][42113] = dict(
                data=str(nodata),
                datatype=tifftools.Datatype.ASCII,
            )

    tifftools.write_tiff(info, path, allowExisting=True, ifdsFirst=True, dedup=True)


def write_multiframe_geotiff(results):
    OUTPUTS_FOLDER.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUTS_FOLDER / 'flood_simulation.tif'
    n_frames, size_y, size_x = results.shape
    sink = large_image_source_zarr.new()
    for t in range(n_frames):
        sink.addTile(results[t], x=0, y=0, t=t)
    sink.projection = GEOSPATIAL_PROJECTION
    min_lng, max_lat, max_lng, min_lat = GEOSPATIAL_BOUNDS
    sink.gcps = [[min_lng, max_lat, 0, 0], [max_lng, min_lat, size_x, size_y]]
    sink.write(output_path, keepFloat=True, overwriteAllowed=True, compression='zstd')

    modify_tiff_tags(output_path, nodata=numpy.min(results))
