# Generated by Django 4.1 on 2024-01-19 05:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0004_alter_user_options_alter_user_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterUniqueTogether(
            name='user',
            unique_together=set(),
        ),
    ]