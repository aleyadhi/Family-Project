# Generated by Django 3.2.18 on 2023-06-12 14:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_family_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='family',
            name='joined_date',
            field=models.DateField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
