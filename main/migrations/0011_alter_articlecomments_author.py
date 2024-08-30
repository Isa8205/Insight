# Generated by Django 5.0.6 on 2024-08-22 20:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_articlecomments_articledislikes_articlesaves_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlecomments',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
