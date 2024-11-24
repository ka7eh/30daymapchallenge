"""
Data from the VIIRS NTL product.

You can get data for other dates from here and change the INPUT_PATH variable: https://search.earthdata.nasa.gov/search/granules?p=C1898025206-LAADS&pg[0][v]=f&pg[0][gsk]=-start_date&q=VNP46A1&sb[0]=13.08833%2C52.33816%2C13.76166%2C52.67583&tl=1730239977!2!!&lat=52.534423828125&long=13.4384765625

More on data source: https://www.earthdata.nasa.gov/topics/human-dimensions/nighttime-lights

Example usage:
# python dnl.py --input-path data/VNP46A2.A2024307.h19v03.001.2024315092628.h5 --boundary-name berlin --marker-coordinates 13.445852097309034,52.50013522309102
"""

import argparse
import json
from pathlib import Path
import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.mask import mask

SCRIPT_PATH = Path(__file__).parent


def create_map(
    input_path: Path,
    boundary_name: str,
    marker_coordinates: tuple[float, float] | None = None,
) -> None:
    # This is for masking the final data with the Berlin boundary
    with open(SCRIPT_PATH / "data" / f"{boundary_name}.geojson") as f:
        boundary = json.load(f)

    bbox = boundary["bbox"]
    bbox_polygon = {
        "type": "Polygon",
        "coordinates": [
            [
                [bbox[0], bbox[1]],
                [bbox[2], bbox[1]],
                [bbox[2], bbox[3]],
                [bbox[0], bbox[3]],
                [bbox[0], bbox[1]],
            ]
        ],
    }

    # This is for the ASCII gradient. The last character is for the Berlin boundary.
    ASCII_GRADIENT = " ░▒▓█."

    with rasterio.open(input_path) as src:
        # We work with the first subdataset, which is the NTL corrected version
        ntl_corrected_path = src.subdatasets[0]

    with rasterio.open(ntl_corrected_path) as src:
        # Crop the data to the Berlin bbox
        cropped_data, cropped_transform = mask(src, [bbox_polygon], crop=True)
        NO_DATA_VALUE = src.nodata
        cropped_data = np.where(cropped_data == NO_DATA_VALUE, 0, cropped_data)[0]

    # Filter out the no data values for min/max calculation and make intervals using the ASCII_GRADIENT length
    filtered_data = cropped_data[cropped_data != NO_DATA_VALUE]
    levels = np.arange(
        filtered_data.min(),
        filtered_data.max(),
        (filtered_data.max() - filtered_data.min()) / (len(ASCII_GRADIENT) - 1),
    ).astype(int)

    # Group the data into levels
    grouped_data = np.digitize(cropped_data, levels)

    # Rasterize Berlin boundary with the shape of the cropped data
    BOUNDARY_VALUE = len(ASCII_GRADIENT)
    berlin_boundary_rasterized = rasterize(
        [boundary],
        default_value=BOUNDARY_VALUE,
        out_shape=cropped_data.shape,
        transform=cropped_transform,
    )

    # Mask the grouped data with the rasterized Berlin boundary, where the boundary overrides the grouped data
    masked_grouped_data = np.where(
        berlin_boundary_rasterized == BOUNDARY_VALUE,
        berlin_boundary_rasterized,
        grouped_data,
    )

    if marker_coordinates:
        # Find the index of the marker coordinates
        col, row = ~cropped_transform * marker_coordinates
        row, col = int(row), int(col)
        print(f"Your coordinates are at row {row}, column {col}")
        masked_grouped_data[row, col] = 0

    # Write the masked data to a text file and also print it.
    with open(SCRIPT_PATH / "data" / f"{boundary_name}_ntl.txt", "w") as f:
        for row in masked_grouped_data:
            row_str = "\t" + "".join(
                "🌎" if level == 0 else ASCII_GRADIENT[int(level) - 1] for level in row
            )
            f.write(row_str + "\n")
            print(row_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=Path, required=True)
    parser.add_argument("--boundary-name", type=str, required=True)
    parser.add_argument("--marker-coordinates", type=str, required=False)
    args = parser.parse_args()

    coords: tuple[float, float] | None = None
    if args.marker_coordinates:
        coords_list = [float(x) for x in args.marker_coordinates.split(",")]
        if len(coords_list) == 2:
            coords = (coords_list[0], coords_list[1])

    create_map(args.input_path, args.boundary_name, coords)
