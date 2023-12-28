# Generated by Django 3.2.23 on 2023-12-27 23:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('merchants', '0002_auto_20231227_1705'),
        ('categories', '0002_alter_category_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='categories.category')),
                ('merchant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='merchants.merchant')),
            ],
        ),
    ]
