from flask import Flask, request, render_template, redirect, url_for
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt
from skimage import io
import shutil

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['STATIC_FOLDER'] = 'static/'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'tif', 'tiff'}

def load_multispectral_image(file_path):
    with rasterio.open(file_path) as dataset:
        bands = [dataset.read(i + 1) for i in range(dataset.count)]
    return bands

def calculate_ndvi(red_band, nir_band):
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    return ndvi

def calculate_evi(red_band, blue_band, nir_band):
    evi = 2.5 * (nir_band - red_band) / (nir_band + 6 * red_band - 7.5 * blue_band + 1)
    return evi

def calculate_savi(red_band, nir_band, L=0.5):
    savi = (nir_band - red_band) / (nir_band + red_band + L) * (1 + L)
    return savi

def analyze_image(bands):
    if len(bands) < 4:
        return None

    blue_band = bands[0]
    green_band = bands[1]
    red_band = bands[2]
    nir_band = bands[3]

    ndvi = calculate_ndvi(red_band, nir_band)
    evi = calculate_evi(red_band, blue_band, nir_band)
    savi = calculate_savi(red_band, nir_band)

    analysis_results = {
        'ndvi': ndvi,
        'evi': evi,
        'savi': savi,
        'soil_composition': np.mean(red_band) * 0.1,
        'water_quality': np.mean(blue_band) * 0.2,
    }

    return analysis_results

def analyze_thermal_image(file_path):
    thermal_image = io.imread(file_path)
    
    # Extract temperature data
    temperature_data = thermal_image

    # Calculate statistics
    min_temp = np.min(temperature_data)
    max_temp = np.max(temperature_data)
    mean_temp = np.mean(temperature_data)

    # Detect hot spots (e.g., pixels with temperature above a certain threshold)
    hot_spot_threshold = 60  # Set an appropriate threshold
    hot_spots = np.where(temperature_data > hot_spot_threshold)

    # Save the thermal image with hot spots for visualization
    plt.imshow(thermal_image, cmap='inferno')
    plt.scatter(hot_spots[1], hot_spots[0], color='blue', marker='o', s=10)
    plt.colorbar(label='Temperature (°C)')
    plt.title('Thermal Image with Hot Spots')
    thermal_image_path = 'thermal_with_hot_spots.png'
    thermal_image_fullpath = os.path.join(app.config['UPLOAD_FOLDER'], thermal_image_path)
    plt.savefig(thermal_image_fullpath)
    plt.close()
    
    # Move the thermal image to the static folder
    static_path = os.path.join(app.config['STATIC_FOLDER'], thermal_image_path)
    shutil.move(thermal_image_fullpath, static_path)

    thermal_results = {
        'min_temp': min_temp,
        'max_temp': max_temp,
        'mean_temp': mean_temp,
        'thermal_image_path': thermal_image_path
    }

    return thermal_results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)
        
        if file.filename.lower().endswith('.tif') or file.filename.lower().endswith('.tiff'):
            try:
                # Try to analyze as a multispectral image first
                bands = load_multispectral_image(filename)
                analysis_results = analyze_image(bands)
                if analysis_results:
                    ndvi_image_path = 'ndvi.png'
                    ndvi_image_fullpath = os.path.join(app.config['UPLOAD_FOLDER'], ndvi_image_path)
                    plt.imshow(analysis_results['ndvi'], cmap='viridis')
                    plt.colorbar()
                    plt.savefig(ndvi_image_fullpath)
                    plt.close()

                    static_path = os.path.join(app.config['STATIC_FOLDER'], ndvi_image_path)
                    shutil.move(ndvi_image_fullpath, static_path)
                    
                    return render_template('results.html', results=analysis_results, ndvi_image_path=ndvi_image_path)
                else:
                    raise ValueError("Insufficient bands for multispectral analysis")
            except Exception as e:
                # If it fails, try to analyze as a thermal image
                thermal_results = analyze_thermal_image(filename)
                return render_template('temperature_result.html', results=thermal_results)

    return "File type not allowed", 400


@app.route('/Multispectral.html')
def multispectral():
    return render_template('Multispectral.html')
@app.route('/HyperSpectral.html')
def hyperspectral():
    return render_template('HyperSpectral.html')
@app.route('/Thermal.html')
def thermal():
    return render_template('Thermal.html')
@app.route('/lidar.html')
def lidar():
    return render_template('lidar.html')
@app.route('/gassensor.html')
def gassensor():
    return render_template('gassensor.html')
@app.route('/LoginSign.html')
def login():
    return render_template('LoginSign.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['STATIC_FOLDER']):
        os.makedirs(app.config['STATIC_FOLDER'])
    app.run(debug=True)
