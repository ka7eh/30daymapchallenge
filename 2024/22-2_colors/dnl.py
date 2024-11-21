"""
Data from the VIIRS NTL product.

You can get data for other dates from here and change the INPUT_PATH variable: https://search.earthdata.nasa.gov/search/granules?p=C1898025206-LAADS&pg[0][v]=f&pg[0][gsk]=-start_date&q=VNP46A1&sb[0]=13.08833%2C52.33816%2C13.76166%2C52.67583&tl=1730239977!2!!&lat=52.534423828125&long=13.4384765625

More on data source: https://www.earthdata.nasa.gov/topics/human-dimensions/nighttime-lights
"""

import json
from pathlib import Path
import numpy as np
import rasterio
from rasterio.features import rasterize
from rasterio.mask import mask

SCRIPT_PATH = Path(__file__).parent

INPUT_PATH = SCRIPT_PATH / "data/VNP46A2.A2024307.h19v03.001.2024315092628.h5"

# This is for masking the final data with the Berlin boundary
with open(SCRIPT_PATH / "data/berlin.geojson") as f:
    BERLIN_BOUNDARY = json.load(f)

# This is for clipping the data to the Berlin bbox
BERLIN_BBOX = {
    "type": "Polygon",
    "coordinates": [
        [
            [13.088333, 52.338167],
            [13.761667, 52.338167],
            [13.761667, 52.675833],
            [13.088333, 52.675833],
            [13.088333, 52.338167],
        ]
    ],
}

LIVEEO_COORDINATES = (13.445852097309034, 52.50013522309102)

# This is for the ASCII gradient. The last character is for the Berlin boundary.
ASCII_GRADIENT = " ░▒▓█."

with rasterio.open(INPUT_PATH) as src:
    # We work with the first subdataset, which is the NTL corrected version
    ntl_corrected_path = src.subdatasets[0]

with rasterio.open(ntl_corrected_path) as src:
    # Crop the data to the Berlin bbox
    cropped_data, cropped_transform = mask(src, [BERLIN_BBOX], crop=True)
    NO_DATA_VALUE = src.nodata
    cropped_data = np.where(cropped_data == NO_DATA_VALUE, 0, cropped_data)[0]


# Filter out the no data values for min/max calculation and make intervals using the ASCII_GRADIENT length
filtered_data = cropped_data[cropped_data != NO_DATA_VALUE]
levels = np.arange(
    filtered_data.min(),
    filtered_data.max(),
    (filtered_data.max() - filtered_data.min()) / (len(ASCII_GRADIENT) - 1),
)

# Group the data into levels
grouped_data = np.digitize(cropped_data, levels)

# Rasterize Berlin boundary with the shape of the cropped data
BOUNDARY_VALUE = len(ASCII_GRADIENT)
berlin_boundary_rasterized = rasterize(
    [BERLIN_BOUNDARY],
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

# Find the index of the LiveEO coordinates
col, row = ~cropped_transform * LIVEEO_COORDINATES
row, col = int(row), int(col)
print(f"LiveEO coordinates are at row {row}, column {col}")
masked_grouped_data[row, col] = 0

# Write the masked data to a text file and also print it.
with open(SCRIPT_PATH / "data/berlin_ntl.txt", "w") as f:
    for row in masked_grouped_data:
        row_str = "\t" + "".join(
            "🌎" if level == 0 else ASCII_GRADIENT[level - 1] for level in row
        )
        f.write(row_str + "\n")
        print(row_str)
