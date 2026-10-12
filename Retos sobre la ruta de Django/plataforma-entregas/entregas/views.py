import socket
import uuid

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Pedido
from .reglas import elegir_medio

COPIA = socket.gethostname()

pedidos_en_memoria = {}


def hola(request):
    return HttpResponse("Hola. Plataforma de entregas (aún sin pedidos).")


def estado(request):
    return JsonResponse({
        "servicio": "entregas",
        "version": 1,
        "medios_disponibles": ["camioneta", "moto", "bicicleta", "dron"],
        "atendido_por": COPIA,
    })


def nuevo_folio():
    return uuid.uuid4().hex[:8].upper()


@csrf_exempt
@require_POST
def registrar_pedido(request):
    pedido = Pedido.objects.create(
        folio=nuevo_folio(),
        destino=request.POST.get("destino", "sin destino"),
    )
    return JsonResponse({"folio": pedido.folio, "registrado_por": COPIA}, status=201)


@require_GET
def seguimiento(request, folio):
    pedido = Pedido.objects.filter(folio=folio).first()
    if pedido is None:
        return JsonResponse({"error": "pedido no encontrado", "atendido_por": COPIA}, status=404)
    return JsonResponse({
        "folio": pedido.folio,
        "destino": pedido.destino,
        "estado": pedido.estado,
        "atendido_por": COPIA,
    })


@csrf_exempt
@require_POST
def registrar_pedido_mal(request):
    folio = nuevo_folio()
    pedidos_en_memoria[folio] = {
        "destino": request.POST.get("destino", "sin destino"),
        "estado": "registrado",
    }
    return JsonResponse({"folio": folio, "registrado_por": COPIA}, status=201)


@require_GET
def seguimiento_mal(request, folio):
    pedido = pedidos_en_memoria.get(folio)
    if pedido is None:
        return JsonResponse({"error": "pedido no encontrado", "atendido_por": COPIA}, status=404)
    return JsonResponse({"folio": folio, **pedido, "atendido_por": COPIA})


def cotizar(request):
    # 1. Leer los datos de la petición (que llegan como texto)
    km_str = request.GET.get("km")
    kg_str = request.GET.get("kg")

    # 2. Validar que no falten y que sean números positivos
    if km_str is None or kg_str is None:
        return JsonResponse({"error": "Faltan los parámetros 'km' y/o 'kg'"}, status=400)

    try:
        km = float(km_str)
        kg = float(kg_str)
        if km < 0 or kg < 0:
            raise ValueError
    except ValueError:
        return JsonResponse({"error": "Los parámetros deben ser números positivos válidos"}, status=400)

    # 3. Llamar a la regla de negocio
    resultado = elegir_medio(km, kg)

    # 4. Devolver la respuesta en JSON
    return JsonResponse({
        "km": km,
        "kg": kg,
        "medio": resultado["medio"],
        "motivo": resultado["motivo"]
    })
