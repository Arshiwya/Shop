# Generated by Django 4.1 on 2023-03-11 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='categories',
            field=models.ManyToManyField(null=True, related_name='products', to='products.category'),
        ),
    ]