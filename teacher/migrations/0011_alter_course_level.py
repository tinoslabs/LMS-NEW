# Generated by Django 5.1.6 on 2025-04-09 09:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0010_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='teacher.levels'),
        ),
    ]
