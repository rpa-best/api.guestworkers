# Generated by Django 4.1 on 2024-09-09 11:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('organization', '0006_organization_has_skud_historicalorganization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorganization',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='gen_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Генеральный директор'),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='has_skud',
            field=models.BooleanField(default=False, verbose_name='СКУД'),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='inn',
            field=models.CharField(db_index=True, max_length=20, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='k_s',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='к/с'),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='phone_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Контактное лицо'),
        ),
        migrations.AlterField(
            model_name='historicalorganization',
            name='r_s',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='р/с'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='gen_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Генеральный директор'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='has_skud',
            field=models.BooleanField(default=False, verbose_name='СКУД'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='inn',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='ИНН'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='k_s',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='к/с'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='phone_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Контактное лицо'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='r_s',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='р/с'),
        ),
        migrations.CreateModel(
            name='OrganizationDoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='orgdocs/')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользовател')),
            ],
            options={
                'verbose_name': 'Ведомость',
                'verbose_name_plural': 'Ведомости',
            },
        ),
    ]
