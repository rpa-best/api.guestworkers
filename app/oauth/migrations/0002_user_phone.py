# Generated by Django 4.1 on 2024-01-18 08:06

from django.db import migrations, models
import oauth.validators


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, validators=[oauth.validators.validate_phone], verbose_name='Phone'),
        ),
    ]
