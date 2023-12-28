from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Merchant
from categories.models import Category
from django.utils import timezone
import json

@csrf_exempt
def merchants_view(request):
  if request.method == 'POST':
    data = json.loads(request.body)

    # Validar el ID de la categoría si viene el campo solamente
    category_id = data.get('category_id')
    if category_id != None:
      try:
        category = Category.objects.get(id=category_id)
      except Category.DoesNotExist:
        return HttpResponseBadRequest('Categoría inválida')

    merchant_name = data.get('merchant_name')
    merchant_logo = data.get('merchant_logo')
    # category_id = data.get('category_id')
    current_timestamp = timezone.now()
    
    merchant = Merchant.objects.create(
      merchant_name=merchant_name,
      merchant_logo=merchant_logo,
      category_id=category,
      created_at=current_timestamp,
      updated_at=current_timestamp
    )
    
    response_data = {
      'id': merchant.id,
      'merchant_name': merchant.merchant_name,
      'merchant_logo': merchant.merchant_logo,
      'category_id': merchant.category_id.id,
      'created_at': merchant.created_at,
      'updated_at': merchant.updated_at
    }
    return JsonResponse(response_data, status=201)
  
  elif request.method == 'GET':
    merchants = Merchant.objects.all()
    merchants_data = [{
      'id': merchant.id,
      'merchant_name': merchant.merchant_name,
      'merchant_logo': merchant.merchant_logo,
      'category_id': merchant.category_id.id,
      'created_at': merchant.created_at,
      'updated_at': merchant.updated_at
    } for merchant in merchants]
    return JsonResponse(merchants_data, safe=False)
  
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def merchant_detail(request, id):
  if request.method == 'GET':
    try:
      merchant = Merchant.objects.get(id=id)
    except Merchant.DoesNotExist:
      return HttpResponse(status=404)
    
    merchant_data = {
      'id': merchant.id,
      'merchant_name': merchant.merchant_name,
      'merchant_logo': merchant.merchant_logo,
      'category_id': merchant.category_id.id,
    }
    return JsonResponse(merchant_data, status=200)
  
  elif request.method == 'PUT':
    data = json.loads(request.body)

    try:
      merchant = Merchant.objects.get(id=id)
    except Merchant.DoesNotExist:
      merchant = Merchant(id=id)

    # Validar el ID de la categoría
    category_id = data.get('category_id')
    if category_id != None:
      try:
        category = Category.objects.get(id=category_id)
        merchant.category_id = category
      except Category.DoesNotExist:
        return HttpResponseBadRequest('Categoría inválida')
    
    merchant.merchant_name = data.get('merchant_name', merchant.merchant_name)
    merchant.merchant_logo = data.get('merchant_logo', merchant.merchant_logo)
    
    current_timestamp = timezone.now()
    merchant.updated_at = current_timestamp
    
    merchant.save()

    return HttpResponse(status=204)

  if request.method == 'DELETE':
    try:
      merchant = Merchant.objects.get(id=id)
      merchant.delete()
      return HttpResponse(status=204)
    except Merchant.DoesNotExist:
      return HttpResponse(status=404)