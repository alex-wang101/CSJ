import subprocess

def main():
    print("🚀 Running geocode.py...")
    subprocess.run(["python", "Coordinate.py"], check=True)

    print("\n📏 Running distance.py...")
    subprocess.run(["python", "Distance.py"], check=True)

    print("\n✅ All done!")

if __name__ == "__main__":
    main()
