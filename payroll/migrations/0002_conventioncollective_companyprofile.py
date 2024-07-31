# Generated by Django 5.0.7 on 2024-07-30 23:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConventionCollective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_entreprise', models.CharField(blank=True, max_length=100)),
                ('pays', models.CharField(blank=True, max_length=100)),
                ('ville', models.CharField(blank=True, max_length=100)),
                ('addresse', models.TextField(blank=True)),
                ('code_postal', models.CharField(blank=True, max_length=20)),
                ('code_dexploitation', models.CharField(blank=True, max_length=50)),
                ('cnss', models.CharField(blank=True, max_length=50)),
                ('matricule_fiscale', models.CharField(blank=True, max_length=50)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='company_logos/')),
                ('registration_complete', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_profile', to=settings.AUTH_USER_MODEL)),
                ('convention_collective', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payroll.conventioncollective')),
            ],
        ),
    ]
