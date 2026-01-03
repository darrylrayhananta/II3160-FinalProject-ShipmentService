import requests
import uuid
from .repositories import ShipmentRepository

class ShippingService:
    def __init__(self):
        self.repo = ShipmentRepository()
        self.WAREHOUSE_URL = "http://127.0.0.1:8000/api/packages/"

    def initiate_shipment(self, package_id, courier_name): 
        try: 
            response = requests.get(self.WAREHOUSE_URL)
            all_packages = response.json()
             
            package_exists = any(p['id'] == package_id for p in all_packages)
            
            if not package_exists:
                return {"error": "Barang tidak ditemukan di Warehouse!"}
 
            shipment_data = {
                "package_id": package_id,
                "courier_name": courier_name,
                "tracking_number": f"TRX-{uuid.uuid4().hex[:8].upper()}"
            }
            return self.repo.create_shipment(shipment_data)

        except requests.exceptions.ConnectionError:
            return {"error": "Gagal konek ke Warehouse Service (Repo 1 mati?)"}