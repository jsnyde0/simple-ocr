import json
from django.http import JsonResponse

def api_home(request, *args, **kwargs):
    data = {}
    
    try:
        data = json.loads(request.body) # JSON.loads() converts JSON string to Python dictionary
    except:
        pass

    data['url_params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type

    return JsonResponse(data)