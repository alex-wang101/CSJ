import csv
from collections import defaultdict
import glob
import os

input_files = glob.glob('distances_*.csv')

for input_file in input_files:
    suffix = os.path.basename(input_file)[len('distances_'):]
    output_file = f'avg_dist_{suffix}'

    # Structure to hold grouped data
    grouped = defaultdict(list)

    # Read input CSV
    with open(input_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dauid = row['DAUID']
            target_name = row['Target_name']
            key = (dauid, target_name)
            grouped[key].append({
                'DA_address': row['DA_address'],
                'Target_address': row['Target_address'],
                'Distance': float(row['Distance (km)'])
            })

    # Process and write output
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['DAUID', 'Target_name', 'Target_address', 'Distance (km)'])

        for (dauid, target_name), entries in grouped.items():
            distances = [entry['Distance'] for entry in entries]
            avg_distance = sum(distances) / len(distances)

            # Use the Target_address from the first entry (should be the same for all)
            target_address = entries[0]['Target_address']
            writer.writerow([dauid, target_name, target_address, round(avg_distance, 2)])

# # Structure to hold grouped data
# grouped = defaultdict(list)

# # Read input CSV
# with open(input_file, 'r', newline='', encoding='utf-8') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         dauid = row['DAUID']
#         target_name = row['Target_name']
#         key = (dauid, target_name)
#         grouped[key].append({
#             'DA_address': row['DA_address'],
#             'Target_address': row['Target_address'],
#             'Distance': float(row['Distance (km)'])
#         })

# # Process and write output
# with open(output_file, 'w', newline='', encoding='utf-8') as f:
#     writer = csv.writer(f)
#     writer.writerow(['DAUID', 'Target_name', 'Target_address', 'Distance (km)'])

#     for (dauid, target_name), entries in grouped.items():
#         distances = [entry['Distance'] for entry in entries]
#         avg_distance = sum(distances) / len(distances)

#         # Use the Target_address from the first entry (should be the same for all)
#         target_address = entries[0]['Target_address']
#         writer.writerow([dauid, target_name, target_address, round(avg_distance, 2)])
