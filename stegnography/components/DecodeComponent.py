from django_unicorn.components import UnicornView
from stegano import lsb

class DecodecomponentView(UnicornView):
    stego_image = None
    decoded_message = None

    def decode(self):
        if self.stego_image:
            # Retrieve the hidden message from the image
            self.decoded_message = lsb.reveal(self.stego_image.temporary_file_path())
