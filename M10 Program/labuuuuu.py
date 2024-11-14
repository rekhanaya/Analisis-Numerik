import numpy as np
import cv2
from matplotlib import pyplot as plt

# Constants
background_width = 1.6  # meters
background_height = 1.1  # meters
image_width = 1600  # pixels
image_height = 1100  # pixels

# Load the image
image_path = "labuuu.jpg"
pic = cv2.imread(image_path)

# Convert to grayscale
gray_image = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)

# Threshold the grayscale image to binary
_, binary_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)

# Find contours
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a mask for the pumpkin and fill the interior with black
mask = np.zeros_like(pic)
cv2.drawContours(mask, contours, -1, (255, 255, 255), -1)  # Fill the contour area with white

# Invert the mask
mask_inv = cv2.bitwise_not(mask)

# Set the interior of the pumpkin to black in the original image
result_image = cv2.bitwise_and(pic, mask_inv)

# Draw the black contour on the result image
cv2.drawContours(result_image, contours, -1, (0, 0, 0), 3)

# Enhance the detection of the stem using morphological operations
kernel = np.ones((5, 5), np.uint8)
gray_result = cv2.cvtColor(result_image, cv2.COLOR_BGR2GRAY)
_, binary_result = cv2.threshold(gray_result, 50, 255, cv2.THRESH_BINARY_INV)
binary_result = cv2.morphologyEx(binary_result, cv2.MORPH_CLOSE, kernel)

# Find contours again to include the stem
contours_with_stem, _ = cv2.findContours(binary_result, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Fill the interior with black again to include the stem
cv2.drawContours(result_image, contours_with_stem, -1, (0, 0, 0), -1)

# Save and display the result image
result_image_path = "labu_black_inside_with_stem.jpg"
cv2.imwrite(result_image_path, result_image)

# Convert BGR to RGB for displaying with matplotlib
result_image_rgb = cv2.cvtColor(result_image, cv2.COLOR_BGR2RGB)

# Display the image
plt.imshow(result_image_rgb)
plt.show()

# Calculate the area of the largest contour
areas = [cv2.contourArea(contour) for contour in contours_with_stem]
max_area = max(areas) if areas else 0

# Convert the area from pixels to square meters
scale_factor = (background_width * background_height) / (image_width * image_height)  # meters per pixel
area_in_meters = max_area * scale_factor

print(f"The cross-sectional area of the pumpkin is approximately {area_in_meters:.2f} square meters.")
