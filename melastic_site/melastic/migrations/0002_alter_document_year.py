# Generated by Django 4.1 on 2022-08-18 17:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('melastic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='year',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]