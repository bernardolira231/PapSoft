# Generated by Django 4.1.5 on 2023-05-02 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NetworkDiscover', '0002_device_neighbors'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='neighbors2',
            field=models.ManyToManyField(to='NetworkDiscover.device'),
        ),
        migrations.AddField(
            model_name='device',
            name='neighbors3',
            field=models.ManyToManyField(to='NetworkDiscover.device'),
        ),
        migrations.AddField(
            model_name='device',
            name='neighbors4',
            field=models.ManyToManyField(to='NetworkDiscover.device'),
        ),
    ]
