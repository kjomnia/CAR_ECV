import os
import shutil
from PIL import Image

# Use the full path with raw string
brain_dir = r"C:\Users\강요한\.gemini\antigravity\brain\81d82c38-c891-4a07-a1cd-1532b89bcebb"
target_filename = "media__1771055847113.png"
target_file = os.path.join(brain_dir, target_filename)

print(f"Checking: {target_file}")

if os.path.exists(target_file):
    size = os.path.getsize(target_file)
    print(f"File exists, size: {size} bytes")
    if size > 0:
        try:
            img = Image.open(target_file)
            print(f"Image opened: {img.size}")
            w, h = img.size
            # The uploaded image is horizontal. 
            # Top-left quadrant has the car the user wants.
            # Let's crop it.
            # Adding a bit of margin to avoid watermarks at the edges if possible
            left = 10
            top = 10
            right = w // 2 - 10
            bottom = h // 2 - 10
            
            car = img.crop((left, top, right, bottom))
            
            # Rotate 90 deg clockwise to make it vertical
            # car in image faces LEFT. Rotating 90 deg CW makes it face UP.
            car = car.rotate(-90, expand=True)
            
            os.makedirs("src", exist_ok=True)
            car.save("src/car_view.png")
            print(f"SUCCESS: Saved to src/car_view.png ({car.size})")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("Error: File is empty.")
else:
    # Try searching just in case
    print("Exact file not found, searching...")
    for f in os.listdir(brain_dir):
        if f.startswith("media__1771055847113"):
            print(f"Found match: {f}")
            # ... repeat logic or just fix the path
    print(f"Failed to find: {target_filename}")
