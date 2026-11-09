from django.contrib import admin
from .models import Unidade, Sala, AlocacaoSala, Curso, Turma, Perfil, Aluno, Professor

# Register your models here.
admin.site.register(Unidade)
admin.site.register(Sala)
admin.site.register(AlocacaoSala)
admin.site.register(Curso)
admin.site.register(Turma)
admin.site.register(Perfil)
admin.site.register(Aluno)
admin.site.register(Professor)