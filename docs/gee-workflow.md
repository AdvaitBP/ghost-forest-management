# Google Earth Engine Workflow Guide

This guide walks through the Google Earth Engine (GEE) workflow used to generate vegetation change products for the Ghost (Forest) Stories project. Follow these steps to reproduce the NDVI composites that power the StoryMap visuals and decision-support analyses.

## Prerequisites
- **Google Earth Engine account:** Request access at [earthengine.google.com](https://earthengine.google.com/). Approval is required before you can run scripts or export data.
- **Python environment:** Python 3.8+ with the [`earthengine-api`](https://developers.google.com/earth-engine/guides/python_install) package installed. Install project dependencies with `pip install -r requirements.txt`.
- **Authentication:** Run `earthengine authenticate` from your terminal. A browser window will prompt you to sign into your Google account and authorize Earth Engine. Once authenticated, the credentials will be cached locally for the Python API.
- **Google Drive access:** Ensure you have a Drive folder available for receiving Earth Engine exports (e.g., `GEE_Exports`). Verify that your account has sufficient storage space.

## Configure Workflow Parameters
The primary automation lives in `scripts/landsat_ndvi_export.py`. Edit the variables in the `if __name__ == "__main__":` block to match your study area and output preferences.

1. **Year range:** Update the `YEARS` list to the range of analysis years you need. Example: `YEARS = list(range(1985, 2024))`.
2. **Region of interest:** Replace `REGION` with a valid Earth Engine geometry describing your project boundary. You can:
   - Import a shapefile or feature collection from your Earth Engine assets and call `ee.FeatureCollection("users/you/albemarle_peninsula").geometry()`.
   - Define a geometry manually using coordinates, e.g. `ee.Geometry.Polygon([...])`.
3. **Drive export folder:** Set `DRIVE_FOLDER` to the name of an existing folder in your Google Drive where the rasters should be saved (e.g., `DRIVE_FOLDER = "GEE_Exports"`).
4. **File naming:** Customize `FILE_PREFIX` if you want to distinguish between scenarios or regions. Filenames follow the pattern `<FILE_PREFIX>_<YEAR>_Albemarle.tif`.

## Run the Script
1. Activate your Python environment and ensure `earthengine-api` is installed.
2. Authenticate with Earth Engine if you have not already (`earthengine authenticate`).
3. Execute the workflow: `python scripts/landsat_ndvi_export.py`.
4. Monitor the console output. Each year’s export will appear in the Earth Engine Tasks tab; click **Run** if manual confirmation is required.
5. Wait for the tasks to finish. Earth Engine will write each GeoTIFF to the specified Google Drive folder.

## Expected Outputs
- **File names:** GeoTIFF rasters named `<FILE_PREFIX>_<YEAR>_Albemarle.tif` (e.g., `NDVI_2005_Albemarle.tif`).
- **Destination:** Saved in the Google Drive folder defined by `DRIVE_FOLDER`.
- **Usage in the StoryMap:** These rasters are ingested into ArcGIS Pro and shared as tiled imagery layers that appear in the [Ghost (Forest) Stories StoryMap](https://storymaps.arcgis.com/stories/eabc31ae132e42149e7cf1800c5985a3). Each map section references specific years to illustrate marsh migration, canopy decline, and management strategy hotspots derived from the NDVI trends.

## Next Steps After Export
1. Download the GeoTIFFs from Google Drive or access them directly in ArcGIS Pro.
2. Publish the rasters as hosted imagery layers in ArcGIS Online or Enterprise.
3. Update the StoryMap web maps to point to the new layers so that the visual narrative stays synchronized with the latest analyses.

Following this process ensures the geospatial products showcased to stakeholders and employers match the reproducible workflow documented in this repository.
