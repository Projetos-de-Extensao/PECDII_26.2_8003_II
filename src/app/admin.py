from django.contrib import admin
from .models import Unidade, Sala, AlocacaoSala, Curso, Turma

# Register your models here.
admin.site.register(Unidade)
admin.site.register(Sala)
admin.site.register(AlocacaoSala)
admin.site.register(Curso)
admin.site.register(Turma)
