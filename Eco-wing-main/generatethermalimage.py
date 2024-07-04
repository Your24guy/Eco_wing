import numpy as np
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt

# Define image dimensions
width = 512
height = 512

# Create a grid of temperatures
# Example: random temperatures between 10°C to 40°C
temperatures = np.random.uniform(low=10, high=40, size=(height, width))

# Define metadata for the TIFF file
metadata = {
    'driver': 'GTiff',
    'count': 1,  # Number of bands
    'dtype': 'float32',  # Data type of the pixel values
    'width': width,
    'height': height,
    'crs': 'EPSG:4326',  # Coordinate Reference System (WGS84)
    'transform': from_origin(0, 0, 1, 1)  # Affine transformation (pixel size: 1x1)
}

# Save the synthetic thermal image as a TIFF file
output_tiff_path = 'synthetic_thermal_image.tif'
with rasterio.open(output_tiff_path, 'w', **metadata) as dst:
    dst.write(temperatures.astype(np.float32), 1)  # Write the temperatures to the TIFF file

# Display the synthetic thermal image (optional)
plt.figure(figsize=(8, 6))
plt.imshow(temperatures, cmap='inferno', interpolation='nearest')
plt.colorbar(label='Temperature (°C)')
plt.title('Synthetic Thermal Image')
plt.axis('off')  # Turn off axis for better visualization
plt.show()

print(f"Synthetic thermal image saved as: {output_tiff_path}")
