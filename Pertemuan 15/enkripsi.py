from PIL import Image

def encrypt_image(image_path, message):
    image = Image.open(image_path)
    pixels = list(image.getdata())

    message_binary = ''.join(format(ord(char), '08b') for char in message)
    message_length = len(message_binary)

    if message_length > len(pixels):
        raise ValueError("Message is too large to be encrypted in the image.")

    encrypted_pixels = []
    for i in range(message_length):
        pixel = list(pixels[i])
        pixel[0] = pixel[0] & ~1 | int(message_binary[i])
        encrypted_pixels.append(tuple(pixel))

    encrypted_image = Image.new(image.mode, image.size)
    encrypted_image.putdata(encrypted_pixels)

    encrypted_image.save("encrypted_image.png")
    print("Encryption complete.")

image_path = "GreenTech Innovations.png"
message = "Halo selamat sore"

encrypt_image(image_path, message)
