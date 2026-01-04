import json
import os
import functools
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .services import ShippingService

service = ShippingService()
load_dotenv()
API_TOKEN = os.getenv("WAREHOUSE_API_TOKEN")

def token_required(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header == f"Bearer {API_TOKEN}":
            return view_func(request, *args, **kwargs)
        return JsonResponse({"error": "Unauthorized"}, status=401)
    return wrapper

@csrf_exempt
@token_required
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
@token_required
def shipment_detail(request, pk):
    if request.method == 'GET':
        shipment = service.repo.get_shipment_by_id(pk)
        if shipment:
            return JsonResponse({
                "id": shipment.id,
                "tracking_number": shipment.tracking_number,
                "status": shipment.status,
                "current_location": shipment.current_location,
                "courier": shipment.courier_name
            })
        return JsonResponse({"error": "Not Found"}, status=404)

    elif request.method == 'PATCH':
        body = json.loads(request.body)
        shipment = service.repo.get_shipment_by_id(pk)
        
        if shipment:
            if 'location' in body:
                shipment.current_location = body['location']
            if 'status' in body:
                shipment.status = body['status']
                
            shipment.save()
            return JsonResponse({"message": "Status Updated", "status": shipment.status})
        
        return JsonResponse({"error": "Failed to update"}, status=404)