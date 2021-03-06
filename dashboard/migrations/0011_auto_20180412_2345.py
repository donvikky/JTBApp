# Generated by Django 2.0.2 on 2018-04-12 22:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0010_auto_20180412_2339'),
    ]

    operations = [
        migrations.AddField(
            model_name='biometric',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='biometric',
            name='create_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biometric_creater', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='biometric',
            name='update_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='biometric',
            name='update_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='biometric_updater', to=settings.AUTH_USER_MODEL),
        ),
    ]
