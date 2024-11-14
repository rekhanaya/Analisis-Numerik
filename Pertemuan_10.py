import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2

# Load image
denah = mpimg.imread("C:\\Users\\rekha\\OneDrive - Universitas Pembangunan Jaya\\COOLYEAH\\SEMESTER 4\\Analisis Numerik\\Pertemuan 10\\tanah.jpg")

# Define green color range (RGB)
lower_green = np.array([0, 100, 0])  # lower bound of green
upper_green = np.array([100, 255, 100])  # upper bound of green

# Mask green color in the image
mask = cv2.inRange(denah, lower_green, upper_green)

# Count green pixels
green_pixels = np.sum(mask == 255)

# Calculate total pixels
total_pixel = denah.shape[0] * denah.shape[1]

# Calculate green area percentage
green_area_percentage = (green_pixels / total_pixel) * 100

# Print the results
print("Total pixel area of the image:", total_pixel)
print("Total green pixel area of the image:", green_pixels)
print("Percentage of green area:", green_area_percentage, "%")

# Display the masked image
plt.imshow(mask, cmap='gray')
plt.title('Green Areas')
plt.show()