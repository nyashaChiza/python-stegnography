import os
import uuid
import io
from django.conf import settings
from django.shortcuts import render
from django.core.files.base import ContentFile
from PIL import Image
from stegnography.forms import FileEncodeForm, FileDecodeForm  # Ensure you have this form

# Utility functions for binary conversion
def file_to_binary(file_bytes):
    return ''.join(format(byte, '08b') for byte in file_bytes)

def binary_to_bytes(binary_data):
    byte_data = bytearray(int(binary_data[i:i+8], 2) for i in range(0, len(binary_data), 8))
    return bytes(byte_data)

def file_encode_view(request):
    if request.method == 'POST':
        form = FileEncodeForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the form data
            file = form.cleaned_data['file']  # This should be a file
            cover_image = form.cleaned_data['cover_image']

            # Read file into memory
            file_content = file.read()
            binary_data = file_to_binary(file_content)

            # Process the image and file content
            image_file = cover_image.read()
            image = Image.open(io.BytesIO(image_file))

            # Encode the file content into the image
            pixels = list(image.getdata())
            binary_data += '1111111111111110'  # Add a delimiter to signify the end of data

            new_pixels = []
            data_index = 0
            settings.LOGGER.critical('processing pixels')
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

                if len(pixel) == 4:
                    new_pixels.append((new_r, new_g, new_b, pixel[3]))
                else:
                    new_pixels.append((new_r, new_g, new_b))

            new_image = Image.new(image.mode, image.size)
            new_image.putdata(new_pixels)

            # Save the stego image to an in-memory file
            output = io.BytesIO()
            new_image.save(output, format="PNG")
            output.seek(0)

            # Generate a unique file name
            file_name = f'stego_image_{uuid.uuid4().hex[:6]}.png'
            stego_image_file = ContentFile(output.read(), file_name)

            # Save file to media folder
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(stego_image_file.read())

            # Pass file_name_only to the context
            return render(request, 'encryption/file/encrypt_result.html', {'stego_image_file_name': file_name})

    else:
        form = FileEncodeForm()

    return render(request, 'encryption/file/encode.html', {'form': form})


def file_decode_view(request):
    if request.method == 'POST':
        form = FileDecodeForm(request.POST, request.FILES)

        if form.is_valid():
            # Get the uploaded stego image
            stego_image = form.cleaned_data['stego_image']

            # Read the image file into memory
            image_file = stego_image.read()
            image = Image.open(io.BytesIO(image_file))

            # Decode the message from the image
            pixels = list(image.getdata())
           
            binary_data = ""
            for count ,pixel in enumerate(pixels):
                settings.LOGGER.debug(f'processing pixels: {count/len(pixels) * 100:.2f}%')
                r, g, b = pixel[:3]
                binary_data += str(r & 1)
                binary_data += str(g & 1)
                binary_data += str(b & 1)

            # Find the delimiter and cut the data there
            delimiter = '1111111111111110'
            end_index = binary_data.find(delimiter)
            if end_index != -1:
                binary_data = binary_data[:end_index]

            decoded_file_content = binary_to_bytes(binary_data)

            file_name = 'decoded_file'  # Adjust the file extension as needed

            # Save the decoded file to an in-memory file
            output = io.BytesIO(decoded_file_content)
            content_file = ContentFile(output.read(), file_name)

            # Save file to media folder
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'wb') as f:
                f.write(content_file.read())

            # Pass file_name to the context
            return render(request, 'encryption/file/decode_result.html', {'decoded_file_name': file_name})

    else:
        form = FileDecodeForm()

    return render(request, 'encryption/file/decode.html', {'form': form})
