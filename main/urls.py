from django.urls import path
from . import views

urlpatterns = [
    path('api/shipments/', views.shipment_list_create),
]