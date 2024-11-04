from rest_framework import serializers

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField(
        error_messages={
            'invalid': "Please upload a valid image file.",
            'required': "An image file is required."
        }
    )

    def validate_image(self, value):
        """Optional: Add specific size/dimension validation if needed"""
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError("Image file too large ( > 5MB )")
        return value
