from django.db import models
from categories.models import Category
from django.utils import timezone

import uuid

class Merchant(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  merchant_name = models.CharField(max_length=255)
  merchant_logo = models.URLField()
  category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.merchant_name
