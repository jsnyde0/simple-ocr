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

class ImageSerializerTests(TestCase):
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

class OCRAPITests(APITestCase):
    def setUp(self):
        # set up user and token
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.headers = {
            'Authorization': f'Token {self.token.key}'
        }
        # Create a test image with known text
        self.test_image_path = os.path.join(
            os.path.dirname(__file__),
            'test_files',
            'tesseract-example-noisy.png'
        )

    def _create_test_image(self):
        """Helper method to create a test image and return its ID"""
        url = reverse('api:image_create')
        with open(self.test_image_path, 'rb') as image_file:
            response = self.client.post(
                url,
                {'image': image_file},
                format='multipart',
                headers=self.headers
            )
        return response.data['id']
        
    def test_image_create(self):
        """Test successful image creation"""
        create_url = reverse('api:image_create')
        headers = {
            'Authorization': f'Token {self.token.key}'
        }
        
        with open(self.test_image_path, 'rb') as image_file:
            response = self.client.post(
                create_url,
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
        create_url = reverse('api:image_create')
        
        invalid_file = SimpleUploadedFile(
            "file.txt",
            b"This is not an image",
            content_type="text/plain"
        )
        
        response = self.client.post(
            create_url,
            {'image': invalid_file},
            format='multipart',
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_image(self):
        """Test successful image retrieval"""
        image_id = self._create_test_image()
        get_url = reverse('api:image_get_delete', kwargs={'id': image_id})
        
        response = self.client.get(
            get_url,
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('self_url', response.data)
        self.assertIn('delete_url', response.data)
        self.assertIn('result_url', response.data)
        self.assertIn('status', response.data)
        self.assertNotEqual(response.data['status'], 'failed')

    def test_delete_image(self):
        """Test successful image retrieval"""
        image_id = self._create_test_image()
        delete_url = reverse('api:image_get_delete', kwargs={'id': image_id})
        
        response = self.client.delete(
            delete_url,
            headers=self.headers
        )
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_image_result(self):
        """Test successful image result retrieval"""
        image_id = self._create_test_image()

        get_image_url = reverse('api:image_get_delete', kwargs={'id': image_id})
        get_image_response = self.client.get(
            get_image_url,
            headers=self.headers
        )

        get_result_url = get_image_response.data['result_url']
        get_result_response = self.client.get(
            get_result_url,
            headers=self.headers
        )

        self.assertEqual(get_result_response.status_code, status.HTTP_200_OK)
        self.assertIn('text', get_result_response.data)
        self.assertEqual(get_result_response.data['text'], 'Tesseract sample\n')