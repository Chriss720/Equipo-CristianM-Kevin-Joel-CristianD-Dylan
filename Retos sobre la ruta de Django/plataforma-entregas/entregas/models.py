from django.db import models


class Pedido(models.Model):
    folio = models.CharField(max_length=12, unique=True)
    destino = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, default="registrado")
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.folio} → {self.destino}"
