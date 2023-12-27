from django.test import TestCase
from django.urls import reverse
from keywords.models import Keyword
from categories.models import Category
from merchants.models import Merchant
import json
import uuid

class KeywordAPITestCase(TestCase):
  def setUp(self):
    self.category = Category.objects.create(name='Category 1', type='expense')

    self.merchant = Merchant.objects.create(
      merchant_name='Merchant 1',
      merchant_logo='https://www.google.com',
      category_id=self.category,
    )

    self.keyword = Keyword.objects.create(
      keyword="Keyword 1",
      merchant=self.merchant,
    )

  def test_create_keyword(self):
    """ Test para crear un nuevo keyword """

    url = reverse('keywords:keywords')
    data = {
      'keyword': "New Keyword",
      'merchant_id': str(self.merchant.id), 
    }
    response = self.client.post(url, json.dumps(data), content_type='application/json')
    self.assertEqual(response.status_code, 201)

    # Verificar que la respuesta incluye un UUID válido para 'id'
    response_data = json.loads(response.content)
    self.assertTrue(uuid.UUID(response_data['id']))

    # Verificar que los datos del keyword creado son correctos
    self.assertEqual(response_data['keyword'], data['keyword'])
    self.assertEqual(response_data['merchant_id'], str(self.merchant.id))
  
  def test_list_keywords(self):
    """ Test para listar keywords """

    # Crear algunos keywords de prueba
    Keyword.objects.create(
      keyword="Keyword 1",
      merchant=self.merchant,
    )
    Keyword.objects.create(
      keyword="Keyword 2",
      merchant=self.merchant,
    )

    # Obtener la lista de keywords
    url = reverse('keywords:keywords')
    response = self.client.get(url)

    # Verificar que la respuesta tenga el código de estado 200
    self.assertEqual(response.status_code, 200)

    # Verificar que se devuelva una lista de keywords en la respuesta
    response_data = json.loads(response.content)
    self.assertIsInstance(response_data, list)
    self.assertEqual(len(response_data), 3)

  def test_delete_keyword(self):
    """ Test para eliminar un keyword """

    # Crear algunos keywords de prueba
    keyword = Keyword.objects.create(
      keyword="Keyword 1",
      merchant=self.merchant,
    )

    # Get the URL for deleting the keyword
    url = reverse('keywords:keyword_detail', args=[keyword.id])

    # Send a DELETE request
    response = self.client.delete(url)

    # Verify that the keyword is deleted and the response status is 204 (No Content)
    self.assertEqual(response.status_code, 204)
    self.assertFalse(Keyword.objects.filter(id=keyword.id).exists())

  def test_update_keyword_by_id(self):
    """ Test to update a keyword by its ID """

    url = reverse('keywords:keyword_detail', kwargs={'id': str(self.keyword.id)})
    data = {
      'keyword': "Updated Keyword",
      'merchant_id': str(self.merchant.id),
    }
    response = self.client.put(url, json.dumps(data), content_type='application/json')
    self.assertEqual(response.status_code, 204)

    # Verify that the keyword has been updated
    updated_keyword = Keyword.objects.get(id=self.keyword.id)
    self.assertEqual(updated_keyword.keyword, data['keyword'])
    self.assertEqual(str(updated_keyword.merchant.id), data['merchant_id'])

  def test_retrieve_keyword_by_id(self):
    """ Test to retrieve a keyword by its ID """

    url = reverse('keywords:keyword_detail', kwargs={'id': str(self.keyword.id)})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

    # Verify the response data matches the keyword
    response_data = json.loads(response.content)
    self.assertEqual(response_data['id'], str(self.keyword.id))
    self.assertEqual(response_data['keyword'], self.keyword.keyword)
    self.assertEqual(response_data['merchant_id'], str(self.keyword.merchant.id))

