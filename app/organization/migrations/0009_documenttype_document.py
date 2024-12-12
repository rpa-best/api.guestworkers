# Generated by Django 4.1 on 2024-12-12 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_organizationtabel'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('file', models.FileField(upload_to='doc/')),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.organization')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organization.documenttype')),
            ],
        ),
    ]
