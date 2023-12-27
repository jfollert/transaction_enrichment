from django.test import TestCase
from django.urls import reverse
import json
import uuid

class HealthCheckTestCase(TestCase):
  def test_health_check(self):
    """
    Health check para asegurar que el sistema de pruebas está funcionando.
    """
    self.assertTrue(True)


class CategoryAPITestCase(TestCase):
    def test_create_category(self):
        """ Test para crear una nueva categoría """
        url = reverse('categories')
        data = {'name': 'New Category', 'type': 'expense'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)

         # Verificar que la respuesta incluye un UUID válido para 'id'
        response_data = json.loads(response.content)
        self.assertTrue(uuid.UUID(response_data['id']))

        # Verificar que los datos de la categoría creada son correctos
        self.assertEqual(response_data['name'], 'New Category')
        self.assertEqual(response_data['type'], 'expense')
