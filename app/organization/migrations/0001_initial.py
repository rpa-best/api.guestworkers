# Generated by Django 4.1 on 2024-01-18 08:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('name', models.CharField(blank=True, max_length=255, verbose_name='Название')),
                ('inn', models.CharField(max_length=20, primary_key=True, serialize=False, validators=[django.core.validators.MinLengthValidator(8, 'Неправильный ИНН'), django.core.validators.MaxLengthValidator(10, 'Неправильный ИНН')], verbose_name='ИНН')),
                ('bik', models.CharField(blank=True, max_length=255, verbose_name='ВИК')),
                ('address', models.CharField(blank=True, max_length=255, verbose_name='Адрес')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Телефон')),
                ('ogrn', models.CharField(blank=True, max_length=20, verbose_name='ОГРН')),
                ('kpp', models.CharField(blank=True, max_length=20, verbose_name='КПП')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.CreateModel(
            name='UserToOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('checking', 'Checking'), ('done', 'Done'), (None, 'Nothing')], max_length=20, null=True)),
                ('role', models.CharField(choices=[('owner', 'Owner'), ('client', 'Client'), ('worker', 'Worker')], default='worker', max_length=20)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('org', 'user')},
            },
        ),
    ]
