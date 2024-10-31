from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ImageUploadSerializer
from PIL import Image
import pytesseract
import io

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    serializer = ImageUploadSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        image_file = serializer.validated_data['image']
        image = Image.open(image_file)

        try:
            extracted_text = pytesseract.image_to_string(image)
            return Response({
                'text': extracted_text,
                'status': 'success'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'OCR failed': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        document = serializer.save()
        return Response({
            'id': document.id,
            'image_name': document.image.name,
            'image_size': document.image.size,
            'image_url': document.image.url,
            'uploaded_at': document.uploaded_at,
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
