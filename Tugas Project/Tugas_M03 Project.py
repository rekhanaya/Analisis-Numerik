print("\033c")
import numpy as np
import matplotlib.pyplot as plt

x_awal = -5.0
x_akhir = -4.0
dx = 0.001
err_m = 0.00001
x = x_awal
y = 2*x**3 - 3*x**2 - 5*x + 3

i = 0
while(x < x_akhir and y**2 > err_m**2):
    i = i + 1
    x = x + dx
    y = 2*x**3 - 3*x**2 - 5*x + 3
    print("Iterasi ke-", i)
    print("x =", x)
    print("y =", y)

print(" ")
print("VARIABEL")
print("x_awal =", x_awal)
print("x_akhir =", x_akhir)
print("dx =", dx)
print("error margin untuk y =", err_m)
print("HASIL AKHIR")
if(y<err_m):
    print("Pencarian akar berhasil.")
else:
    print("Pencarian akar gagal, silahkan perkecil dx atau perbesar error margin")
print("Banyaknya iterasi:", i)

#Visualisasikan Kurva
x = np.linspace(-2, 3, 10000)
plt.figure(figsize = (6, 6.5))
sumbu_x = x-x-0
y       = 2*x**3 - 3*x**2 - 5*x + 3
plt.plot(x, sumbu_x,                '-k')
plt.plot(x, (0.01-x**2)**0.5,       '-k')
plt.plot(x, -((0.01-x**2)**0.5),    '-k')
plt.plot(x, y,                      '-g', label = 'y')
plt.legend()
plt.grid()
plt.title('Visualization of the Polynomial Equation and Root')
plt.xlabel('x')
plt.ylabel('y')
plt.show()