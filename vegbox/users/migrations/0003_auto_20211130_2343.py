# Generated by Django 3.2.9 on 2021-11-30 18:13

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_product'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Profile',
            new_name='Register',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
