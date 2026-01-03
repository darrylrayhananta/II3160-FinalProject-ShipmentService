from .models import Shipment

class ShipmentRepository:
    @staticmethod
    def create_shipment(data):
        return Shipment.objects.create(**data)

    @staticmethod
    def get_all_shipments():
        return Shipment.objects.all().order_by('-created_at')

    @staticmethod
    def get_by_tracking(tracking_number):
        return Shipment.objects.filter(tracking_number=tracking_number).first()
    
    @staticmethod
    def get_shipment_by_id(shipment_id):
        return Shipment.objects.filter(id=shipment_id).first()

    @staticmethod
    def update_location(shipment_id, new_location):
        shipment = Shipment.objects.filter(id=shipment_id).first()
        if shipment:
            shipment.current_location = new_location
            shipment.save()
        return shipment