# Generated by Django 4.1.7 on 2023-06-11 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, choices=[('Fruits', 'Fruits'), ('Vegetables', 'Vegetables'), ('Nigerian', 'Nigerian'), ('French', 'French'), ('Turkish', 'Turkish')], max_length=20, null=True),
        ),
    ]
