from django.urls import path
from . import views

urlpatterns = [
    path("hola/", views.hola, name="hola"),
    path("estado/", views.estado, name="estado"),
    path("pedidos/", views.registrar_pedido, name="registrar_pedido"),
    path("pedidos/<str:folio>/", views.seguimiento, name="seguimiento"),
    path("pedidos-mal/", views.registrar_pedido_mal, name="registrar_pedido_mal"),
    path("pedidos-mal/<str:folio>/", views.seguimiento_mal, name="seguimiento_mal"),
    path("cotizar/", views.cotizar, name="cotizar"),
]
