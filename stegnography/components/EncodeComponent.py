from django_unicorn.components import UnicornView
from stegano import lsb
from django.core.files.base import ContentFile
from PIL import Image
from django.conf import settings
import io

class EncodecomponentView(UnicornView):
    stego_image_url = None
    message = ""
    cover_image = None

    def encode(self):
        if self.cover_image and self.message:
            input(self.cover_image)
            # Read the image file into memory
            image_file = self.cover_image.read()
            
            # Open the image with PIL
            image = Image.open(io.BytesIO(image_file))
            
            # Process the image with the message
            stego_image = lsb.hide(image, self.message)
            
            # Save the stego image to an in-memory file
            output = io.BytesIO()
            stego_image.save(output, format="PNG")
            output.seek(0)

            # Convert the in-memory image to a ContentFile
            file_name = 'stego_image.png'
            self.stego_image_url = ContentFile(output.read(), file_name)
            
            # Optionally save the file or perform further actions
        else:
            # Handle errors or invalid form submissions
            settings.LOGGERdebug('input not found')
