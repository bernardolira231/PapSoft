# Generated by Django 4.1.5 on 2023-01-12 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('device_id', models.AutoField(primary_key=True, serialize=False)),
                ('device_name', models.CharField(max_length=100)),
                ('device_type', models.CharField(max_length=100)),
                ('device_ip', models.CharField(max_length=100)),
                ('device_username', models.CharField(max_length=100)),
                ('device_password', models.CharField(max_length=100)),
            ],
        ),
    ]
