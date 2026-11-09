from django.contrib import admin
from .models import (
    Unidade, Sala, AlocacaoSala, Curso, Turma, Perfil, Aluno, Professor,
    TesteProgresso, Inscricao, ResultadoTesteProgresso,
)

# Register your models here.
admin.site.register(Unidade)
admin.site.register(Sala)
admin.site.register(AlocacaoSala)
admin.site.register(Curso)
admin.site.register(Turma)
admin.site.register(Perfil)
admin.site.register(Aluno)
admin.site.register(Professor)


@admin.register(TesteProgresso)
class TesteProgressoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'data', 'status')

    def get_queryset(self, request):
        TesteProgresso.finalizar_vencidos()
        return super().get_queryset(request)

admin.site.register(Inscricao)
admin.site.register(ResultadoTesteProgresso)
