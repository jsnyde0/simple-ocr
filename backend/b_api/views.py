from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import ImageUploadSerializer

@api_view(['POST'])
def api_home(request, *args, **kwargs):
    serializer = ImageUploadSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        image = serializer.validated_data['file']
        return Response({
            'image_name': image.name,
            'image_size': image.size,
            'content_type': image.content_type
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
