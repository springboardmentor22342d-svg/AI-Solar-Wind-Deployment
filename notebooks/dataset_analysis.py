# Dataset Analysis Notebook – Solar & Wind Deployment Intelligence Platform
# Day 2 Task: Analyze the datasets
# Run this script to perform exploratory data analysis on all datasets.

# This file acts as a Python script version of the analysis notebook.
# To convert to a Jupyter Notebook, run: jupytext --to notebook dataset_analysis.py

# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
# ---

# %% [markdown]
# # Dataset Analysis – Solar & Wind Deployment Intelligence Platform
# **Day 2 | Infosys Virtual Internship**
#
# This notebook analyzes all five datasets used in the platform:
# 1. NASA POWER – Solar irradiance and climate data
# 2. Global Wind Atlas – Wind speed data
# 3. Sentinel-2 – Satellite imagery metrics
# 4. OpenStreetMap – Infrastructure data
# 5. SRTM – Elevation and terrain data

# %% [markdown]
# ## 1. Setup

# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.figsize'] = (12, 5)
from pathlib import Path

DATASETS_DIR = Path('../datasets')

print("✅ Libraries loaded successfully")
print(f"📁 Datasets directory: {DATASETS_DIR.resolve()}")

# %% [markdown]
# ## 2. NASA POWER – Solar Irradiance & Climate Data

# %%
nasa_path = DATASETS_DIR / 'nasa_power/nasa_power_climate_risk_indices_190_capitals_1990_2024.csv'

if nasa_path.exists():
    nasa_df = pd.read_csv(nasa_path)
    print(f"✅ NASA POWER loaded | Shape: {nasa_df.shape}")
    print(f"\n📋 Columns ({len(nasa_df.columns)}):")
    print(nasa_df.columns.tolist())
    print(f"\n🔍 Data Types:\n{nasa_df.dtypes.value_counts()}")
    print(f"\n📊 First 3 rows:\n{nasa_df.head(3)}")
    print(f"\n❓ Missing values:\n{nasa_df.isnull().sum()[nasa_df.isnull().sum() > 0]}")
    print(f"\n📈 Numeric summary:\n{nasa_df.describe().round(2)}")
else:
    print(f"❌ File not found: {nasa_path}")

# %%
# Visualize solar irradiance distribution (if column exists)
if nasa_path.exists():
    irr_cols = [c for c in nasa_df.columns if 'ALLSKY' in c or 'irr' in c.lower() or 'solar' in c.lower()]
    if irr_cols:
        fig, axes = plt.subplots(1, len(irr_cols[:3]), figsize=(15, 4))
        if len(irr_cols) == 1:
            axes = [axes]
        for ax, col in zip(axes, irr_cols[:3]):
            nasa_df[col].dropna().hist(bins=40, ax=ax, color='#FF8C00', edgecolor='white')
            ax.set_title(f'{col}\n(Solar Irradiance Distribution)')
            ax.set_xlabel('kWh/m²/day')
            ax.set_ylabel('Frequency')
        plt.suptitle('NASA POWER – Solar Irradiance Distribution', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('../reports/nasa_power_irradiance_distribution.png', dpi=150, bbox_inches='tight')
        plt.show()
        print("✅ Plot saved to reports/")

# %% [markdown]
# ## 3. Global Wind Atlas – Wind Speed Data

# %%
gwa_path = DATASETS_DIR / 'global_wind_atlas/gwa_data.csv'

if gwa_path.exists():
    gwa_df = pd.read_csv(gwa_path)
    print(f"✅ Global Wind Atlas loaded | Shape: {gwa_df.shape}")
    print(f"\n📋 Columns: {gwa_df.columns.tolist()}")
    print(f"\n📊 First 3 rows:\n{gwa_df.head(3)}")
    print(f"\n📈 Summary statistics:\n{gwa_df.describe().round(2)}")

    wind_cols = [c for c in gwa_df.columns if 'wind' in c.lower() or 'speed' in c.lower()]
    if wind_cols:
        fig, ax = plt.subplots(figsize=(10, 4))
        for col in wind_cols:
            gwa_df[col].dropna().hist(bins=30, ax=ax, alpha=0.7, label=col)
        ax.set_title('Global Wind Atlas – Wind Speed Distribution')
        ax.set_xlabel('Wind Speed (m/s)')
        ax.set_ylabel('Frequency')
        ax.legend()
        plt.tight_layout()
        plt.savefig('../reports/gwa_wind_speed_distribution.png', dpi=150, bbox_inches='tight')
        plt.show()
        print("✅ Plot saved to reports/")
else:
    print(f"❌ File not found: {gwa_path}\n   ℹ  Run run_day2.py first to generate sample data.")

# %% [markdown]
# ## 4. Sentinel-2 – Satellite Imagery Metrics

# %%
sentinel_path = DATASETS_DIR / 'sentinel/sentinel2_data.csv'

if sentinel_path.exists():
    sentinel_df = pd.read_csv(sentinel_path)
    print(f"✅ Sentinel-2 loaded | Shape: {sentinel_df.shape}")
    print(f"\n📋 Columns: {sentinel_df.columns.tolist()}")
    print(f"\n📊 First 3 rows:\n{sentinel_df.head(3)}")
    print(f"\n📈 Summary:\n{sentinel_df.describe().round(3)}")
else:
    print(f"❌ File not found: {sentinel_path}")

# %% [markdown]
# ## 5. OpenStreetMap – Infrastructure Data

# %%
osm_path = DATASETS_DIR / 'openstreetmap/osm_infrastructure.csv'

if osm_path.exists():
    osm_df = pd.read_csv(osm_path)
    print(f"✅ OpenStreetMap loaded | Shape: {osm_df.shape}")
    print(f"\n📋 Columns: {osm_df.columns.tolist()}")
    print(f"\n📊 First 3 rows:\n{osm_df.head(3)}")

    if 'type' in osm_df.columns:
        print(f"\n🏗 Infrastructure types:\n{osm_df['type'].value_counts()}")
else:
    print(f"❌ File not found: {osm_path}")

# %% [markdown]
# ## 6. SRTM – Elevation & Terrain Data

# %%
srtm_path = DATASETS_DIR / 'srtm/srtm_elevation.csv'

if srtm_path.exists():
    srtm_df = pd.read_csv(srtm_path)
    print(f"✅ SRTM loaded | Shape: {srtm_df.shape}")
    print(f"\n📋 Columns: {srtm_df.columns.tolist()}")
    print(f"\n📊 First 3 rows:\n{srtm_df.head(3)}")
    print(f"\n📈 Summary:\n{srtm_df.describe().round(2)}")
else:
    print(f"❌ File not found: {srtm_path}")

# %% [markdown]
# ## 7. Dataset Summary

# %%
print("\n" + "="*60)
print("DATASET SUMMARY")
print("="*60)

datasets = {
    'NASA POWER':        nasa_path,
    'Global Wind Atlas': gwa_path,
    'Sentinel-2':        sentinel_path,
    'OpenStreetMap':     osm_path,
    'SRTM Elevation':    srtm_path,
}

purposes = {
    'NASA POWER':        'Solar irradiance, climate risk → Solar Prediction',
    'Global Wind Atlas': 'Wind speed at height → Wind Prediction',
    'Sentinel-2':        'NDVI, land cover → Environmental Constraints',
    'OpenStreetMap':     'Grid distance, roads → Connection Cost Analysis',
    'SRTM Elevation':    'Elevation, slope → Site Suitability Scoring',
}

for name, path in datasets.items():
    status = "✅ Found" if path.exists() else "❌ Missing"
    print(f"\n{name:<22} {status}")
    print(f"  Purpose: {purposes[name]}")
    if path.exists():
        df = pd.read_csv(path)
        print(f"  Shape:   {df.shape[0]:,} rows × {df.shape[1]} columns")

print("\n" + "="*60)
print("✅ Dataset analysis complete!")
print("="*60)
