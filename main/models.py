from django.db import models

class Shipment(models.Model): 
    package_id = models.IntegerField()
    courier_name = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='IN_TRANSIT')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tracking_number} - {self.courier_name}"