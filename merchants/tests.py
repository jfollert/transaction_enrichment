from django.test import TestCase
from django.urls import reverse
from merchants.models import Merchant
from categories.models import Category
import json
import uuid

class MerchantAPITestCase(TestCase):
  def setUp(self):
    self.category = Category.objects.create(name='Category 1', type='expense')

    self.merchant = Merchant.objects.create(
      merchant_name='Merchant 1',
      merchant_logo='https://www.google.com',
      category_id=self.category,
    )

  def test_create_merchant(self):
    """ Test para crear un nuevo comercio """

    # Crear una categoría para usar su ID
    category = Category.objects.create(name='Category 1', type='expense')

    url = reverse('merchants:merchants')
    data = {
      'merchant_name': "New Merchant",
      'merchant_logo': "https://www.google.com",
      'category_id': str(category.id), 
    }
    response = self.client.post(url, json.dumps(data), content_type='application/json')
    self.assertEqual(response.status_code, 201)

    # Verificar que la respuesta incluye un UUID válido para 'id'
    response_data = json.loads(response.content)
    self.assertTrue(uuid.UUID(response_data['id']))

    # Verificar que los datos del comercio creado son correctos
    self.assertEqual(response_data['merchant_name'], 'New Merchant')
    self.assertEqual(response_data['merchant_logo'], "https://www.google.com")
    self.assertEqual(response_data['category_id'], str(category.id))
  
  def test_list_merchants(self):
    """ Test para listar comercios """

    # Crear una categoría para los comercios
    category = Category.objects.create(name='Category 1', type='expense')

    # Crear algunos comercios de prueba
    Merchant.objects.create(
      merchant_name='Merchant 1',
      merchant_logo='https://www.google.com',
      category_id=category,
    )
    Merchant.objects.create(
      merchant_name='Merchant 2',
      merchant_logo='https://www.google.com',
      category_id=category,
    )

    # Obtener la lista de comercios
    url = reverse('merchants:merchants')
    response = self.client.get(url)

    # Verificar que la respuesta tenga el código de estado 200
    self.assertEqual(response.status_code, 200)

    # Verificar que se devuelva una lista de comercios en la respuesta
    response_data = json.loads(response.content)
    self.assertIsInstance(response_data, list)
    self.assertEqual(len(response_data), 3)

  def test_delete_merchant(self):
    # Crear una categoría para los comercios
    category = Category.objects.create(name='Category 1', type='expense')

    # Crear algunos comercios de prueba
    merchant = Merchant.objects.create(
      merchant_name='Merchant 1',
      merchant_logo='https://www.google.com',
      category_id=category,
    )

    # Get the URL for deleting the merchant
    url = reverse('merchants:merchant_detail', args=[merchant.id])

    # Send a DELETE request
    response = self.client.delete(url)

    # Verify that the merchant is deleted and the response status is 204 (No Content)
    self.assertEqual(response.status_code, 204)
    self.assertFalse(Merchant.objects.filter(id=merchant.id).exists())

  def test_update_merchant_by_id(self):
    """ Test to update a merchant by its ID """
    url = reverse('merchants:merchant_detail', kwargs={'id': str(self.merchant.id)})
    data = {
      'merchant_name': 'Updated Merchant',
      'merchant_logo': 'https://www.google.com',
      'category_id': str(self.category.id),
    }
    response = self.client.put(url, json.dumps(data), content_type='application/json')
    self.assertEqual(response.status_code, 204)

    # Verify that the merchant has been updated
    updated_merchant = Merchant.objects.get(id=self.merchant.id)
    self.assertEqual(updated_merchant.merchant_name, data['merchant_name'])
    self.assertEqual(updated_merchant.merchant_logo, data['merchant_logo'])
    self.assertEqual(str(updated_merchant.category_id.id), data['category_id'])

  def test_retrieve_merchant_by_id(self):
    """ Test to retrieve a merchant by its ID """
    url = reverse('merchants:merchant_detail', kwargs={'id': str(self.merchant.id)})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

    # Verify the response data matches the merchant
    response_data = json.loads(response.content)
    self.assertEqual(response_data['id'], str(self.merchant.id))
    self.assertEqual(response_data['merchant_name'], self.merchant.merchant_name)
    self.assertEqual(response_data['merchant_logo'], self.merchant.merchant_logo)
    self.assertEqual(response_data['category_id'], str(self.merchant.category_id.id))

