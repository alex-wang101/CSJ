import subprocess

def main():
    print("🚀 Running AM_geocode.py...")
    subprocess.run(["python", "AM_geocode.py"], check=True)

    print("\n🚀 Running DA_geocode.py...")
    subprocess.run(["python", "DA_geocode.py"], check=True)

    print("\n📏 Running distance.py...")
    subprocess.run(["python", "distance.py"], check=True)

    print("\n✅ All done!")

if __name__ == "__main__":
    main()
