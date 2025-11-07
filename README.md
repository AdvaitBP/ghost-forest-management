# Ghost Forest Management

## Overview
Ghost forests across coastal North Carolina reveal the cascading impacts of sea-level rise, saltwater intrusion, and changing land use on once-thriving maritime forests. This repository supports research focused on the Albemarle and Pamlico Sounds region, where remote-sensing analyses and management scenarios inform conservation and adaptation planning. The workflow combines Python-based geospatial processing with interactive storytelling to surface the ecological, cultural, and policy dimensions of these landscape transitions.

## Repository Structure
- `scripts/`: Production-ready automation for exporting annual Landsat NDVI composites via the Google Earth Engine Python API.
- `docs/`: Narrative and operational documentation, including the NDVI export walkthrough for collaborators and reviewers.

## Data Sources
- **Landsat Surface Reflectance (Collections 5, 7, 8):** Retrieved through the Google Earth Engine (GEE) Python API to build long-term NDVI composites that capture vegetation change from 1985 to the present.
- **Derived NDVI Time Series:** Median annual composites clipped to the Albemarle Peninsula to quantify vegetation vigor, forest loss, and marsh transition hotspots that appear in the StoryMap narratives.
- **Historical and Community Context:** Qualitative accounts, archival imagery, and local histories referenced in the Ghost (Forest) Stories ArcGIS StoryMap to ground quantitative trends in lived experience.
- **Management Strategy Profiles:** Scenario descriptions for thin-layer sediment placement, salt-tolerant plantings, living shorelines, and hydrologic barriers synthesized for decision support.

## Methodology
1. **Data Ingestion:** Authenticate with Google Earth Engine and assemble Landsat collections by year, masking clouds and harmonizing band names across sensors.
2. **NDVI Composite Generation:** Calculate median NDVI mosaics for user-specified years, clip to the Albemarle Peninsula, and queue Drive exports for downstream analysis.
3. **Interpretation & Storytelling:** Integrate NDVI outputs with field observations, community interviews, and historical research showcased in the Ghost (Forest) Stories StoryMap to highlight environmental change drivers and community responses.

## Results
- **Landscape Change Detection:** NDVI composites reveal the expansion of marshes and decline of canopy vigor, aligning with StoryMap imagery showing toppled trees and salt-scarred stands along the Albemarle Peninsula.
- **Management Scenario Insights:** StoryMap sections distill quantitative outputs into actionable guidance on sediment nourishment, salt-tolerant planting schemes, and shoreline stabilization to bolster ecosystem resilience.

### ArcGIS StoryMap
Explore the companion StoryMap, **[Ghost (Forest) Stories](https://storymaps.arcgis.com/stories/eabc31ae132e42149e7cf1800c5985a3)**, for interactive maps, historical timelines, and management strategy spotlights that contextualize the NDVI analyses and connect them to stakeholder narratives.

## Next Steps
- Incorporate salinity, hydrology, and land-use datasets to pair NDVI trends with abiotic drivers of forest decline.
- Expand time-series modeling to include predictive scenarios that estimate future ghost forest extent under alternative management strategies.
- Automate data pipelines for StoryMap updates so new analyses and community feedback seamlessly refresh the narrative content.
- Collaborate with regional partners to validate model outputs and co-design adaptation investments for vulnerable communities.

## Quickstart
**What the script does:** `scripts/landsat_ndvi_export.py` authenticates with Google Earth Engine, merges Landsat 5/7/8 collections, computes annual median NDVI composites for the Albemarle Peninsula, and exports them to Google Drive for mapping and scenario evaluation.

> 📘 Looking for a detailed walkthrough? See [docs/gee-workflow.md](docs/gee-workflow.md) for step-by-step guidance on configuring Earth Engine parameters, running the export script, and aligning outputs with the StoryMap.

**Prerequisites:**
- Python 3.8+
- `earthengine-api` (see `requirements.txt` for dependencies)
- Approved Google Earth Engine account with CLI authentication configured (`earthengine authenticate`)
- Access to a Google Drive folder for NDVI exports

**How to run:**
1. Install dependencies: `pip install -r requirements.txt`.
2. Authenticate Earth Engine: `earthengine authenticate` (or `earthengine authenticate --quiet` for headless environments).
3. Update the region geometry, years, and export parameters in the script as needed.
4. Execute `python scripts/landsat_ndvi_export.py` to trigger NDVI exports. Monitor progress in the Earth Engine Tasks tab or the console logs.

**Output:** Annual NDVI rasters stored in your Google Drive (`GEE_Exports/NDVI_<YEAR>_Albemarle.tif`) ready for integration into spatial analyses, dashboards, or the Ghost (Forest) Stories StoryMap.
