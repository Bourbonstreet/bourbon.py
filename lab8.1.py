import cv2
import numpy as np
import os

image_path = r"C:\Users\CHRISTOPHER'M\PycharmProjects\pythonProject\new image\variant-1.jpg"

if not os.path.exists(image_path):
    print(f"Error: Image file not found at {image_path}")
    exit(1)

image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

if image is None:
    print(f"Error: Unable to load image from {image_path}")
    exit(1)

print(f"Image type: {type(image)}")
print(f"Image shape: {image.shape}")

height, width = image.shape

halftone = np.zeros_like(image)

dot_size = 4

for y in range(0, height, dot_size):
    for x in range(0, width, dot_size):
        block = image[y:y+dot_size, x:x+dot_size]
        average_intensity = np.mean(block)

        radius = int((255 - average_intensity) / 255 * (dot_size // 2))

        if radius > 0:
            cv2.circle(halftone, (x + dot_size // 2, y + dot_size // 2), radius, 255, -1)

output_path = r"C:\Users\CHRISTOPHER'M\Desktop\halftone.jpg"
cv2.imwrite(output_path, halftone)
print(f"Halftone image saved to {output_path}")