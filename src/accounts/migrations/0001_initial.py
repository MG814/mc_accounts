# Generated by Django 5.1 on 2025-02-27 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth0_id', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('surname', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15)),
                ('role', models.CharField(choices=[('Patient', 'Patient'), ('Doctor', 'Doctor')], max_length=10)),
                ('specialization', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
