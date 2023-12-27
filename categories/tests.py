from django.test import TestCase
from django.urls import reverse
from categories.models import Category
import json
import uuid

class CategoryAPITestCase(TestCase):
  def setUp(self):
    self.category = Category.objects.create(name='Category 1', type='expense')

  def test_create_category(self):
    """ Test para crear una nueva categoría """
    url = reverse('categories:categories')
    data = {'name': 'New Category', 'type': 'expense'}
    response = self.client.post(url, json.dumps(data), content_type='application/json')
    self.assertEqual(response.status_code, 201)

    # Verificar que la respuesta incluye un UUID válido para 'id'
    response_data = json.loads(response.content)
    self.assertTrue(uuid.UUID(response_data['id']))

    # Verificar que los datos de la categoría creada son correctos
    self.assertEqual(response_data['name'], 'New Category')
    self.assertEqual(response_data['type'], 'expense')
  
  def test_list_categories(self):
    """ Test para listar categorías """
    # Crear algunas categorías de prueba
    Category.objects.create(name='Category 1', type='expense')
    Category.objects.create(name='Category 2', type='income')

    # Obtener la lista de categorías
    url = reverse('categories:categories')
    response = self.client.get(url)

    # Verificar que la respuesta tenga el código de estado 200
    self.assertEqual(response.status_code, 200)

    # Verificar que se devuelva una lista de categorías en la respuesta
    response_data = json.loads(response.content)
    self.assertIsInstance(response_data, list)
    self.assertEqual(len(response_data), 3)

  def test_delete_category(self):
    # Create a category for testing
    category = Category.objects.create(name='Test Category', type='expense')

    # Get the URL for deleting the category
    url = reverse('categories:category_detail', args=[category.id])

    # Send a DELETE request
    response = self.client.delete(url)

    # Verify that the category is deleted and the response status is 204 (No Content)
    self.assertEqual(response.status_code, 204)
    self.assertFalse(Category.objects.filter(id=category.id).exists())

  def test_update_category_by_id(self):
    """ Test to update a category by its ID """
    url = reverse('categories:category_detail', kwargs={'id': str(self.category.id)})
    data = {'name': 'Updated Category', 'type': 'income'}
    response = self.client.put(url, json.dumps(data), content_type='application/json')
    self.assertEqual(response.status_code, 204)

    # Verify that the category has been updated
    updated_category = Category.objects.get(id=self.category.id)
    self.assertEqual(updated_category.name, 'Updated Category')
    self.assertEqual(updated_category.type, 'income')

  def test_retrieve_category_by_id(self):
    """ Test to retrieve a category by its ID """
    url = reverse('categories:category_detail', kwargs={'id': str(self.category.id)})
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)

    # Verify the response data matches the category
    response_data = json.loads(response.content)
    self.assertEqual(response_data['id'], str(self.category.id))
    self.assertEqual(response_data['name'], self.category.name)
    self.assertEqual(response_data['type'], self.category.type)
