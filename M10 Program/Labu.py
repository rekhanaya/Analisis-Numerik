print("\033c")  # To clear the screen
import numpy as np
from matplotlib import pyplot as plt

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print ("(1) ACQUIRING USER ENTRIES: FILE NAME OF THE PICTURE, SIZE OF THE LENSE,")
print ("    VAR_TH, AND HOW THE PICTURE IS SPLIT INTO SUB_IMAGES...")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
dir = ""
nama_file_input = "Labbu"
sld = 0.05   # 0.02 means that scanning lense diameter is 2% of image height (row).
var_th_normal = 0.1 # Any scanning region that has 0.2 of max_var will be detected.
sub_image_structure = [1, 1] # [8,8] means that the image is split into 8x8 sub-images.
warna_kontur = 0
print("")

# Constants for color to grayscale conversion
r = 0.3333; g = 0.3333; b = 1 - r - g

def menghitung_dan_menampung_var(ori_gs, TM, BM, LM, RM, hld):
    tabel_var = []
    for y in range(TM, BM, hld):
        for x in range(LM, RM, hld):
            lense = ori_gs[y-hld:y+hld+1, x-hld:x+hld+1]
            if lense.size > 1:  
                with np.errstate(divide='ignore', invalid='ignore'):  # Temporarily suppress warnings
                    var = np.var(lense)
                    if not np.isnan(var):  # Check for NaN values
                        tabel_var.append(var)
                    else:
                        tabel_var.append(0)  # Replace NaN with 0 or any preferred default
            else:
                tabel_var.append(0)  # Handle cases with too few elements
    return tabel_var

def buat_daftar_batas_sub_images(sub_image_structure, TM, BM, LM, RM):
    nos = sub_image_structure[0] * sub_image_structure[1]
    row_sub, col_sub = sub_image_structure[0], sub_image_structure[1]
    batas_sub_images = np.zeros((row_sub, col_sub, 4), dtype=int)
    delta_y = round((BM - TM) / row_sub)
    delta_x = round((RM - LM) / col_sub)
    for i in range(row_sub):
        for j in range(col_sub):
            batas_sub_images[i, j] = [TM + i * delta_y - hld, TM + (i + 1) * delta_y - hld, LM + j * delta_x - hld, LM + (j + 1) * delta_x - hld]
    batas_sub_images = batas_sub_images.reshape(nos, 4)
    batas_sub_images = np.append(batas_sub_images, [[0, 0, 0, 0]], axis=0)
    return batas_sub_images

def cari_koordinat_edge(ori_gs, batas_sub_images, hld, var_th):
    m, n = np.shape(batas_sub_images)
    koordinat_obj = np.zeros((m, 2), dtype=int)
    for i in range(m):
        y1, y2, x1, x2 = batas_sub_images[i]
        for y in range(y1, y2, hld):
            for x in range(x1, x2, hld):
                lense = ori_gs[y-hld:y+hld+1, x-hld:x+hld+1]
                if np.var(lense) > var_th:
                    koordinat_obj[i] = [y, x]
                    break
            else:
                continue
            break
        if not any(koordinat_obj[i]):
            koordinat_obj[i] = [1, 1]
    return koordinat_obj

def next_max_var(ori_gs, curr_dir, y, x):
    next_dir = ""
    y_temp, x_temp = 0, 0
    max_var = 0

    directions = {'east': (0, hld), 'west': (0, -hld), 'south': (hld, 0), 'north': (-hld, 0)}
    for direction, (dy, dx) in directions.items():
        if direction == {'east': 'west', 'west': 'east', 'south': 'north', 'north': 'south'}.get(curr_dir):
            continue
        ny, nx = y + dy, x + dx
        lense = ori_gs[ny-hld:ny+hld+1, nx-hld:nx+hld+1]
        if lense.size > 1:  
            with np.errstate(divide='ignore', invalid='ignore'):
                var = np.var(lense)
                if not np.isnan(var):  
                    if var > max_var:
                        max_var = var
                        next_dir = direction
                        y_temp, x_temp = ny, nx
        else:
            max_var = 0

    return next_dir, y_temp, x_temp


def lukis_kontur(ori_gs, buffer, y, x):
    y_start, x_start = y, x
    curr_dir = ""
    distance = row
    batas = round(1.5 * (row + row + col + col) / hld)
    for j in range(batas):
        next_dir, y_next, x_next = next_max_var(ori_gs, curr_dir, y, x)
        buffer[y-hld:y+hld+1, x-hld:x+hld+1] = warna_kontur
        curr_dir, y, x = next_dir, y_next, x_next
        distance = round(((y_next - y_start)**2 + (x_next - x_start)**2)**0.5)
        if j > 10 and distance < round(0.8 * sld):
            break
    return buffer

print("(2) MAIN PROGRAM ...")
print("    CONTOUR DETECTION USING MAXIMUM VARIANCE IS TAKING PLACE...")
print("    During operation, measurement is done to the ori_gs, without changing any of its pixels.")
print("    Marking is done only to the buffer.")
print("    At last, cropping is done to the original color picture (pic).")
print("")

print("(i)  PREPARATION: CREATING NEW VARIABLES BASED ON USER ENTRIES ...")
pic = plt.imread(dir + nama_file_input + ".jpg")
row, col, depth = np.shape(pic)
print("     col, row, depth =", row, ",", col, ",", depth, ".\n")
ori_gs = np.uint8(r * pic[:, :, 0] + g * pic[:, :, 1] + b * pic[:, :, 2])
buffer = np.copy(ori_gs)

sld = round(sld * row)
hld = round(0.5 * sld)

TM = round(1.5 * sld)
BM = round(row - 0.5 * sld)
LM = round(1.5 * sld)
RM = round(col - 0.5 * sld)

nos = sub_image_structure[0] * sub_image_structure[1]

print("(ii) STATISTICS: FINDING max_var AND var_th OF THE WHOLE PICTURE...")
print("     The max(var) is used to define var_th.")
print("     Then var_th will be the threshold when detecting an object's contour.")
tabel_var = menghitung_dan_menampung_var(ori_gs, TM, BM, LM, RM, hld)
print("      var_th_normal =", var_th_normal)
var_th = round(var_th_normal * max(tabel_var))
print("      min(var), max(var), var_th =", round(min(tabel_var)), ",", round(max(tabel_var)), ",", var_th, ".\n")

print("(iii) CREATING THE TABLE OF batas-batas sub-images BERDASARKAN sub_image_structure. \n")
batas_sub_images = buat_daftar_batas_sub_images(sub_image_structure, TM, BM, LM, RM)

print("(iv) FIRST SCANNING: FINDING AN EDGE (GRIP) OF AN OBJECT WITHIN EVERY")
print("     SUB_IMAGE BASED ON batas_sub_images AND var_th...")
print("     The coordinates of the edges found (y, x) are stored in koordinat_obj.")
print("     var_th =", var_th)
print("")
koordinat_obj = cari_koordinat_edge(ori_gs, batas_sub_images, hld, var_th)
print("np.shape(batas_sub_images) =", np.shape(batas_sub_images))
print("np.shape(koordinat_obj) =", np.shape(koordinat_obj))
print("batas_sub_images =", batas_sub_images)
print("koordinat_obj =", koordinat_obj)

print("(v)  SECOND SCANNING. USING koordinat_obj AND MAX VAR METHOD, ")
print("     FIND OBJECT_S CONTOUR. OBJECT_S CONTOUR IS DRAWN FOR EVERY i.\n")
print("koordinat_obj =", koordinat_obj)

i = 0
# ... previous code ...
num_valid_sub_images = np.sum(koordinat_obj[:, 0] > 0)

for i in range(num_valid_sub_images):  # Loop only up to the number of valid sub-images
    print("i, koordinat_obj[i,0], koordinat_obj[i,1] =", i, ",", koordinat_obj[i, 0], ",", koordinat_obj[i, 1])
    y, x = koordinat_obj[i]
    buffer = lukis_kontur(ori_gs, buffer, y, x)


print("buffer =", buffer)
plt.imsave(dir + nama_file_input + "_hasil.jpg", buffer, cmap='gray')
plt.imshow(buffer, cmap='gray')
plt.show()

print("\n\n(3) Acquiring the exact contour of the object...\n")
import cv2

# Convert buffer to binary image
_, binary_buffer = cv2.threshold(buffer, 128, 255, cv2.THRESH_BINARY)

# Find contours using OpenCV
contours, _ = cv2.findContours(binary_buffer, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on the original image
contour_image = np.copy(pic)
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 3)

# Save and display the contour image
contour_image_path = dir + nama_file_input + "_contour.jpg"
plt.imsave(contour_image_path, contour_image)
plt.imshow(contour_image)
plt.show()

# Calculate the area of the contours
area = sum(cv2.contourArea(contour) for contour in contours)
scale_factor = 1.1 * 1.6 / (row * col)  # Scaling factor to convert pixel area to square meters
area_in_meters = area * scale_factor

print(f"The cross-sectional area of the pumpkin is approximately {area_in_meters:.2f} square meters.")

print("\n\n(4) Calculating the area of the black region inside the pumpkin...\n")

