# Generated by Django 3.2.18 on 2023-06-20 10:45

import app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_rename_details_details_family'),
    ]

    operations = [
        migrations.AlterField(
            model_name='details',
            name='education',
            field=models.CharField(max_length=100, validators=[app.validators.EducationStages]),
        ),
    ]
