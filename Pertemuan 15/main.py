from cryptography.fernet import Fernet
from steganography import encode_image, decode_image

# Membuat kunci enkripsi
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Pesan yang akan disembunyikan
message = "Halo Selamat Pagi"

# Mengenkripsi pesan
encrypted_message = cipher_suite.encrypt(message.encode()).decode()

# Path ke gambar input dan output
input_image_path = 'gambar_pembawa.jpg'
output_image_path = 'gambar_hasil.png'

# Encode pesan terenkripsi ke dalam gambar
encode_image(input_image_path, output_image_path, encrypted_message)
print(f"Pesan terenkripsi telah disembunyikan dalam {output_image_path}")

# Decode pesan dari gambar
decoded_encrypted_message = decode_image(output_image_path)

# Mendekripsi pesan
decrypted_message = cipher_suite.decrypt(decoded_encrypted_message.encode()).decode()
print(f"Pesan yang diungkap: {decrypted_message}")
