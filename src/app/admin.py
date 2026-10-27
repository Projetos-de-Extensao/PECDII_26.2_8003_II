from django.contrib import admin
from .models import Sala, AlocacaoSala, Curso, Turma

# Register your models here.
admin.site.register(Sala)
admin.site.register(AlocacaoSala)
admin.site.register(Curso)
admin.site.register(Turma)