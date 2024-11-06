from rest_framework import serializers
from .models import OCRImage


class OCRImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRImage
        fields = ['image']

    def validate_image(self, value):
        """Optional: Add specific size/dimension validation if needed"""
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError("Image file too large ( > 5MB )")
        return value

class OCRImageDetailSerializer(serializers.ModelSerializer):
    result_url = serializers.HyperlinkedIdentityField(
        view_name='api:image_result',
        lookup_field='id',
        lookup_url_kwarg='id'
    )
    class Meta:
        model = OCRImage
        fields = ['id', 'status', 'uploaded_at', 'completed_at', 'result_url']
        read_only_fields = fields

class OCRResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRImage
        fields = ['id', 'text', 'completed_at']
        read_only_fields = fields
