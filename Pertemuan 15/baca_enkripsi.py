def caesar_decrypt(ciphertext, shift):
    decrypted_text = ""
    for char in ciphertext:
        if char.isalpha():
            shifted = ord(char) - shift
            if char.islower():
                if shifted < ord('a'):
                    shifted += 26
                decrypted_text += chr(shifted)
            elif char.isupper():
                if shifted < ord('A'):
                    shifted += 26
                decrypted_text += chr(shifted)
        else:
            decrypted_text += char
    return decrypted_text

# Membaca dari file terenkripsi
with open('encrypted.txt', 'r') as file:
    ciphertext = file.read()

shift = 3  # Jumlah pergeseran yang digunakan untuk enkripsi

# Mendekripsi teks
decrypted_text = caesar_decrypt(ciphertext, shift)

# Menulis hasil dekripsi ke file lain
with open('decrypted.txt', 'w') as file:
    file.write(decrypted_text)

print("Teks terenkripsi berhasil didekripsi dan disimpan ke 'decrypted.txt'")
