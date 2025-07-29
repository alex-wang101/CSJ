import csv
import requests
import math
import time

# --- Geocoding (free Nominatim service) ---
def geocode_address(address):
    """Geocode address using Nominatim (OpenStreetMap)."""
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'YourAppName (your@email.com)'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    if data:
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        print(f"❌ Could not geocode: {address}")
        return None, None

# --- Haversine distance formula ---
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# --- Main Program ---
def main():
    input_address = input("Enter the reference address: ").strip()
    lat1, lon1 = geocode_address(input_address)
    time.sleep(1)  # Be polite to Nominatim

    if lat1 is None or lon1 is None:
        print("❌ Geocoding failed. Exiting.")
        return

    # Load pre-geocoded addresses
    input_file = 'geocoded_addresses.csv'
    output_file = 'distances.csv'
    results = []

    with open(input_file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            name = row['name']
            address2 = row['address']
            try:
                lat2 = float(row['latitude'])
                lon2 = float(row['longitude'])
                distance = haversine_distance(lat1, lon1, lat2, lon2)
                results.append([name,input_address, address2, round(distance, 2)])
            except ValueError:
                print(f"⚠️ Skipping row with invalid coordinates: {row}")

    # sort results by distance
    results.sort(key=lambda x: x[3])

    # Save results
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['name', 'From Address', 'To Address', 'Distance (km)'])
        writer.writerows(results)

    print(f"✅ Distances saved to '{output_file}'")

if __name__ == '__main__':
    main()
