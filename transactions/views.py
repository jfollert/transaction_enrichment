from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Transaction
from django.utils import timezone
import json

@csrf_exempt
def transactions_view(request):
  if request.method == 'POST':
    data = json.loads(request.body)

    # Validar que es una lista
    if not isinstance(data, list):
      return JsonResponse({'error': 'Request body must be a list'}, status=400)  

    #Validar que cada elemento de la lista es un diccionario
    for transaction in data:
      if not isinstance(transaction, dict):
        return JsonResponse({'error': 'Request body must be a list of dictionaries'}, status=400)

    amount_of_transactions = len(data)
    amount_of_categorized_transactions = 0
    amount_of_merchant_identified_transactions = 0

    # Procesar transacciones
    for transaction in data:
      pass

    
    response_data = {
      'amount_of_transactions': amount_of_transactions,
      'categorization_rate': amount_of_categorized_transactions / amount_of_transactions,
      'merchant_identification_rate': amount_of_merchant_identified_transactions / amount_of_transactions,
    }
    return JsonResponse(response_data, status=201)
  
  
  else:
    return HttpResponse(status=405)