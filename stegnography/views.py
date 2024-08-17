import os
import uuid
import io
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.core.files.base import ContentFile
from stegnography.forms import EncodeForm, DecodeForm
from stegano import lsb
from PIL import Image
from django.utils.http import unquote

def encode_view(request):
    if request.method == 'POST':
        form = EncodeForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the form data
            message = form.cleaned_data['message']
            cover_image = form.cleaned_data['cover_image']

            # Process the image and message
            image_file = cover_image.read()
            image = Image.open(io.BytesIO(image_file))
            stego_image = lsb.hide(image, message)
            
            # Save the stego image to an in-memory file
            output = io.BytesIO()
            stego_image.save(output, format="PNG")
            output.seek(0)
            
            # Generate a unique file name
            file_name = f'stego_image_{uuid.uuid4().hex[:6]}.png'
            stego_image_file = ContentFile(output.read(), file_name)
            
            # Save file to media folder
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            with open(file_path, 'wb') as f:
                f.write(stego_image_file.read())

            # Extract just the file name from the path
            file_name_only = os.path.basename(file_path)

            # Pass file_name_only to the context
            return render(request, 'encryption/encrypt_result.html', {'stego_image_file_name': file_name_only})

    else:
        form = EncodeForm()

    return render(request, 'encryption/encode.html', {'form': form})

def decode_view(request):
    decoded_message = None
    if request.method == 'POST':
        form = DecodeForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the uploaded stego image
            stego_image = form.cleaned_data['stego_image']
            
            # Read the image file into memory
            image_file = stego_image.read()
            image = Image.open(io.BytesIO(image_file))
            
            # Decode the message from the image
            decoded_message = lsb.reveal(image)
    else:
        form = DecodeForm()

    return render(request, 'encryption/decode.html', {'form': form, 'decoded_message': decoded_message})

def download_file(request, file_name):
    # Construct the file path
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    # Check if the file exists
    if not os.path.exists(file_path):
        raise Http404("File does not exist")
    
    # Open the file
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{unquote(file_name)}"'
        return response
