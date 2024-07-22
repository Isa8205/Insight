# Generated by Django 5.0.6 on 2024-07-07 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_users_alter_comments_options_alter_reviews_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='email',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='profile',
            field=models.FileField(null=True, upload_to='profiles/'),
        ),
    ]
