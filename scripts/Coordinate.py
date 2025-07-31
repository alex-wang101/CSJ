import csv
import requests
import time

def geocode_address(address):
    """Use Nominatim (OpenStreetMap) to get coordinates."""
    url = 'https://nominatim.openstreetmap.org/search'
    params = {'q': address, 'format': 'json', 'limit': 1}
    headers = {'User-Agent': 'MyGeocoderApp (your@email.com)'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    
    if data:
        return float(data[0]['lat']), float(data[0]['lon'])
    else:
        print(f"Geocoding failed for: {address}")
        return None, None

def main():
    input_csv = 'Address.csv'
    output_csv = 'geocoded_addresses.csv'
    results = []

    with open(input_csv, newline='', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            name = row['name']
            address = row['address']
            lat, lon = geocode_address(address)
            time.sleep(1)  # Respect Nominatim rate limit
            results.append({'name': name,'address': address, 'latitude': lat, 'longitude': lon})

    with open(output_csv, 'w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['name','address', 'latitude', 'longitude']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Saved geocoded data to {output_csv}")

if __name__ == '__main__':
    main()
