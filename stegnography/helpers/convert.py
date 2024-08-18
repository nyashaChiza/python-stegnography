from PIL import Image

def file_to_binary(file_bytes):
    return ''.join(format(byte, '08b') for byte in file_bytes)


def binary_to_bytes(binary_data):
    byte_data = bytearray(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
    return bytes(byte_data)


def file_to_bytes(file_path):
    with open(file_path, 'rb') as file:
        file_bytes = file.read()
    return file_bytes


def bytes_to_file(file_path, file_bytes):
    with open(file_path, 'wb') as file:
        file.write(file_bytes)


def hide_data_in_image(image_path, file_bytes, output_image_path):
    image = Image.open(image_path)
    pixels = list(image.getdata())

    binary_data = file_to_binary(file_bytes)
    binary_data += '1111111111111110'  # Add a delimiter to signify the end of data

    new_pixels = []
    data_index = 0
    for pixel in pixels:
        r, g, b = pixel[:3]
        if data_index < len(binary_data):
            new_r = (r & ~1) | int(binary_data[data_index])
            data_index += 1
        else:
            new_r = r
            
        if data_index < len(binary_data):
            new_g = (g & ~1) | int(binary_data[data_index])
            data_index += 1
        else:
            new_g = g
            
        if data_index < len(binary_data):
            new_b = (b & ~1) | int(binary_data[data_index])
            data_index += 1
        else:
            new_b = b

        # Maintain the alpha channel if present
        if len(pixel) == 4:
            new_pixels.append((new_r, new_g, new_b, pixel[3]))
        else:
            new_pixels.append((new_r, new_g, new_b))

    new_image = Image.new(image.mode, image.size)
    new_image.putdata(new_pixels)
    new_image.save(output_image_path)
    
    
def extract_data_from_image(image_path):
    image = Image.open(image_path)
    pixels = list(image.getdata())

    binary_data = ""
    for pixel in pixels:
        r, g, b = pixel[:3]
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)

    # Find the delimiter and cut the data there
    delimiter = '1111111111111110'
    end_index = binary_data.find(delimiter)
    if end_index != -1:
        binary_data = binary_data[:end_index]
    
    return binary_to_bytes(binary_data)

