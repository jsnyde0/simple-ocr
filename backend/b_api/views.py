from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import OCRImageCreateSerializer, OCRImageDetailSerializer, OCRResultSerializer
from PIL import Image
import pytesseract
from django.utils import timezone

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_create(request, *args, **kwargs):
    try:
        serializer = OCRImageCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        ocr_image = serializer.save(user=request.user)
        
        ocr_image.text = pytesseract.image_to_string(Image.open(ocr_image.image))
        ocr_image.status = 'completed'
        ocr_image.completed_at = timezone.now()
        ocr_image.save()

        detail_serializer = OCRImageDetailSerializer(ocr_image)
        return Response(
            detail_serializer.data,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
