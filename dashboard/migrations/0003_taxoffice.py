# Generated by Django 2.0.2 on 2018-04-09 22:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0002_auto_20180305_0037'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxOffice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Tax Office Name')),
                ('address', models.TextField()),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=20, verbose_name='Status')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taxoffice_creater', to=settings.AUTH_USER_MODEL)),
                ('lga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lga', to='dashboard.Lga')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state', to='dashboard.State')),
                ('update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='taxoffice_updater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
