# Generated by Django 4.1 on 2023-03-17 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_product_image_alter_product_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='../static/images/default-product.png', null=True, upload_to='products/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(choices=[('p', 'published'), ('d', 'draft')], default='d', max_length=1),
        ),
    ]
