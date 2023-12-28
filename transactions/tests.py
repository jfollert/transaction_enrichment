from django.test import TestCase
from django.urls import reverse
from keywords.models import Keyword
from merchants.models import Merchant
from categories.models import Category
import json
import uuid

class TransactionEnrichmentTestCase(TestCase):
  def setUp(self):
    # Crear datos de prueba: categoría, comerciante y keyword
    category = Category.objects.create(name='Food', type='expense')
    merchant = Merchant.objects.create(
      merchant_name='Test Merchant',
      merchant_logo='https://example.com/logo.png',
      category_id=category,
    )
    Keyword.objects.create(keyword='testmerchant', merchant=merchant)

  def test_enrich_transaction(self):
    """ Test para enriquecer transacciones """
    
    # Transacciones de prueba
    transactions = [
      {
        'id': str(uuid.uuid4()),
        'description': 'Pago en TestMerchant',
        'amount': 100,
        'date': '2021-01-01'
      },
      # Puedes añadir más transacciones aquí
    ]

    # Enviar solicitud POST al endpoint
    url = reverse('transactions:transactions')  # Asegúrate de que el nombre del endpoint es correcto
    response = self.client.post(url, json.dumps(transactions), content_type='application/json')

    # Verificar que la respuesta sea correcta
    self.assertEqual(response.status_code, 201)
    response_data = json.loads(response.content)
    self.assertEqual(len(response_data['transactions']), len(transactions))

    # Verificar que las transacciones estén enriquecidas correctamente
    for transaction in response_data['transactions']:
      self.assertIn('merchant', transaction)
      self.assertIn('category', transaction)
      self.assertEqual(transaction['merchant']['name'], 'Test Merchant')
      self.assertEqual(transaction['category']['name'], 'Food')

    # Verificar tasas de categorización y de identificación de comerciantes
    self.assertGreater(response_data['categorization_rate'], 0)
    self.assertGreater(response_data['merchant_identification_rate'], 0)
