import json
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def api_home(request, *args, **kwargs):
    data = {}
    
    try:
        data = json.loads(request.body) # JSON.loads() converts JSON string to Python dictionary
    except:
        pass

    data['url_params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type

    return Response(data)