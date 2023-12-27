from django.db import models
from merchants.models import Merchant
from django.utils import timezone
import uuid

class Keyword(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  keyword = models.CharField(max_length=255)
  merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
  created_at = models.DateTimeField(default=timezone.now)
  updated_at = models.DateTimeField(default=timezone.now)

  def __str__(self):
    return self.keyword
