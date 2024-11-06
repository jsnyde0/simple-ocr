from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class OCRImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='ocr_images/', error_messages={
        'invalid': "Please upload a valid image file.",
        'required': "An image file is required."
    })
    uploaded_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('processing', 'Processing'),
            ('completed', 'Completed'),
            ('failed', 'Failed')
        ],
        default='processing'
    )
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"OCR Image {self.id} by {self.user.username}"

    class Meta:
        ordering = ['-uploaded_at']

