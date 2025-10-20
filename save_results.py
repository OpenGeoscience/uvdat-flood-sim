import numpy
from pathlib import Path
from constants import OUTPUTS_FOLDER, GEOSPATIAL_PROJECTION, GEOSPATIAL_BOUNDS


def rasterio_write(results, output_path):
    import rasterio

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


def modify_tiff_tags(path, nodata=None):
    import tifftools
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


def large_image_write(results, output_path):
    import large_image_source_zarr

    n_frames, size_y, size_x = results.shape
    sink = large_image_source_zarr.new()
    for t in range(n_frames):
        sink.addTile(results[t], x=0, y=0, t=t)
    sink.projection = GEOSPATIAL_PROJECTION
    min_lng, max_lat, max_lng, min_lat = GEOSPATIAL_BOUNDS
    sink.gcps = [[min_lng, max_lat, 0, 0], [max_lng, min_lat, size_x, size_y]]
    sink.write(output_path, keepFloat=True, overwriteAllowed=True, compression='zstd')

    modify_tiff_tags(output_path, nodata=numpy.min(results))
    print(f'Wrote GeoTIFF to {output_path}.')


def write_multiframe_geotiff(results, output_path=None, writer='rasterio'):
    if output_path is None:
        output_path = OUTPUTS_FOLDER / 'flood_simulation.tif'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if writer == 'rasterio':
        rasterio_write(results, output_path)
    elif writer == 'large_image':
        large_image_write(results, output_path)
