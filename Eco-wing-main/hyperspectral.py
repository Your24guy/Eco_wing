import numpy as np
import rasterio
from rasterio.enums import Resampling

def create_hyperspectral_image(width, height, bands):
    """Creates a synthetic hyperspectral image with random data."""
    return np.random.rand(bands, height, width).astype('float32')

def save_hyperspectral_image(image, filepath):
    """Saves the hyperspectral image as a TIFF file."""
    bands, height, width = image.shape
    with rasterio.open(
        filepath, 'w',
        driver='GTiff',
        height=height,
        width=width,
        count=bands,
        dtype=image.dtype
    ) as dst:
        for i in range(bands):
            dst.write(image[i], i + 1)

def main():
    width, height, bands = 100, 100, 10  # Example dimensions and number of bands
    hyperspectral_image = create_hyperspectral_image(width, height, bands)
    save_hyperspectral_image(hyperspectral_image, 'hyperspectral_image.tiff')
    print(f"Hyperspectral image saved as 'hyperspectral_image.tiff'")

if __name__ == "__main__":
    main()
