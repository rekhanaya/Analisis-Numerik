from cryptography.fernet import Fernet
from steganography.steganography import Steganography

# Membuat kunci enkripsi
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Mengenkripsi pesan
pesan = "Halo Ananta"
pesan_terenkripsi = cipher_suite.encrypt(pesan.encode())

# Menyembunyikan pesan terenkripsi dalam gambar
Steganography.encode("gambar_pembawa.jpg", "gambar_hasil.png", pesan_terenkripsi.decode())

# Mengungkap pesan terenkripsi dari gambar
pesan_terenkripsi_tersembunyi = Steganography.decode("gambar_hasil.png")

# Mendekripsi pesan
pesan_dekripsi = cipher_suite.decrypt(pesan_terenkripsi_tersembunyi.encode()).decode()
print(pesan_dekripsi)
