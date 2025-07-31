import subprocess
import threading



def process_hospital():
    print("🚀 Processing hospital geocoding...")
    subprocess.run(["python3", "scripts/AM_geocode_hospital.py"], check=True)

def process_shopping():
    print("🚀 Processing shopping geocoding...")
    subprocess.run(["python3", "scripts/AM_geocode_shopping.py"], check=True)

def process_school():
    print("🚀 Processing school geocoding...")
    subprocess.run(["python3", "scripts/AM_geocode_schools.py"], check=True)

def process_waterfront():
    print("🚀 Processing waterfront geocoding...")
    subprocess.run(["python3", "scripts/AM_geocode_waterfront.py"], check=True)

def threading_function():
    thread1 = threading.Thread(target=process_hospital)
    thread1.start()
    thread2 = threading.Thread(target=process_shopping)
    thread2.start()
    thread3 = threading.Thread(target=process_school)
    thread3.start()
    thread4 = threading.Thread(target=process_waterfront)
    thread4.start()
    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

def main():
    print("starting threading")
    threading_function()
    print("🔄 Starting geocoding processes for shopping...")
    subprocess.run(["python3", "scripts/distance_shopping.py"], check=True)
    print("🔄 Starting geocoding processes for hospital...")
    subprocess.run(["python3", "scripts/distance_hospital.py"], check=True)
    print("🔄 Starting geocoding processes for school...")
    subprocess.run(["python3", "scripts/distance_school.py"], check=True)
    print("🔄 Starting geocoding processes for waterfront...")
    subprocess.run(["python3", "scripts/distance_waterfront.py"], check=True)
    print("✅ All geocoding processes completed successfully!")

    print("\n✅ All done!")

if __name__ == "__main__":
    main()
