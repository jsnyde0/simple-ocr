from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from PIL import Image
import io
import os

class ImageUploadSerializerTests(TestCase):
    def setUp(self):
        # Create a simple test image in memory
        self.image = Image.new('RGB', (100, 100), color='white')
        img_io = io.BytesIO()
        self.image.save(img_io, 'PNG')
        self.image_file = SimpleUploadedFile(
            "test_image.png",
            img_io.getvalue(),
            content_type="image/png"
        )

    def test_valid_image_serializer(self):
        from .serializers import OCRImageCreateSerializer
        
        serializer = OCRImageCreateSerializer(data={
            'image': self.image_file
        })
        self.assertTrue(serializer.is_valid())

    def test_invalid_image_serializer(self):
        from .serializers import OCRImageCreateSerializer
        
        serializer = OCRImageCreateSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('image', serializer.errors)

class OCRAPIViewTests(APITestCase):
    def setUp(self):
        # set up user and token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        # Create a test image with known text
        self.test_image_path = os.path.join(
            os.path.dirname(__file__),
            'test_files',
            'tesseract-example-noisy.png'
        )
        
    def test_image_create(self):
        """Test successful image creation"""
        url = reverse('api:image_create')
        headers = {
            'Authorization': f'Token {self.token.key}'
        }
        
        with open(self.test_image_path, 'rb') as image_file:
            response = self.client.post(
                url,
                {'image': image_file},
                format='multipart',
                headers=headers
            )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('self_url', response.data)
        self.assertIn('delete_url', response.data)
        self.assertIn('result_url', response.data)
        self.assertIn('status', response.data)
        self.assertNotEqual(response.data['status'], 'failed')

    def test_invalid_image_create(self):
        """Test uploading an invalid file"""
        url = reverse('api:image_create')
        headers = {
            'Authorization': f'Token {self.token.key}'
        }
        
        invalid_file = SimpleUploadedFile(
            "file.txt",
            b"This is not an image",
            content_type="text/plain"
        )
        
        response = self.client.post(
            url,
            {'image': invalid_file},
            format='multipart',
            headers=headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)