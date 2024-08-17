import io
import os
import uuid

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, Client
from django.urls import reverse
from PIL import Image
from stegano import lsb



class EncodeViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.encode_url = reverse('encode')  # Update this if your URL pattern is different

    def test_encode_view_post(self):
        # Create a dummy image for testing
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)
        
        # Create a dummy message
        message = 'This is a secret message'
        
        # Post the form with the image and message
        response = self.client.post(self.encode_url, {
            'message': message,
            'cover_image': SimpleUploadedFile('test_image.png', image_io.read(), content_type='image/png')
        })
        
        # Check if the response is rendered correctly
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encryption/encrypt_result.html')
        
        # Check if the file was saved
        file_name = response.context['stego_image_file_name']
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        self.assertTrue(os.path.exists(file_path))
        
        # Clean up the file
        os.remove(file_path)

    def test_encode_view_get(self):
        response = self.client.get(self.encode_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encryption/encode.html')

class DecodeViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.decode_url = reverse('decode')  # Update this if your URL pattern is different

    def test_decode_view_post(self):
        # Create a dummy image for testing
        image = Image.new('RGB', (100, 100), color='red')
        image_io = io.BytesIO()
        image.save(image_io, format='PNG')
        image_io.seek(0)

        # Create a dummy message
        message = 'This is a secret message'
        stego_image = lsb.hide(image, message)
        output = io.BytesIO()
        stego_image.save(output, format="PNG")
        output.seek(0)

        # Post the form with the image
        response = self.client.post(self.decode_url, {
            'stego_image': SimpleUploadedFile('stego_image.png', output.read(), content_type='image/png')
        })

        # Check if the message was decoded
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encryption/decode.html')
        self.assertEqual(response.context['decoded_message'], message)

    def test_decode_view_get(self):
        response = self.client.get(self.decode_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'encryption/decode.html')

class DownloadFileTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.download_url = reverse('download', kwargs={'file_name': 'test_file.png'})  # Update this if your URL pattern is different

        # Create a dummy file for testing
        self.file_name = 'test_file.png'
        self.file_path = os.path.join(settings.MEDIA_ROOT, self.file_name)
        with open(self.file_path, 'wb') as f:
            f.write(b'This is a test file')

    def test_download_file_success(self):
        response = self.client.get(self.download_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Disposition'], f'attachment; filename="{self.file_name}"')
        self.assertEqual(response.content, b'This is a test file')

    def test_download_file_not_found(self):
        invalid_url = reverse('download', kwargs={'file_name': 'non_existent_file.png'})
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)

    def tearDown(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
