# Generated by Django 4.1 on 2024-01-19 04:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0003_user_passport_user_surname_alter_user_phone'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together={('first_name', 'last_name', 'surname')},
        ),
    ]