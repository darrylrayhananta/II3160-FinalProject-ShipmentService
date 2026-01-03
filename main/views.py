import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import ShippingService

service = ShippingService()

@csrf_exempt
def shipment_list_create(request):
    if request.method == 'GET':
        shipments = service.repo.get_all_shipments()
        return JsonResponse(list(shipments.values()), safe=False)

    elif request.method == 'POST':
        body = json.loads(request.body)
        result = service.initiate_shipment(
            package_id=body.get('package_id'),
            courier_name=body.get('courier_name')
        )
        
        if isinstance(result, dict) and "error" in result:
            return JsonResponse(result, status=400)
            
        return JsonResponse({
            "message": "Shipment Created",
            "tracking_number": result.tracking_number,
            "status": result.status
        }, status=201)