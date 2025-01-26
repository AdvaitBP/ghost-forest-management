#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
landsat_ndvi.py
---------------
A robust script to generate NDVI composites (median) for multiple Landsat collections 
across a range of years, apply cloud masking, and export to Google Drive.

Usage:
  1) Activate your Python environment (venv).
  2) Ensure 'earthengine-api' is installed and Earth Engine is authenticated.
  3) Run: python landsat_ndvi.py
"""

import ee
import datetime
import sys

# ------------------------ USER CONFIGURATIONS ------------------------

# Years to analyze: here, every 5 years from 1985 to 2020 (inclusive).
START_YEARS = list(range(1985, 2021, 5))

# Region of interest (Albemarle Peninsula approx. bounding box).
# You can refine this or replace with your own AOI geometry.
REGION = ee.Geometry.Rectangle([-76.5, 35.5, -75.5, 36.5])

# Output folder in your Google Drive (must exist or GEE will create it).
DRIVE_FOLDER = 'GEE_Exports'

# Desired projection scale (meters). Landsat ~30m resolution.
SCALE = 30

# CRS
CRS = 'EPSG:4326'

# Landsat Collections (Tier 1, Surface Reflectance). 
# Using older collections for historical coverage:
LANDSAT_COLLECTIONS = {
    'LANDSAT_5':  'LANDSAT/LT05/C02/T1_L2',  # Available 1984 - 2012
    'LANDSAT_7':  'LANDSAT/LE07/C02/T1_L2',  # Available 1999 - present
    'LANDSAT_8':  'LANDSAT/LC08/C02/T1_L2',  # Available 2013 - present
}

# Define sensor-specific band names
SENSOR_BANDS = {
    'LANDSAT_5': {'nir': 'SR_B4', 'red': 'SR_B3', 'qa': 'QA_PIXEL'},
    'LANDSAT_7': {'nir': 'SR_B4', 'red': 'SR_B3', 'qa': 'QA_PIXEL'},
    'LANDSAT_8': {'nir': 'SR_B5', 'red': 'SR_B4', 'qa': 'QA_PIXEL'},
}

# -------------------------------------------------------------

def mask_clouds(image, sensor_key):
    """
    Mask clouds and shadows using the QA_PIXEL band.
    Adjust bitwise logic if needed for different sensors or GEE versions.
    """
    qa = image.select(SENSOR_BANDS[sensor_key]['qa'])
    
    # Bits 3 = cloud shadow, 5 = cloud
    cloud_shadow_bit_mask = 1 << 3
    clouds_bit_mask = 1 << 5
    
    mask = qa.bitwiseAnd(cloud_shadow_bit_mask).eq(0).And(
           qa.bitwiseAnd(clouds_bit_mask).eq(0))
    return image.updateMask(mask)

def add_ndvi(image, sensor_key):
    """
    Calculate NDVI using the sensor-specific RED and NIR bands.
    NDVI = (NIR - RED) / (NIR + RED)
    """
    nir_band = SENSOR_BANDS[sensor_key]['nir']
    red_band = SENSOR_BANDS[sensor_key]['red']
    ndvi = image.normalizedDifference([nir_band, red_band]).rename('NDVI')
    return image.addBands(ndvi)

def get_landsat_collection(sensor_key, start_date, end_date):
    """
    Fetch, cloud-mask, and add NDVI for the specified sensor (L5, L7, or L8)
    within the given date range.
    """
    collection_id = LANDSAT_COLLECTIONS[sensor_key]
    try:
        collection = (ee.ImageCollection(collection_id)
                      .filterDate(start_date, end_date)
                      .map(lambda img: mask_clouds(img, sensor_key))
                      .map(lambda img: add_ndvi(img, sensor_key))
                     )
        return collection
    except Exception as e:
        print(f"Error fetching collection {sensor_key} for dates {start_date} to {end_date}: {e}")
        return ee.ImageCollection([])

def combine_collections(start_date, end_date):
    """
    Combine L5, L7, and L8 collections for the date range,
    as some years might have multiple sensors operational.
    """
    combined = ee.ImageCollection([])
    
    for sensor_key in LANDSAT_COLLECTIONS.keys():
        sensor_coll = get_landsat_collection(sensor_key, start_date, end_date)
        combined = combined.merge(sensor_coll)
    
    return combined

def export_ndvi(year):
    """
    For a given year, build a date range, fetch and combine sensor data,
    create a median NDVI image, and export to Google Drive.
    """
    # Build date range for the entire year
    start_date = f"{year}-01-01"
    end_date   = f"{year}-12-31"
    
    print(f"Processing year: {year}")
    
    collection = combine_collections(start_date, end_date)
    
    # Check if collection is empty
    if collection.size().getInfo() == 0:
        print(f"No images found for year {year}. Skipping export.")
        return
    
    # Create median composite focusing on NDVI band
    median_image = collection.median().select(['NDVI'])
    
    # Clip to region
    composite_clipped = median_image.clip(REGION)
    
    # Prepare export task
    file_prefix = f"NDVI_{year}_Albemarle"
    task = ee.batch.Export.image.toDrive(
        image=composite_clipped,
        description=file_prefix,
        folder=DRIVE_FOLDER,
        fileNamePrefix=file_prefix,
        region=REGION.toGeoJSON()['coordinates'],
        scale=SCALE,
        crs=CRS,
        maxPixels=1e13  # Increase if dealing w/ large areas
    )
    
    try:
        task.start()
        print(f"Export to Google Drive started for year {year}.")
    except Exception as e:
        print(f"Failed to start export for year {year}: {e}")

def main():
    print("Starting NDVI export script...")
    
    # Loop through specified years
    for y in START_YEARS:
        # Handle pre-1984 data (only L5 available)
        if y < 1984:
            print(f"Year {y} is before Landsat 5 availability. Skipping.")
            continue
        
        # Handle data availability based on sensor timelines
        if y <= 2012:
            sensors = ['LANDSAT_5']
        elif y <= 2013:
            sensors = ['LANDSAT_5', 'LANDSAT_7']
        else:
            sensors = ['LANDSAT_7', 'LANDSAT_8']
        
        export_ndvi(y)
    
    print("All exports have been triggered. Check your GEE Tasks panel or monitor logs.")

if __name__ == "__main__":
    try:
        main()
    except ee.ee_exception.EEException as ee_e:
        print(f"Earth Engine Error: {ee_e}")
        print("Ensure your Earth Engine account is approved and authenticated.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
