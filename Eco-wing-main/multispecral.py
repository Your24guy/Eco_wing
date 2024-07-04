import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.transform import from_origin

# Create a dummy image with 4 bands (e.g., Blue, Green, Red, NIR)
width, height = 100, 100
num_bands = 4
data = np.random.rand(num_bands, height, width) * 255

# Define transform and metadata for the raster file
transform = from_origin(0, 0, 1, 1)  # arbitrary transform
metadata = {
    'driver': 'GTiff',
    'count': num_bands,
    'width': width,
    'height': height,
    'dtype': 'uint8',
    'crs': '+proj=latlong',
    'transform': transform
}

# Save the image as a TIFF file with 4 bands
with rasterio.open('test_multispectral.tif', 'w', **metadata) as dst:
    for i in range(num_bands):
        dst.write(data[i].astype('uint8'), i + 1)
