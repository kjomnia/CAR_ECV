from PIL import Image
import os

input_path = "car_source.png"
output_path = "src/car_view.png"

try:
    img = Image.open(input_path)
    w, h = img.size
    
    # Crop top-left car (first quadrant of 2x2 grid)
    # The image is 1500x844 or something similar.
    # Let's crop exactly the top-left quadrant.
    left = 0
    top = 0
    right = w // 2
    bottom = h // 2
    
    car = img.crop((left, top, right, bottom))
    
    # Rotate 90 degrees clockwise to make it vertical
    car = car.rotate(-90, expand=True)
    
    # Save as PNG
    car.save(output_path)
    print(f"Successfully saved processed image to {output_path}")
    print(f"Original size: {w}x{h}, Cropped size: {car.size}")
except Exception as e:
    print(f"Error processing image: {e}")
