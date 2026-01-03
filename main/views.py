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
        
@csrf_exempt
def shipment_detail(request, pk):
    if request.method == 'GET':
        shipment = service.repo.get_shipment_by_id(pk)
        if shipment:
            return JsonResponse({
                "tracking_number": shipment.tracking_number,
                "courier": shipment.courier_name,
                "current_location": shipment.current_location,
                "status": shipment.status,
                "last_update": shipment.updated_at
            })
        return JsonResponse({"error": "Resi tidak ditemukan"}, status=404)

    elif request.method == 'PATCH':
        body = json.loads(request.body)
        new_location = body.get('location')
        updated = service.repo.update_location(pk, new_location)
        if updated:
            return JsonResponse({
                "message": "Lokasi diperbarui",
                "new_location": updated.current_location
            })
        return JsonResponse({"error": "Gagal update"}, status=404)