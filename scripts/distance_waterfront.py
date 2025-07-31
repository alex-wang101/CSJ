import csv
import math
from collections import defaultdict

# --- Haversine formula ---
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def main():
    da_file = 'csvs/DA_geocoded.csv'
    target_file = 'csvs/AM_geocoded_waterfront.csv'
    output_file = 'csvs/distances_waterfront.csv'

    # Load destination addresses
    with open(target_file, newline='', encoding='utf-8') as f:
        targets = list(csv.DictReader(f))

    results = []

    # Load source DA addresses and calculate distances
    with open(da_file, newline='', encoding='utf-8') as f:
        da_reader = csv.DictReader(f)
        for da_row in da_reader:
            da_uid = da_row['DAUID']
            da_address = da_row['address']
            try:
                da_lat = float(da_row['latitude'])
                da_lon = float(da_row['longitude'])
            except ValueError:
                print(f"⚠️ Invalid coordinates in DA row: {da_row}")
                continue

            for target in targets:
                target_name = target.get('name', '')
                target_address = target['address']
                try:
                    target_lat = float(target['latitude'])
                    target_lon = float(target['longitude'])
                except ValueError:
                    print(f"⚠️ Invalid coordinates in target row: {target}")
                    continue

                distance = haversine_distance(da_lat, da_lon, target_lat, target_lon)
                results.append([
                    da_uid,
                    da_address,
                    target_name,
                    target_address,
                    round(distance, 2)
                ])

    # Sort results by distance (ascending)
    results.sort(key=lambda x: (x[0], x[1], x[4]))

    # Group results by (DAUID, DA_address)
    grouped = defaultdict(list)
    for row in results:
        key = (row[0], row[1])  # DAUID, DA_address
        grouped[key].append(row)

    # Filter each group by distance
    final_rows = []
    for key, rows in grouped.items():
        # Sort this group by distance
        rows.sort(key=lambda x: x[4])

        # Find all under 0.5 km
        close_matches = [r for r in rows if r[4] <= 0.5]

        if close_matches:
            final_rows.extend(close_matches)
        else:
            final_rows.append(rows[0])  # closest only if no match ≤ 0.5

    # Optional: sort final output
    final_rows.sort(key=lambda x: (x[0], x[1], x[4]))

    # Write filtered output
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['DAUID', 'DA_address', 'Target_name', 'Target_address', 'Distance (km)'])
        writer.writerows(final_rows)

    print(f"✅ Filtered distances written to '{output_file}'")

if __name__ == '__main__':
    main()
