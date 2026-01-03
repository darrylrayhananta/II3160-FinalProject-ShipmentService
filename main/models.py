from django.db import models

class Shipment(models.Model):
    package_id = models.IntegerField()
    courier_name = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='IN_TRANSIT')
    current_location = models.CharField(max_length=255, default='Warehouse Origin') 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Biar tau kapan terakhir update lokasinya