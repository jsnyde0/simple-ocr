from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ImageUploadSerializer
from PIL import Image
import pytesseract

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    try:
        serializer = ImageUploadSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({
                'error': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        

        image_file = serializer.validated_data['image']
        image = Image.open(image_file)
        extracted_text = pytesseract.image_to_string(image)
        
        return Response({
            'text': extracted_text,
            'status': 'success'
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
