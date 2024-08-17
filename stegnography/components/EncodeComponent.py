from django_unicorn.components import UnicornView
from stegano import lsb
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

class EncodecomponentView(UnicornView):
    message = ""
    cover_image = None
    stego_image_url = None

    def encode(self):
        if self.message and self.cover_image:
            # Hide the message in the image using Stegano
            stego_image = lsb.hide(self.cover_image.temporary_file_path(), self.message)
            
            # Save the stego image to an in-memory file
            output = io.BytesIO()
            stego_image.save(output, format="PNG")
            output.seek(0)

            # Convert to an InMemoryUploadedFile for easy download
            self.stego_image_url = InMemoryUploadedFile(output, None, 'stego_image.png', 'image/png', output.tell(), None)
            input('wait here')
        else:
            input(self.message)
