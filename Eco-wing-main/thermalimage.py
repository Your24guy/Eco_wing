import numpy as np
import matplotlib.pyplot as plt
from skimage import io, exposure

# Load the thermal image
thermal_image = io.imread('synthetic_thermal_image.tif')

# Display the thermal image
plt.imshow(thermal_image, cmap='inferno')
plt.colorbar(label='Temperature (°C)')
plt.title('Thermal Image')
plt.show()

# Extract temperature data
temperature_data = thermal_image

# Calculate statistics
min_temp = np.min(temperature_data)
max_temp = np.max(temperature_data)
mean_temp = np.mean(temperature_data)

print(f"Min Temperature: {min_temp:.2f}°C")
print(f"Max Temperature: {max_temp:.2f}°C")
print(f"Mean Temperature: {mean_temp:.2f}°C")

# Detect hot spots (e.g., pixels with temperature above a certain threshold)
hot_spot_threshold = 60  # Set an appropriate threshold
hot_spots = np.where(temperature_data > hot_spot_threshold)

# Display hot spots on the thermal image
plt.imshow(thermal_image, cmap='inferno')
plt.scatter(hot_spots[1], hot_spots[0], color='blue', marker='o', s=10)
plt.colorbar(label='Temperature (°C)')
plt.title('Thermal Image with Hot Spots')
plt.show()
