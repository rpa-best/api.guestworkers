# Generated by Django 4.1 on 2024-01-18 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_alter_usertoorganization_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='bik',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='ВИК'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='kpp',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='КПП'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='ogrn',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='ОГРН'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон'),
        ),
    ]
