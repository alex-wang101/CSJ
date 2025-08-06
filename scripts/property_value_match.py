import csv
import glob
import os

# File paths
assessment_file = 'Assessment_Values_by_Census_Dissemination_Area_and_Property_Type (1).csv'

input_files = glob.glob('avg_dist_*.csv')
output_files = ['merged_output_' + f[len('avg_dist_'):] for f in input_files]

for targets_file, output_file in zip(input_files, output_files):
    # Step 1: Load Assessment Values by DAUID
    assessment_data = {}
    with open(assessment_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dauid = row['DAUID']
            res_avg = row['Residential_TotalGross_Average']
            assessment_data[dauid] = res_avg

    # Step 2: Load targets_file and merge Residential_TotalGross_Average
    with open(targets_file, 'r', newline='', encoding='utf-8') as f_in, \
         open(output_file, 'w', newline='', encoding='utf-8') as f_out:

        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames + ['Residential_TotalGross_Average']
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            dauid = row['DAUID']
            row['Residential_TotalGross_Average'] = assessment_data.get(dauid, '')  # blank if not found
            writer.writerow(row)

# # Step 1: Load Assessment Values by DAUID
# assessment_data = {}
# with open(assessment_file, 'r', newline='', encoding='utf-8') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         dauid = row['DAUID']
#         res_avg = row['Residential_TotalGross_Average']
#         assessment_data[dauid] = res_avg

# # Step 2: Load output.csv and merge Residential_TotalGross_Average
# with open(targets_file, 'r', newline='', encoding='utf-8') as f_in, \
#      open(output_file, 'w', newline='', encoding='utf-8') as f_out:

#     reader = csv.DictReader(f_in)
#     fieldnames = reader.fieldnames + ['Residential_TotalGross_Average']
#     writer = csv.DictWriter(f_out, fieldnames=fieldnames)
#     writer.writeheader()

#     for row in reader:
#         dauid = row['DAUID']
#         row['Residential_TotalGross_Average'] = assessment_data.get(dauid, '')  # blank if not found
#         writer.writerow(row)
