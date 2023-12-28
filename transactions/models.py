from django.db import models
from categories.models import Category
from merchants.models import Merchant
import uuid

import uuid

class Transaction(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  description = models.CharField(max_length=255)
  amount = models.DecimalField(max_digits=10, decimal_places=2)
  date = models.DateField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
  merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, null=True)

  def __str__(self):
    return self.description
