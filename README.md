# Victoria Geocoding and Distance Analysis Pipeline

This project processes address data for various amenities in Victoria, BC, geocodes them using OpenStreetMap's Nominatim service, and calculates distances from Dissemination Areas (DAs) to these amenities.

## Project Structure

```
CSJ/
├── main.py                 # Main execution script
├── csvs/                   # CSV data files
│   ├── Address.csv         # Source address data
│   ├── DA_geocoded.csv     # Geocoded Dissemination Areas
│   ├── AM_address_*.csv    # Address files for each amenity type
│   ├── AM_geocoded_*.csv   # Geocoded amenity files
│   └── distances_*.csv     # Distance calculation results
└── scripts/                # Processing scripts
    ├── AM_geocode_*.py     # Geocoding scripts for each amenity type
    ├── distance_*.py       # Distance calculation scripts
    ├── DA_geocode.py       # DA geocoding script
    └── Coordinate.py       # Coordinate utilities
```

## Features

- **Multi-threaded Geocoding**: Processes multiple amenity types simultaneously
- **Four Amenity Categories**:
  - 🏥 Hospitals and medical facilities
  - 🛒 Shopping centers and commercial areas
  - 🏫 Schools and educational institutions
  - 🌊 Waterfront and recreational areas
- **Distance Analysis**: Calculates distances from DAs to amenities using the Haversine formula
- **Smart Filtering**: Prioritizes amenities within 0.5km, falls back to closest if none found
- **Rate Limiting**: Respects OpenStreetMap API limits with 1-second delays

## Requirements

- Python 3.x
- Required packages:
  - `requests` - for API calls to Nominatim
  - `csv` - for CSV file processing (built-in)
  - `math` - for distance calculations (built-in)
  - `threading` - for concurrent processing (built-in)

## Installation

1. Clone or download this repository
2. Install required packages:
   ```bash
   pip install requests
   ```

## Usage

### Quick Start
Run the complete pipeline:
```bash
python3 main.py
```

This will:
1. **Geocode all amenities** (hospitals, shopping, schools, waterfront) in parallel
2. **Calculate distances** from each DA to all amenities
3. **Generate filtered results** with closest amenities for each DA

### Individual Scripts
You can also run individual components:

```bash
# Geocode specific amenity types
python3 scripts/AM_geocode_hospital.py
python3 scripts/AM_geocode_shopping.py
python3 scripts/AM_geocode_schools.py
python3 scripts/AM_geocode_waterfront.py

# Calculate distances for specific amenity types
python3 scripts/distance_hospital.py
python3 scripts/distance_shopping.py
python3 scripts/distance_school.py
python3 scripts/distance_waterfront.py
```

## Input Files

### Required CSV Files in `csvs/` directory:
- `DA_geocoded.csv` - Dissemination Areas with coordinates
- `AM_address_hospitals.csv` - Hospital addresses
- `AM_address_shopping.csv` - Shopping center addresses  
- `AM_address_schools.csv` - School addresses
- `AM_address_waterfront.csv` - Waterfront location addresses

### CSV Format:
All address files should have columns: `name`, `address`

## Output Files

The pipeline generates several output files in the `csvs/` directory:

### Geocoded Files:
- `AM_geocoded_hospitals.csv`
- `AM_geocoded_shopping.csv`
- `AM_geocoded_schools.csv`
- `AM_geocoded_waterfront.csv`

### Distance Files:
- `distances_hospitals.csv`
- `distances_shopping.csv`
- `distances_school.csv`
- `distances_waterfront.csv`

Each distance file contains:
- `DAUID` - Dissemination Area identifier
- `DA_address` - DA address
- `Target_name` - Amenity name
- `Target_address` - Amenity address
- `Distance (km)` - Distance in kilometers

## Algorithm Details

### Geocoding Process
1. Uses OpenStreetMap's Nominatim API for address geocoding
2. Implements 1-second delay between requests to respect rate limits
3. Handles failed geocoding attempts gracefully with error logging

### Distance Calculation
1. **Haversine Formula**: Calculates great-circle distances between coordinates
2. **Smart Filtering**: For each DA, finds all amenities within 0.5km
3. **Fallback Strategy**: If no amenities within 0.5km, returns the closest one
4. **Sorting**: Results sorted by DA and distance for easy analysis

### Performance Features
- **Multi-threading**: Geocoding runs in parallel for faster processing
- **Error Handling**: Invalid coordinates are logged and skipped
- **Memory Efficient**: Processes data in chunks to handle large datasets

## Troubleshooting

### Common Issues:

1. **File Not Found Errors**: Ensure all required CSV files are in the `csvs/` directory
2. **Geocoding Failures**: Some addresses may fail to geocode - these are logged as warnings
3. **Rate Limiting**: If you encounter rate limit errors, the built-in delays should handle this
4. **Invalid Coordinates**: Entries with missing/invalid coordinates are skipped with warnings

### Error Messages:
- `⚠️ Invalid coordinates in DA row` - DA has missing latitude/longitude
- `⚠️ Invalid coordinates in target row` - Amenity has missing coordinates
- `Geocoding failed for: [address]` - Address couldn't be geocoded

## Contributing

When adding new amenity types:
1. Create address CSV file in `csvs/AM_address_[type].csv`
2. Create geocoding script in `scripts/AM_geocode_[type].py`
3. Create distance script in `scripts/distance_[type].py`
4. Add processing functions to `main.py`

## License

This project processes public address data for research and analysis purposes.

## Contact

For questions or issues, please refer to the project documentation or create an issue in the repository.
