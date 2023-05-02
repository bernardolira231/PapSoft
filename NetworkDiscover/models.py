from django.db import models

# Create your models here.


class Device(models.Model):
    device_id = models.AutoField(primary_key=True)
    device_name = models.CharField(max_length=100)
    device_type = models.CharField(max_length=100)
    device_ip = models.CharField(max_length=100)
    device_username = models.CharField(max_length=100)
    device_password = models.CharField(max_length=100)
    neighbors = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.device_name + ' - ' + self.device_ip
