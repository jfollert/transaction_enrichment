from django.db import models
from django.utils import timezone
import uuid

class Category(models.Model):
  EXPENSE = 'expense'
  INCOME = 'income'
    
  TYPE_CHOICES = [
    (EXPENSE, 'Expense'),
    (INCOME, 'Income'),
  ]
  
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(max_length=255)
  type = models.CharField(max_length=50, choices=TYPE_CHOICES)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.name
