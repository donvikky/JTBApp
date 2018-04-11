# Generated by Django 2.0.2 on 2018-04-10 23:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0005_auto_20180410_2114'),
    ]

    operations = [
        migrations.CreateModel(
            name='CorporateShareholder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Registration Name')),
                ('address', models.TextField()),
                ('trade_name', models.CharField(max_length=150, verbose_name='Trade Name')),
                ('phone', models.CharField(max_length=15, verbose_name='Phone')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('tin', models.CharField(blank=True, max_length=10, null=True, verbose_name='JTB TIN')),
                ('reg_status', models.CharField(choices=[('Registered', 'Registered'), ('Unregistered', 'Unregistered')], max_length=20, verbose_name='Registration Status')),
                ('bvn', models.BigIntegerField()),
                ('status', models.CharField(choices=[('Appointed', 'Appointed'), ('Reappointed', 'Re-appointed'), ('Resigned', 'Resigned'), ('Removed', 'Removed')], max_length=20, verbose_name='Status')),
                ('share', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corporate_shareholder_creater', to=settings.AUTH_USER_MODEL)),
                ('update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='corporate_shareholder_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Corporate Shareholder',
            },
        ),
        migrations.CreateModel(
            name='IndividualShareholder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=75, verbose_name='Surname')),
                ('first_name', models.CharField(max_length=75, verbose_name='First Name')),
                ('other_name', models.CharField(max_length=75, null=True, verbose_name='Other Name')),
                ('residential_address', models.TextField()),
                ('phone', models.CharField(max_length=15, verbose_name='Phone')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('position', models.CharField(blank=True, max_length=250, null=True, verbose_name='Position')),
                ('bvn', models.BigIntegerField()),
                ('status', models.CharField(choices=[('Appointed', 'Appointed'), ('Reappointed', 'Re-appointed'), ('Resigned', 'Resigned'), ('Removed', 'Removed')], max_length=20, verbose_name='Status')),
                ('share', models.IntegerField()),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('create_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='individual_shareholder_creater', to=settings.AUTH_USER_MODEL)),
                ('nationality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='individual_shareholder_nationality', to='dashboard.Country')),
                ('update_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='individual_shareholder_updater', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Individual Shareholder',
            },
        ),
    ]
