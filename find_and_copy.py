import os
import shutil

# Root path for brain - using raw string and ensuring it's treated as unicode
base_path = r"C:\Users\강요한\.gemini\antigravity\brain"
filename = "media__1771055847113.png"

print(f"Searching for {filename} in {base_path}...")

src_path = None
try:
    for root, dirs, files in os.walk(base_path):
        if filename in files:
            src_path = os.path.join(root, filename)
            break

    if src_path:
        size = os.path.getsize(src_path)
        print(f"Found at: {src_path}")
        print(f"Size: {size} bytes")
        if size > 0:
            shutil.copy(src_path, "car_source.png")
            print("Successfully copied to car_source.png")
        else:
            print("Error: Source file is 0 bytes.")
    else:
        print("Error: File not found in the search path.")
except Exception as e:
    print(f"Error during search/copy: {e}")
