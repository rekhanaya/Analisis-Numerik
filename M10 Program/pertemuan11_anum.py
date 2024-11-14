import cv2
import numpy as np
import matplotlib.pyplot as plt

# Read the original image
original_img = cv2.imread("C:\\Users\\Razan Aubin\\OneDrive\\Pictures\\Gambar buat app\\d952675c-cef4-4fd3-b793-a5a5bd1a5715.png", cv2.IMREAD_GRAYSCALE)

# Read the image
img = original_img.copy()

# Invert the image (make black pixels white and vice versa)
inverted_img = cv2.bitwise_not(img)

# Find contours in the inverted image
contours, hierarchy = cv2.findContours(inverted_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Assuming there's only one large contour for the pumpkin, fill it with black
cv2.drawContours(img, contours, -1, (0, 0, 0), -1)  # -1 to fill all contours

# Create subplots
plt.figure(figsize=(10, 5))

# Plot original image
plt.subplot(1, 2, 1)
plt.imshow(original_img, cmap='gray')
plt.axis('off')
plt.title('Original Image')

# Plot modified image
plt.subplot(1, 2, 2)
plt.imshow(img, cmap='gray')
plt.axis('off')
plt.title('Blackened')

plt.tight_layout()
plt.show()

