# Generated by Django 4.1 on 2023-03-25 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='static/accounts/defult_prof.jpg', upload_to='profiles/'),
        ),
    ]
