########################################################
"""
    This file is part of the MOPS-Hub project.
    Author: Ahmed Qamesh (University of Wuppertal)
    email: ahmed.qamesh@cern.ch  
    Date: 01.05.2023
"""
########################################################
from PIL import Image

# Load the image
img_path = '/home/dcs/Pictures/Screenshot from 2024-02-21 11-27-56.png'
img = Image.open(img_path)

# Convert the image to RGBA (if not already in this mode)
img = img.convert("RGBA")

# Get data of the image
data = img.getdata()

# Use threshold to find the background (assumed to be the most common color in the image)
def find_background_color(image_data):
    # Count the number of times each color appears in the image
    color_counts = {}
    for color in image_data:
        if color in color_counts:
            color_counts[color] += 1
        else:
            color_counts[color] = 1
            
    # Find the most frequent color
    max_count = max(color_counts.values())
    background_color = [color for color, count in color_counts.items() if count == max_count][0]
    return background_color

background_color = find_background_color(data)

# Set a new data list
new_data = []
# Go through each item in image data
for item in data:
    # Change all pixels that match the background color to be transparent
    if item[0] == background_color[0] and item[1] == background_color[1] and item[2] == background_color[2]:
        new_data.append((255, 255, 255, 0))  # Make the pixel fully transparent
    else:
        new_data.append(item)  # Keep the pixel as is

# Update image data with the new data list
img.putdata(new_data)

# Save the new image without background
optimized_img_path = '/home/dcs/Pictures/optimized_image.png'
img.save(optimized_img_path)

optimized_img_path
