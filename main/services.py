import requests, uuid
from .repositories import ShipmentRepository
import os
from dotenv import load_dotenv

load_dotenv()

class ShippingService:
    def __init__(self):
        self.repo = ShipmentRepository()
        self.WAREHOUSE_URL = os.getenv("WAREHOUSE_URL")
        token = os.getenv("WAREHOUSE_API_TOKEN")
        self.HEADERS = {"Authorization": f"Bearer {token}"}

    def initiate_shipment(self, package_id, courier_name):
        try:
            headers = self.HEADERS
            
            res = requests.get(f"{self.WAREHOUSE_URL}{package_id}/", headers=headers)
            if res.status_code != 200:
                shipment_data = {
                    "package_id": package_id,
                    "courier_name": courier_name,
                    "tracking_number": f"TRX-{uuid.uuid4().hex[:6].upper()}"
                }
                new_shipment = self.repo.create_shipment(shipment_data)
                return new_shipment

            shipment_data = {
                "package_id": package_id,
                "courier_name": courier_name,
                "tracking_number": f"TRX-{uuid.uuid4().hex[:6].upper()}"
            }
            new_shipment = self.repo.create_shipment(shipment_data)

            requests.patch(f"{self.WAREHOUSE_URL}{package_id}/", json={"status": "SHIPPED"}, headers=headers)

            return new_shipment
        except Exception as e:
            return {"error": str(e)}