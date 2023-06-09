# Generated by Django 4.1.7 on 2023-06-09 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Fruits', 'Fruits'), ('Vegetables', 'Vegetables'), ('Dishes', 'Dishes')], max_length=20, null=True),
        ),
    ]