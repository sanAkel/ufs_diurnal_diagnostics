#!/usr/bin/env python3

# Load py
# - On Ursa
# source /home/Santha.Akella/pw/software/.miniconda3c/bin/activate  

import matplotlib
# Use the Agg backend for non-interactive environments (e.g., WCOSS2 login nodes)
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import glob
import os

# Configuration
data_path = "/scratch5/NCEPDEV/rstprod/Santha.Akella/tmp/ufs_diurnal_diagnostics/ARAFS/cull_dbuoy/"
date_dir="20251222"
file_pattern = f"drifting_buoys_{date_dir}_*z.csv"
output_plot = f"drifting_buoy_panels_{date_dir}.png"

def plot_buoy_locations():
    # 1. Gather and sort files to ensure 00z, 06z, 12z, 18z order
    files = sorted(glob.glob(os.path.join(data_path, file_pattern)))

    if not files:
        print(f"Error: No files found matching {file_pattern} in {data_path}")
        return

    # 2. Set up the 2x2 Figure
    fig, axes = plt.subplots(
        nrows=2, ncols=2, figsize=(16, 10),
        subplot_kw={'projection': ccrs.PlateCarree()}
    )
    axes = axes.flatten()
    fig.suptitle('Drifting Buoy Locations (Type 564) - f{date_dir}', fontsize=20, y=0.95)

    for i, f in enumerate(files):
        if i >= 4: break  # Limit to 4 panels

        ax = axes[i]
        hour_label = os.path.basename(f).split('_')[-1].replace('.csv', '')

        # Load data
        df = pd.read_csv(f)

        # 3. Map Decoration
        ax.set_global()
        ax.add_feature(cfeature.LAND, facecolor='lightgray', zorder=1)
        ax.add_feature(cfeature.OCEAN, facecolor='aliceblue', zorder=0)
        ax.add_feature(cfeature.COASTLINE, linewidth=0.5, zorder=2)
        ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False, alpha=0.3)

        # 4. Plot Buoys
        # PlateCarree handles the 0-360 Longitude automatically
        ax.scatter(
            df['Longitude'], df['Latitude'],
            color='red', s=2, alpha=0.8,
            transform=ccrs.PlateCarree(),
            label=f'Buoys (n={len(df)})',
            zorder=3
        )

        ax.set_title(f"Cycle: {hour_label.upper()} (n={len(df):,})", fontsize=14, fontweight='bold')
        ax.legend(loc='lower right', markerscale=5)

    # 5. Save the plot
    plt.tight_layout(rect=[0, 0.03, 1, 0.92])
    plt.savefig(output_plot, dpi=120, bbox_inches='tight')
    plt.close(fig) # Clean up memory
    print(f"Plot saved successfully to: {os.path.abspath(output_plot)}")

if __name__ == "__main__":
    plot_buoy_locations()
