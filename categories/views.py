from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category
from django.utils import timezone

@csrf_exempt
def create_category(request):
  if request.method == 'POST':
    data = request.POST  # Get data from POST request
    name = data.get('name')
    type = data.get('type')
    
    category = Category.objects.create(name=name, type=type, created_at=timezone.now(), updated_at=timezone.now())
    
    response_data = {'id': category.id, 'name': category.name, 'type': category.type, 'created_at': category.created_at, 'updated_at': category.updated_at}
    return JsonResponse(response_data, status=201)
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)

