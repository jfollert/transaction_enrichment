from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from keywords.models import Keyword
import json
from datetime import datetime

@csrf_exempt
def transactions_view(request):
  if request.method != 'POST':
    return HttpResponse(status=405)

  try:
    data = json.loads(request.body)
  except json.JSONDecodeError:
    return JsonResponse({'error': 'Invalid JSON'}, status=400)

  # Validar que es una lista
  if not isinstance(data, list):
    return JsonResponse({'error': 'Request body must be a list'}, status=400)  
    
  amount_of_transactions = len(data)
  amount_of_categorized_transactions = 0
  amount_of_merchant_identified_transactions = 0
  transactions = []

  # Obtener keywords
  keywords = Keyword.objects.all()
  keywords_dict = {keyword.keyword.lower(): keyword for keyword in keywords}

  # Procesar transacciones
  for transaction in data:

    # Validar transacción
    validation_error  = validate_transaction(transaction)
    if validation_error :
      return JsonResponse({'error': validation_error}, status=400)
    
    description = transaction.get('description')
    description_lower = description.lower()

    enriched_transaction = {
      'id': transaction.get('id'),
      'amount': transaction.get('amount', ''),
      'description': description,
      'date': transaction.get('date', ''),
    }

    # Categorizar transacciones
    for keyword_lower, keyword in keywords_dict.items():
      if keyword_lower in description_lower:

        # Identificar comercio
        if keyword.merchant != None:
          enriched_transaction['merchant'] = {
            'name': keyword.merchant.merchant_name,
            'logo': keyword.merchant.merchant_logo
          }
          amount_of_merchant_identified_transactions += 1

          # Identificar categoría
          if keyword.merchant.category_id != None:
            enriched_transaction['category'] = {
              'name': keyword.merchant.category_id.name,
              'type': keyword.merchant.category_id.type
            }
            amount_of_categorized_transactions += 1
          
        break
    

    transactions.append(enriched_transaction)
  
  response_data = {
    'transactions': transactions,
    'amount_of_transactions': amount_of_transactions,
    'categorization_rate': amount_of_categorized_transactions / amount_of_transactions,
    'merchant_identification_rate': amount_of_merchant_identified_transactions / amount_of_transactions
  }
  return JsonResponse(response_data, status=201)



def validate_transaction(transaction):
  if not isinstance(transaction, dict):
      return 'Request body must be a list of dictionaries'
  
  if not transaction.get('id'):
      return 'All transactions must have an ID'
  
  if not transaction.get('description'):
      return 'All transactions must have a description'
  
  if not transaction.get('amount'):
    return 'All transactions must have an amount'
  
  try:
    transaction['amount'] = float(transaction['amount'])
  except ValueError:
    return 'Amount must be a number'
  
  if not transaction.get('date'):
    return 'All transactions must have a date'
  
  try:
    transaction['date'] = str(transaction['date'])
  except ValueError:
    return 'Date must be a string'
  
  try:
    transaction['date'] = datetime.strptime(transaction['date'], '%Y-%m-%d')
  except ValueError:
    return 'Date must be in the format YYYY-MM-DD'
  
  return None 