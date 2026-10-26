from django.contrib import admin
from .models import Produto, Sala, AlocacaoSala

# Register your models here.
admin.site.register(Produto)
admin.site.register(Sala)
admin.site.register(AlocacaoSala)