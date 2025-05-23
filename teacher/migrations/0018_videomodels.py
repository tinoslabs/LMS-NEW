# Generated by Django 5.1.6 on 2025-04-10 11:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0017_requirements'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoModels',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.IntegerField(null=True)),
                ('thumbnail', models.ImageField(null=True, upload_to='Media/Yt_Thumbnail')),
                ('title', models.CharField(max_length=100)),
                ('video', models.FileField(blank=True, null=True, upload_to='course_videos/')),
                ('time_duration', models.IntegerField(null=True)),
                ('preview', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.course')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.lesson')),
            ],
        ),
    ]
