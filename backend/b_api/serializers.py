from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    file = serializers.ImageField()

    # Optional: Custom validation to ensure it's an image
    def validate_file(self, value):
        """
        Field-level validation for 'file' field.
        Called automatically for the 'file' field.
        """
        if not value.content_type.startswith("image"):
            raise serializers.ValidationError("Uploaded file is not an image.")
        
        # You can access file properties:
        print(f"File size: {value.size} bytes")
        print(f"Content type: {value.content_type}")
        print(f"File name: {value.name}")
        
        return value
