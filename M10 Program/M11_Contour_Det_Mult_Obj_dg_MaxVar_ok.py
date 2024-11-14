#Do not remove this copyright information.
#2024. This program is developed by Mohammad Nasucha, Ph.D.
#Department of Informatics, Universitas Pembangunan Jaya

print("\033c")       #To close all
import numpy as np
from matplotlib import pyplot as plt

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print ("(1) ACQUIRING USER ENTRIES: FILE NAME OF THE PICTURE, SIZE OF THE LENSE,")
print ("    VAR_TH, AND HOW THE PICTURE IS SPLIT INTO SUB_IMAGES...")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
dir = "C://Users//INF-9-AllinOne//OneDrive - Universitas Pembangunan Jaya//Coding_Python//MK_VisKomp//Gambar_in_out//"
dir = ""
nama_file_input = "labu"
sld = 0.05   #0.02 means that scanning lense diameter is 2% of image height (row).
var_th_normal = 0.1 #Any scanning region that has 0.2 of max_var will be detected.
sub_image_structure = [1,1] #[8,8] means that the image is split into 8x8 sub-images.
warna_kontur = 0
print("")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++   CONSTANTS FOR COLOR TO GRAYSCALE CONVERSION    ++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
r = 0.3333; g = 0.3333; b = 1 - r - g

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++   FUNCTION UNTUK STATISTIK: MENCARI VARIANCE                            ++
#++   DENGAN SCANNING LENSE KE SELURUH AREA GAMBAR.                         ++
#++   Lensa dibuat secara lokal di dalam function berdasarkan nilai hld.    ++
#++   Input: ori_gs, TM, BM, LM, RM, dan hld.                               ++
#++   Output: tabel_var.                                                    ++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def menghitung_dan_menampung_var(ori_gs, TM, BM, LM, RM, hld):
    tabel_var = 0
    for y in range (TM, BM, hld):         #The scanning lense jumps rightward a much as hld.
        for x in range (LM, RM, hld):     #and jumps downward as much as hld, too.
            temp = tabel_var
            lense = ori_gs[y-hld:y+hld+1, x-hld:x+hld+1] #Reading the targeted region with the lense.
            tabel_var = np.var(lense)
            #print(y, x, tabel_var)
            tabel_var = np.append(temp, tabel_var)
            #print(np.shape(tabel_var))
    return tabel_var

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++   FUNCTION UNTUK MENENTUKAN BATAS-BATAS SUB-IMAGES                      ++
#++   Input: sub_image_structure, TM, BM, LM, dan RM.                    ++
#++   Output function ini adalah batas_sub_image
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def buat_daftar_batas_sub_images(sub_image_structure, TM, BM, LM, RM):
    nos = sub_image_structure[0] * sub_image_structure[1]
    row_sub, col_sub = sub_image_structure[0], sub_image_structure[1]
    # The following 4 elements are needed for y1, y2, x1 and x2 of ecah sub-image.
    batas_sub_images = np.arange(4 * nos).reshape(row_sub, col_sub, 4)
    batas_sub_images[:, :, :] = 0
    delta_y = round((BM - TM) / row_sub)
    delta_x = round((RM - LM) / col_sub)
    for i in range(0, row_sub):
        for j in range(0, col_sub):
            batas_sub_images[i, j, 0] = TM + i * delta_y - hld
            batas_sub_images[i, j, 1] = TM + (i + 1) * delta_y - hld
            batas_sub_images[i, j, 2] = LM + j * delta_x - hld
            batas_sub_images[i, j, 3] = LM + (j + 1) * delta_x - hld

    batas_sub_images = batas_sub_images.reshape(nos, 4)  # Got simplified.
    # [0, 0, 0, 0] is added and will be used as operation stopping token.
    batas_sub_images = np.append(batas_sub_images, [[0, 0, 0, 0]], axis=0)
    return batas_sub_images

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++  FUNCTION UNTUK MENCARI EDGE DI DALAM SETIAP SUB-IMAGE              +++
#+++  Variabel lense dibuat lokal di dalam fungsi ini, berd. nilai hld.  +++
#+++  Input: ori_gs, batas_sub_images, hld, dan var_th                   +++
#+++  Output: koordinat_obj.                                             +++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def cari_koordinat_edge(ori_gs, batas_sub_images, hld, var_th):
    print("np.shape(batas_sub_images) =", np.shape(batas_sub_images))
    m, n = np.shape(batas_sub_images)
    #The last n of the sub_images contains 0 0 0 0 as the stop token.
    #e.g. m = 13, n =4, then we need 13x2 for koordinat_obj to store y and x.
    koordinat_obj = np.arange(2*m).reshape(m, 2) #It has analogue shape with batas_sub_image
    koordinat_obj[m-1, :] = 0                    #It will be the stoping token.
    i = 0
    stop = 0
    while batas_sub_images[i, 0] > 0:
        print("i =", i)
        y1, y2, x1, x2 = batas_sub_images[i, 0:4]
        print("y1, y2, x1, x2 =", y1, y2, x1, x2)
        for y in range (y1, y2, hld):  #The scanning lense jumps rightward as much as hld.
            for x in range (x1, x2, hld): #and jumps downward as much as hld, too.
                lense = ori_gs[y-hld:y+hld+1, x-hld:x+hld+1] #Reading the targeted segment of the image with the lense.
                print('y, x, np.var(lense), var_th =', y, ',', x, ",", np.var(lense), ",", var_th, ".")
                if np.var(lense) > var_th:  #The condition to recognize whether the lense senses an edge or not.
                    stop = 1  #The information that the inner loop breaks is carried out to the outer loop.
                    print('     The x loop breaks here.')
                    break
            print('y, x =', y, ',', x)
            if stop == 1:                              #If the inner loop breaks, the outer loop will break too.
                print('     The y loop breaks here.')
                print('     An object is detected, thus the whole loop breaks here.\n')
                koordinat_obj[i,0], koordinat_obj[i,1] = y, x  #Masukkan y dan x ke koordinat_obj jika edge terdeteksi.
                break
        if stop == 0:
            koordinat_obj[i,0], koordinat_obj[i,1] = 1, 1 #Jika edge tidak terdeteksi, y,x, diberi angka 1, 1.

        print("y, x =", koordinat_obj[i,0], ",", koordinat_obj[i,1], ".")
        print("")
        stop = 0
        i += 1
    return koordinat_obj

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++ FUNCTION next_max_var UNTUK MENENTUKAN KOORDINAT LENSA SELANJUTNYA  +++
#+++ DAN INDIKASI ARAHNYA DENGAN METODE MAX_VAR
#+++ Input: posisi lensa sekarang (y,x) dan arah sekarang (curr_dir).     +++
#+++ Ouput: next_dir, y_next, x_next.                                    +++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def next_max_var(ori_gs, curr_dir, y, x):
    #print('Finding a neigboring segment that has highest variance...')
    next_dir = ""
    y_temp, x_temp = 0, 0            #y and x of temporary segment that has max-var
    var = np.uint16(0)          #Initial content of var array before being appended
    max_var = np.uint16(0)                  #Initial max_var before var is appended

    #print("#Looking east ...")
    if curr_dir != "west":                                   #To avoid a set back.
        x = x + hld
        lense = ori_gs[y-hld:y+hld+1, x-hld:x+hld+1]
        var = np.append(np.var(lense), var) #; print("var =", var)
        #print("max(var) = ", max(var))
        if max(var) > max_var:
             max_var = max(var)
             next_dir = "east"
             y_temp, x_temp = y, x;
        #print("max_var, y_temp, x_temp =", max_var, ",", y_temp, ",", x_temp)
        x = x - hld                                  #Put it back to previous position.

    #print("#Looking west...")
    if curr_dir != "east":
        x = x - hld
        lense = ori_gs[y-hld:y+hld+1, x-hld:x+hld+1]
        var = np.append(np.var(lense), var) #; print("var =", var)
        #print("max(var) = ", max(var))
        if max(var) > max_var:
             max_var = max(var)
             next_dir = "west"
             y_temp, x_temp = y, x;
        #print("max_var, y_temp, x_temp =", max_var, ",", y_temp, ",", x_temp)
        x = x + hld                                #Put it back to previous position.

    #print("#Looking south...")
    if curr_dir != "north":
        y = y + hld
        lense = ori_gs[y-hld:y+hld+1, x-hld:x+hld+1]
        var = np.append(np.var(lense), var) #; print("var =", var)
        #print("max(var) = ", max(var))
        if max(var) > max_var:
             max_var = max(var)
             next_dir = "south"
             y_temp, x_temp = y, x;
        #print("max_var, y_temp, x_temp =", max_var, ",", y_temp, ",", x_temp)
        y = y - hld                              #Put it back to previous position.

    #print("#Looking north ...")
    if curr_dir != "south":
        y = y - hld
        lense = ori_gs[y-hld:y+hld+1, x-hld:x+hld+1]
        var = np.append(np.var(lense), var) #; print("var =", var)
        #print("max(var) = ", max(var))
        if max(var) > max_var:
             max_var = max(var)
             next_dir = "north"
             y_temp, x_temp = y, x;
        #print("max_var, y_temp, x_temp =", max_var, ",", y_temp, ",", x_temp)
        y = y + hld                            #Put it back to previous position.

    #Concluding
    next_dir, y_next, x_next = next_dir, y_temp, x_temp
    return next_dir, y_next, x_next          #Next direction and coordinate of scanning lense.

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++  FUNCTION UNTUK MELUKIS KONTUR OBJEK                                    ++
#++  DENGAN MEMANGGIL FUNCTION next_max_var                                 ++
#++  Input: ori_gs, buffer, y, x di mana y, x diambilkan dari koordinat_obj ++
#++  Output: buffer yang sudah ditambahi warna kontur                       ++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def lukis_kontur(ori_gs, buffer, y, x):
    y_start, x_start = y, x
    #print("y_start, x_start =", y_start, ",", x_start, ".")
    curr_dir = ""                                         #curr_dir is initially NaN.
    distance = row   #Distance betw the lense and the start posistion; We initially set it far enough.
    #Ini perkiraan kasar untuk juml iterasi maks untuk objek yang besar.
    batas = round(1.5*(row+row+col+col)/hld)
    for j in range(0, batas):
        j += 1
        next_dir, y_next, x_next  = next_max_var(ori_gs, curr_dir, y, x)
        #print('Drawing a white mark at the object_s contour...')
        buffer[y-hld:y+hld+1, x-hld:x+hld+1] = warna_kontur
        curr_dir, y, x = next_dir, y_next, x_next
        distance = round(((y_next-y_start)**2 + (x_next-x_start)**2)**0.5)
        #print("i, sld, distance =", i, ",", sld, ",", distance, ".")
        if j > 10 and distance < round(0.8*sld): break
        # plt.figure('buffer')
        # plt.imshow(buffer, cmap = plt.cm.get_cmap('gray'))
        # plt.ion()
        # plt.show()
        # plt.pause(0.1)
        # print("")
    return buffer

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("(2) MAIN PROGRAM ...")                                    #++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("    CONTOUR DETECTION USING MAXIMUM VARIANCE IS TAKING PLACE...")
print("    During operation, measurement is done to the ori_gs, without changing any of its pixels.")
print("    Marking is done only to the buffer.")
print("    At last, cropping is done to the original color picture (pic).")
print("")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print ("(i)  PREPARATION: CREATING NEW VARIABLES BASED ON USER ENTRIES ...") #+
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
pic = plt.imread(dir + nama_file_input + ".jpg")
row, col, depth = np.shape(pic)
print("     col, row, depth =", row, ",", col, ",", depth, ".\n")
ori_gs = np.uint8(r*pic[:, :, 0] + g*pic[:, :, 1] + b*pic[:, :, 2])
buffer = np.uint8(r*pic[:, :, 0] + g*pic[:, :, 1] + b*pic[:, :, 2])

sld = round(sld*row)                                #scanning lense's diameter
hld = round(0.5*sld)                           #scanning lense's half diameter

#TM, BM, LM, and RM are to prevent the lense hit the image's boundary.
TM = round(1.5*sld)
BM = round(row-0.5*sld)
LM = round(1.5*sld)
RM = round(col-0.5*sld)

#Calculating the number of sub-images
nos = sub_image_structure[0] * sub_image_structure[1]   #Number of sub images

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("(ii) STATISTICS: FINDING max_var AND var_th OF THE WHOLE PICTURE...")
print("     The max(var) is used to define var_th.")
print("     Then var_th will be the threshold when detecting an object's contour.")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
tabel_var = menghitung_dan_menampung_var(ori_gs, TM, BM, LM, RM, hld)
print("      var_th_normal =", var_th_normal)
var_th = round(var_th_normal * max(tabel_var))
print("      min(var), max(var), var_th =", round(min(tabel_var)), ",", \
      round(max(tabel_var)), ",", var_th, ".\n")

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("(iii) CREATING THE TABLE OF batas-batas sub-images BERDASARKAN sub_image_structure. \n")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
batas_sub_images = buat_daftar_batas_sub_images(sub_image_structure, TM, BM, LM, RM)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("(iv) FIRST SCANNING: FINDING AN EDGE (GRIP) OF AN OBJECT WITHIN EVERY")
print("     SUB_IMAGE BASED ON batas_sub_images AND var_th...")
print("     The coordinates of the edges found (y, x) are stored in koordinat_obj.")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Create ori_gs again to avoid bugs, i.e. copying the lense to the previous ori_gs).
ori_gs = np.uint8(r*pic[:, :, 0] + g*pic[:, :, 1] + b*pic[:, :, 2])
print("     var_th =", var_th)
print("")
koordinat_obj = cari_koordinat_edge(ori_gs, batas_sub_images, hld, var_th)
print("np.shape(batas_sub_images) =", np.shape(batas_sub_images))
print("np.shape(koordinat_obj) =", np.shape(koordinat_obj))
print("batas_sub_images =", batas_sub_images)
print("koordinat_obj =", koordinat_obj)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
print("(v)  SECOND SCANNING. USING koordinat_obj AND MAX VAR METHOD, ")
print("     FIND OBJECT_S CONTOUR. OBJECT_S CONTOUR IS DRAWN FOR EVERY i.\n")
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Create ori_gs again to avoid bugs (copying from lense to the previous ori_gs)
ori_gs = np.uint8(r*pic[:, :, 0] + g*pic[:, :, 1] + b*pic[:, :, 2])
buffer = np.uint8(r*pic[:, :, 0] + g*pic[:, :, 1] + b*pic[:, :, 2])
print("koordinat_obj =", koordinat_obj)

i = 0
while koordinat_obj[i,0] > 0: #Koordinat_obj posisi terakhir saja yang berisi 0,0.
    print("i, koordinat_obj[i,0], koordinat_obj[i,1] =", i, ",", \
          koordinat_obj[i,0], ",", koordinat_obj[i,1], "." )
    y, x = koordinat_obj[i, 0], koordinat_obj[i, 1]
    hasil = lukis_kontur(ori_gs, buffer, y, x)
    buffer = hasil
    i += 1
    # plt.imshow(hasil, cmap=plt.cm.get_cmap('gray'))
    # plt.ion()
    # plt.show()
    # plt.pause(0.1)

if i == 0:
    print("No edge detected. Program finished.")

if i>0:
    #Konversikan hasil ke format jpg dan simpan ke storage.
    row, col = hasil.shape[0], hasil.shape[1]
    hasil_jpg = np.zeros(shape=(row, col, 3), dtype=np.uint8)
    hasil_jpg[:, :, 0], hasil_jpg[:, :, 1], hasil_jpg[:, :, 2]= hasil, hasil, hasil
    plt.imsave("hasil.jpg", hasil_jpg)
    plt.imshow(hasil, cmap=plt.cm.get_cmap('gray'))
    plt.ion()
    plt.show()
    plt.pause(300)

"""
README
Realization of algorithm for detecting multiple object's contour by Nasucha.
- First we detect an edge in every sub-image. An edge is an indicator that
  an object's contour can be possibly available.
- The picture is divided into (m, n) sub-images.
- Supposed you have (4, 4); it means you have 16 sub-images.
- The algorithm has been created in such a way that we detect a potential
  object's edge (a potensial pixel) within every sub-image. Thus, we store
  16 pixel coordinates [y, x] into an arary called koordinat_obj. In fact 
  we store [0, 0] at the end of koordinat_obj, thus we have 17 coordinates. 
  As [0, 0] is stored at the end of the array, luckily we use it as the
  'stopping' token of any operation that exercise koordinat_obj.
- It's not necessarily that the picture will have 16 objects, it may have,
  e.g. one object only. The good thing is that with 16 sub-images we may
  have up to 16 objects while it also can detect a single big object.
  
Terms
The scanning lense always perform "variance check" of all pixels under its
observation. 
In the first scanning, it checks if the variance is larger than threshold.
In the second scanning, it checks which one of 3 neighboring cells has the
maximum variance. The cell having the max_var is the next contour cell.
  
Steps
(1) Define the shape and size of the scanning lense. 
(2) Define how the picture is split into sub-images, e.g. 4 by 4. Using 
    this information and the pictures' row and col, find each boundary of 
    sub-image-0, sub-image-1, and so forth.
(3) Do statistical observation, to define var_th. That is, do the first
    scanning for the whole picture, find max_var then decide the value 
    of var_th.
(4) Do the first scanning to pixels within the sub-image-0, and using
    var_th find the coordinates of a potential object and store it to
    koordinat_obj. Do sequentially for sub-image-1 and so forth.  
(5) Do the second scanning. With koordinat_obj we know the positions of
    potential objects. 
    (a) Recall the coordinates of the grip (cell) of first object, mark 
        it white. It is the first cell of the object. Then scan 3 
        neighboring cells and decide which one has the maximum variance.
        That is the next cell. Then you can also provide an information
        about which direction is that next cell is actually going relative
        to previous cell.
    (b) Mark the next cell white. Repeat (i) until the next cell is 
         approaching the first cell.
    (c) Repeat (a) and (b) for the 2nd object, so forth.         
  
Useful syntax for creating penampung such as koordinat_obj:
a = np.arange(2).reshape(1,2)
a[:] = 0
print(a)
y_x_ = [[50, 100]]
a = np.append(y_x_, a, axis = 0)
print(a)

Pada kasus np.append ke variabel a
Misalnya angka 0 dimasukkan paling awal. Angka 1 dan 2 dimasukkan selanjutnya.
0 sebagai angka yang pertama masuk terdorong ke index terbesar.
Angka yang masuk terakhir memasuki indeks terendah, yaitu 0.
Jadi isi a(0) adalah 2, isi a(1) adalah 1 dan isi a(2) adalah 0.

print('y_min, y_max, x_min, x_max =', y_min,",", y_max, ",", x_min,",", x_max)
#Finding Margins of Object (min and max)
if cek_n1r > th2 or cek_n2r > th2 or cek_n3r > th2 or cek_n4r > th2:
    # print(i,j, "Edge detected")
    buffer[i, j, :] = 0, 0, 255  # Piksel yang merupakan edge diwarnai biru.
    n = n + 1
    yc = yc + i
    xc = xc + j
    if i < y_min: y_min = i
    if i > y_max: y_max = i
    if j < x_min: x_min = j
    if j > x_max: x_max = j
"""
