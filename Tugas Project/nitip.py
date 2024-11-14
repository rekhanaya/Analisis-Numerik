import numpy as np
import matplotlib.pyplot as plt

# Parameter
x_awal = -2.0
x_akhir = -1.0
dx = 0.0001
err_m = 0.0001

# Fungsi
def fungsi(x):
    return 2*x**3 - 3*x**2 - 5*x + 3

# Iterasi
x = x_awal
y = fungsi(x)
i = 0

while x < x_akhir and abs(y) > err_m:
    i += 1
    x += dx
    y = fungsi(x)

# Cek keberhasilan pencarian akar
if abs(y) < err_m:
    print("Pencarian akar berhasil.")
    akar = x
else:
    print("Pencarian akar gagal, silahkan perkecil dx atau perbesar error margin.")
    akar = np.nan
print("Banyaknya iterasi:", i)
print("x =", x)
print("y =", y)

# Visualisasi Kurva
x = np.linspace(-2, 3, 1000)
plt.figure(figsize=(8, 6))
plt.plot(x, fungsi(x), '-g', label='y')
plt.axhline(0, color='black', linewidth=0.5, linestyle='--')

# Tampilkan akar pada grafik
plt.axvline(akar, color='red', linewidth=0.5, linestyle='--', label='Root')
plt.text(akar, 0.5, f'Akar: {akar:.4f}', color='red')

plt.legend()
plt.grid()
plt.title('Visualization of the Polynomial Equation and Root')
plt.xlabel('x')
plt.ylabel('y')
plt.show()