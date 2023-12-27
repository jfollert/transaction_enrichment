from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Category
from django.utils import timezone
from django.shortcuts import get_object_or_404
import json

@csrf_exempt
def categories_view(request):
  if request.method == 'POST':
    data = request.body
    data = json.loads(data)

    name = data.get('name')
    type = data.get('type')
    
    category = Category.objects.create(name=name, type=type, created_at=timezone.now(), updated_at=timezone.now())
    
    response_data = {'id': category.id, 'name': category.name, 'type': category.type, 'created_at': category.created_at, 'updated_at': category.updated_at}
    return JsonResponse(response_data, status=201)
  
  elif request.method == 'GET':
    categories = Category.objects.all()
    category_data = [{'id': category.id, 'name': category.name, 'type': category.type} for category in categories]
    return JsonResponse(category_data, safe=False)
  
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def category_detail(request, id):
  category = get_object_or_404(Category, id=id)

  if request.method == 'GET':
    # Handle GET request to retrieve a category by its UUID
    category_data = {
      'id': category.id,
      'name': category.name,
      'type': category.type,
      'created_at': category.created_at,
      'updated_at': category.updated_at
    }
    return JsonResponse(category_data, status=200)
  
  elif request.method == 'PUT':
    # Handle PUT request to update a category by its UUID
    data = json.loads(request.body)
    category.name = data.get('name', category.name)
    category.type = data.get('type', category.type)
    category.updated_at = timezone.now()
    category.save()
    return HttpResponse(status=204)

  if request.method == 'DELETE':
    # Handle DELETE request to delete a category by its UUID
    category.delete()
    return HttpResponse(status=204)

  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)