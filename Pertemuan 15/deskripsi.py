from PIL import Image

def decrypt_image(image_path):
    image = Image.open(image_path)
    pixels = list(image.getdata())

    message_binary = ""
    for pixel in pixels:
        message_binary += str(pixel[0] & 1)

    message = ""
    for i in range(0, len(message_binary), 8):
        byte = message_binary[i:i+8]
        message += chr(int(byte, 2))

    print("Decrypted message:", message)

image_path = "encrypted_image.png"
decrypt_image(image_path)
