# Generated by Django 4.0.4 on 2022-11-08 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upload', '0002_bin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bin',
            name='file',
            field=models.FileField(upload_to='documents/'),
        ),
    ]
