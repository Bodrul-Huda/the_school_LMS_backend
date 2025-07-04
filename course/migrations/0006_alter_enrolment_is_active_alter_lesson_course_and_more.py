# Generated by Django 5.2.3 on 2025-06-26 17:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_lessonprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolment',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='course.course'),
        ),
        migrations.AlterField(
            model_name='lessonprogress',
            name='is_completed',
            field=models.BooleanField(default=False),
        ),
    ]
