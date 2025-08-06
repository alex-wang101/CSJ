import pandas as pd
import glob
import os

# Directory containing your CSV files
csv_dir = "./"  # Change this if files are in a different folder

# Get all merged_output CSVs
csv_files = glob.glob(os.path.join(csv_dir, "merged_output_*.csv"))

# Dictionary to store dataframes per amenity
amenity_data = {}

# Load and process each CSV
for file_path in csv_files:
    df = pd.read_csv(file_path)
    # Get amenity type from filename (e.g., "grocery" from "merged_output_grocery.csv")
    amenity = os.path.basename(file_path).replace("merged_output_", "").replace(".csv", "")
    # Set distance threshold (special case for hospital)
    if amenity == "hospital":
        distance_threshold = 1
    else:
        distance_threshold = 0.5
    # Filter by distance
    df_filtered = df[df["Distance (km)"] < distance_threshold]
    # Count number of targets per DAUID
    counts = df_filtered.groupby("DAUID").size().reset_index(name=amenity + "_count")
    # Special case: if amenity is 'waterfront', limit counts to 1
    if amenity == "waterfront":
        counts[amenity + "_count"] = counts[amenity + "_count"].clip(upper=1)
    # Store Residential_TotalGross_Average
    avg = df[["DAUID", "Residential_TotalGross_Average"]].drop_duplicates()
    # Merge counts and averages
    merged = pd.merge(counts, avg, on="DAUID", how="left")
    amenity_data[amenity] = merged

# Merge all amenity dataframes together on DAUID
output_df = None
for df in amenity_data.values():
    if output_df is None:
        output_df = df
    else:
        output_df = pd.merge(output_df, df, on=["DAUID", "Residential_TotalGross_Average"], how="outer")

# Fill missing counts with 0 and sort
count_cols = [col for col in output_df.columns if col.endswith("_count")]
output_df[count_cols] = output_df[count_cols].fillna(0).astype(int)
output_df = output_df.sort_values("DAUID")

cols = [col for col in output_df.columns if col != "Residential_TotalGross_Average"] + ["Residential_TotalGross_Average"]
output_df = output_df[cols]

# Save to CSV
output_df.to_csv("DA_summary_counts.csv", index=False)
print("Saved to DA_summary_counts.csv")
