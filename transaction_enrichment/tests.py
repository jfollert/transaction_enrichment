from django.test import TestCase

class HealthCheckTestCase(TestCase):
  def test_health_check(self):
    """
    Health check para asegurar que el sistema de pruebas está funcionando.
    """
    self.assertTrue(True)