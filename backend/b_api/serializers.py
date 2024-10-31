from rest_framework import serializers
from .models import Document

class ImageUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'image', 'uploaded_at']

    # Optional: Custom validation to ensure it's an image
    def validate_image(self, value):
        """
        Field-level validation for 'image' field.
        Called automatically for the 'image' field.
        """
        if not value.content_type.startswith("image"):
            raise serializers.ValidationError("Uploaded file is not an image.")
        
        # You can access file properties:
        print(f"Image size: {value.size} bytes")
        print(f"Content type: {value.content_type}")
        print(f"Image name: {value.name}")

        return value
