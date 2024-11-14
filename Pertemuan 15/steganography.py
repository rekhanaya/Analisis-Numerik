from PIL import Image

def encode_image(input_image_path, output_image_path, message):
    # Buka gambar input
    image = Image.open(input_image_path)
    encoded = image.copy()
    width, height = image.size
    
    # Ubah pesan menjadi biner
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1111111111111110'  # Penanda akhir pesan
    
    data_index = 0
    message_length = len(binary_message)
    
    for row in range(height):
        for col in range(width):
            if data_index < message_length:
                r, g, b = image.getpixel((col, row))
                # Ubah bit terakhir dari merah dengan bit pesan
                r = (r & 0b11111110) | int(binary_message[data_index])
                data_index += 1
                if data_index < message_length:
                    g = (g & 0b11111110) | int(binary_message[data_index])
                    data_index += 1
                if data_index < message_length:
                    b = (b & 0b11111110) | int(binary_message[data_index])
                    data_index += 1
                encoded.putpixel((col, row), (r, g, b))
    
    encoded.save(output_image_path)

def decode_image(image_path):
    image = Image.open(image_path)
    width, height = image.size
    
    binary_message = ""
    
    for row in range(height):
        for col in range(width):
            r, g, b = image.getpixel((col, row))
            binary_message += bin(r)[-1]
            binary_message += bin(g)[-1]
            binary_message += bin(b)[-1]
    
    # Bagi biner menjadi 8 bit dan ubah menjadi karakter
    all_bytes = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = ""
    
    for byte in all_bytes:
        if byte == '11111110':
            break
        decoded_message += chr(int(byte, 2))
    
    return decoded_message
