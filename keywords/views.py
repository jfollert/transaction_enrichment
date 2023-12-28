from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Keyword
from merchants.models import Merchant
from .models import Keyword
from django.utils import timezone
import json

@csrf_exempt
def keywords_view(request):
  if request.method == 'POST':
    data = json.loads(request.body)

    # Validar el ID del comercio
    merchant_id = data.get('merchant_id')
    try:
      merchant = Merchant.objects.get(id=merchant_id)
    except Merchant.DoesNotExist:
      return HttpResponseBadRequest('Comercio inválido')

    keyword = data.get('keyword')
    current_timestamp = timezone.now()
    
    keyword = Keyword.objects.create(
      keyword=keyword,
      merchant=merchant,
      created_at=current_timestamp,
      updated_at=current_timestamp
    )
    
    response_data = {
      'id': keyword.id,
      'keyword': keyword.keyword,
      'merchant_id': keyword.merchant.id,
      'created_at': keyword.created_at,
      'updated_at': keyword.updated_at
    }
    return JsonResponse(response_data, status=201)
  
  elif request.method == 'GET':
    keywords = Keyword.objects.all()
    keywords_data = [{
      'id': keyword.id,
      'keyword': keyword.keyword,
      'merchant_id': keyword.merchant.id,
      'created_at': keyword.created_at,
      'updated_at': keyword.updated_at
    } for keyword in keywords]
    return JsonResponse(keywords_data, safe=False)
  
  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def keyword_detail(request, id):
  if request.method == 'GET':
    try:
      keyword = Keyword.objects.get(id=id)
    except Keyword.DoesNotExist:
      return HttpResponse(status=404)
    
    keyword_data = {
      'id': keyword.id,
      'keyword': keyword.keyword,
      'merchant_id': keyword.merchant.id,
      'created_at': keyword.created_at,
      'updated_at': keyword.updated_at
    }
    return JsonResponse(keyword_data, status=200)
  
  elif request.method == 'PUT':
    data = json.loads(request.body)

    keyword, created = Keyword.objects.get_or_create(id=id, defaults=data)
    
    if not created:
      # Validar el ID del comercio
      merchant_id = data.get('merchant_id')
      try:
        merchant = Merchant.objects.get(id=merchant_id)
        keyword.merchant = merchant
      except Merchant.DoesNotExist:
        return HttpResponseBadRequest('Comercio inválido')
      
      keyword.keyword = data.get('keyword', keyword.keyword)
      
      current_timestamp = timezone.now()
      keyword.updated_at = current_timestamp
      
      keyword.save()

    return HttpResponse(status=201 if created else 204)

  if request.method == 'DELETE':
    try:
      keyword = Keyword.objects.get(id=id)
      keyword.delete()
      return HttpResponse(status=204)
    except Keyword.DoesNotExist:
      return HttpResponse(status=404)

  else:
    return JsonResponse({'error': 'Method not allowed'}, status=405)