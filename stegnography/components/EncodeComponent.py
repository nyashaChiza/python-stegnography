# views.py
from django_unicorn.components import UnicornView
from stegano import lsb
from django.core.files.base import ContentFile
from stegnography.forms import EncodeForm
import io
from django.conf import settings


class EncodecomponentView(UnicornView):
    form_class = EncodeForm
    stego_image_url = None

    def encode(self):
        form = self.form_class(self.request.POST, self.request.FILES)
        
        if form.is_valid():
            message = form.cleaned_data['message']
            cover_image = form.cleaned_data['cover_image']
            
            # Process the image
            image_file = cover_image.read()
            stego_image = lsb.hide(io.BytesIO(image_file), message)
            
            # Save to in-memory file
            output = io.BytesIO()
            stego_image.save(output, format="PNG")
            output.seek(0)
            file_name = 'stego_image.png'
            self.stego_image_url = ContentFile(output.read(), file_name)
            
            settings.LOGGER.debug(f'Stego image created: {file_name}')
        else:
            settings.LOGGER.error('Form validation failed')
