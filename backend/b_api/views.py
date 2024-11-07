from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import OCRImage
from .serializers import OCRImageCreateSerializer, OCRImageDetailSerializer, OCRResultSerializer
from PIL import Image
import pytesseract
from django.utils import timezone
from django.shortcuts import get_object_or_404

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
        
        try:
            ocr_image.text = pytesseract.image_to_string(Image.open(ocr_image.image))
            ocr_image.status = 'completed'
        except Exception as e:
            ocr_image.status = 'failed'
            ocr_image.text = f"OCR failed: {str(e)}"
        finally:
            ocr_image.completed_at = timezone.now()
            ocr_image.save()

        detail_serializer = OCRImageDetailSerializer(ocr_image, context={'request': request})
        return Response(
            detail_serializer.data,
            status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_get_delete(request, id, *args, **kwargs):
    """
    GET: Retrieve an OCR image
    DELETE: Remove an OCR image
    """
    ocr_image = get_object_or_404(OCRImage, id=id, user=request.user)

    if request.method == 'DELETE':
        ocr_image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'GET':
        serializer = OCRImageDetailSerializer(ocr_image, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def image_result(request, id, *args, **kwargs):
    ocr_image = get_object_or_404(OCRImage, id=id, user=request.user)
    serializer = OCRResultSerializer(ocr_image)
    return Response(serializer.data, status=status.HTTP_200_OK)
