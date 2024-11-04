from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()

    # Optional: Custom validation to ensure it's an image
    def validate_image(self, value):
        """
        Field-level validation for 'image' field.
        """
        if not value.content_type.startswith("image"):
            raise serializers.ValidationError("Uploaded file is not an image.")
        
        # You can access file properties:
        print(f"Image size: {value.size} bytes")
        print(f"Content type: {value.content_type}")
        print(f"Image name: {value.name}")

        return value
