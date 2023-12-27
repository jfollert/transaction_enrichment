from django.test import TestCase
from django.urls import reverse
from categories.models import Category
import json
import uuid

class CategoryAPITestCase(TestCase):
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
    self.assertEqual(len(response_data), 2)
