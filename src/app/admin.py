from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.db.models import Count, OuterRef, Q, Subquery

from .models import (
    Unidade, Sala, AlocacaoSala, Curso, Turma, Perfil, Aluno, Professor,
    TesteProgresso, Inscricao, ResultadoTesteProgresso, AlocacaoFiscal, Notificacao
)

# Ordem de cadastro (cada etapa depende das anteriores):
# 1. Unidade, TesteProgresso   2. Sala, Curso, Perfil   3. Turma, Aluno, Professor
# 4. Inscricao   5. AlocacaoSala, AlocacaoFiscal, ResultadoTesteProgresso   6. Notificacao


# ---------- Inlines: cadastrar a "parte" dentro da tela do "todo" ----------

class PerfilInline(admin.StackedInline):
    model = Perfil
    can_delete = False
    max_num = 1


class SalaInline(admin.TabularInline):
    model = Sala
    extra = 0
    show_change_link = True


class TurmaInline(admin.TabularInline):
    model = Turma
    fields = ('numero', 'materia')
    extra = 0
    show_change_link = True


class AlunoInline(admin.StackedInline):
    model = Aluno
    max_num = 1
    autocomplete_fields = ['curso']


class ProfessorInline(admin.StackedInline):
    model = Professor
    max_num = 1


class InscricaoInline(admin.TabularInline):
    model = Inscricao
    extra = 0
    autocomplete_fields = ['aluno']
    show_change_link = True


class ResultadoInline(admin.StackedInline):
    model = ResultadoTesteProgresso
    max_num = 1


# ---------- Usuário (com o Perfil na mesma tela) ----------

admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [PerfilInline]


# ---------- 1-2. Base e estrutura ----------

@admin.register(Unidade)
class UnidadeAdmin(admin.ModelAdmin):
    list_display = ('nome', 'endereco')
    search_fields = ('nome', 'endereco')
    inlines = [SalaInline]


@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade', 'capacidade', 'qtd_alocacoes', 'ativa')
    list_filter = ('unidade', 'ativa')
    search_fields = ('nome', 'unidade__nome')
    autocomplete_fields = ['unidade']
    list_select_related = ('unidade',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_alocacoes=Count('alocacaosala', distinct=True))

    @admin.display(description='Alocações', ordering='_alocacoes')
    def qtd_alocacoes(self, obj):
        return obj._alocacoes


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'unidade', 'qtd_turmas', 'qtd_alunos')
    list_filter = ('unidade',)
    search_fields = ('nome',)
    autocomplete_fields = ['unidade', 'alunos']
    inlines = [TurmaInline]
    list_select_related = ('unidade',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            _turmas=Count('turmas', distinct=True), _alunos=Count('alunos', distinct=True),
        )

    @admin.display(description='Turmas', ordering='_turmas')
    def qtd_turmas(self, obj):
        return obj._turmas

    @admin.display(description='Alunos', ordering='_alunos')
    def qtd_alunos(self, obj):
        return obj._alunos


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'tipo', 'telefone')
    list_filter = ('tipo',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'telefone')
    autocomplete_fields = ['user']
    inlines = [AlunoInline, ProfessorInline]


# ---------- 3. Turmas e pessoas ----------

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'materia', 'curso', 'qtd_alunos')
    list_filter = ('curso',)
    search_fields = ('numero', 'materia', 'curso__nome')
    autocomplete_fields = ['curso', 'alunos']
    list_select_related = ('curso',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_alunos=Count('alunos', distinct=True))

    @admin.display(description='Alunos', ordering='_alunos')
    def qtd_alunos(self, obj):
        return obj._alunos


@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('numero_matricula', 'perfil', 'curso', 'periodo')
    list_filter = ('curso', 'periodo')
    search_fields = (
        'numero_matricula', 'perfil__user__username',
        'perfil__user__first_name', 'perfil__user__last_name',
    )
    autocomplete_fields = ['perfil', 'curso']


@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('perfil', 'titulacao', 'area_atuacao')
    list_filter = ('titulacao',)
    search_fields = (
        'area_atuacao', 'perfil__user__username',
        'perfil__user__first_name', 'perfil__user__last_name',
    )
    autocomplete_fields = ['perfil']


# ---------- Teste de Progresso, inscrição e resultado ----------

@admin.register(TesteProgresso)
class TesteProgressoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'data', 'status', 'qtd_inscritos')
    list_filter = ('status',)
    search_fields = ('descricao',)
    date_hierarchy = 'data'
    inlines = [InscricaoInline]

    def get_queryset(self, request):
        TesteProgresso.finalizar_vencidos()
        return super().get_queryset(request).annotate(_inscritos=Count('inscricoes', distinct=True))

    @admin.display(description='Inscritos', ordering='_inscritos')
    def qtd_inscritos(self, obj):
        return obj._inscritos


@admin.register(Inscricao)
class InscricaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'teste', 'status_do_teste')
    list_filter = ('teste__status', 'teste')
    search_fields = (
        'aluno__numero_matricula', 'aluno__perfil__user__username',
        'aluno__perfil__user__first_name', 'aluno__perfil__user__last_name',
    )
    autocomplete_fields = ['aluno']
    inlines = [ResultadoInline]
    list_select_related = ('teste', 'aluno__perfil__user')

    def get_form(self, request, obj=None, **kwargs):
        request._obj_atual = obj
        return super().get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'teste':
            # so testes com inscricoes abertas (mais o teste atual, ao editar)
            TesteProgresso.finalizar_vencidos()
            filtro = Q(status='A')
            if getattr(request, '_obj_atual', None) is not None:
                filtro |= Q(pk=request._obj_atual.teste_id)
            kwargs['queryset'] = TesteProgresso.objects.filter(filtro)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    @admin.display(description='Status do teste', ordering='teste__status')
    def status_do_teste(self, obj):
        return obj.teste.get_status_display()


@admin.register(ResultadoTesteProgresso)
class ResultadoTesteProgressoAdmin(admin.ModelAdmin):
    list_display = ('inscricao', 'nota')
    list_filter = ('inscricao__teste',)
    search_fields = (
        'inscricao__aluno__numero_matricula', 'inscricao__aluno__perfil__user__username',
        'inscricao__aluno__perfil__user__first_name', 'inscricao__aluno__perfil__user__last_name',
    )

    def get_form(self, request, obj=None, **kwargs):
        request._obj_atual = obj
        return super().get_form(request, obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'inscricao':
            # so inscricoes de testes finalizados (mais a atual, ao editar)
            TesteProgresso.finalizar_vencidos()
            filtro = Q(teste__status='F')
            if getattr(request, '_obj_atual', None) is not None:
                filtro |= Q(pk=request._obj_atual.inscricao_id)
            kwargs['queryset'] = Inscricao.objects.filter(filtro)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# ---------- 5. Alocações ----------

@admin.register(AlocacaoSala)
class AlocacaoSalaAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'tipo', 'qtd_alunos', 'data_aplicacao', 'turno', 'sala')
    list_filter = ('turno', 'sala__unidade', 'sala')
    search_fields = (
        'sala__nome', 'turma__materia', 'turma__curso__nome',
        'inscricao__aluno__numero_matricula', 'inscricao__aluno__perfil__user__username',
    )
    date_hierarchy = 'data_aplicacao'
    autocomplete_fields = ['inscricao', 'turma', 'sala']
    list_select_related = (
        'sala__unidade', 'turma__curso', 'inscricao__teste', 'inscricao__aluno__perfil__user',
    )

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(_alunos_turma=Count('turma__alunos', distinct=True))

    @admin.display(description='Tipo')
    def tipo(self, obj):
        return 'Inscrição' if obj.inscricao_id else 'Turma'

    @admin.display(description='Alunos', ordering='_alunos_turma')
    def qtd_alunos(self, obj):
        return 1 if obj.inscricao_id else obj._alunos_turma


@admin.register(AlocacaoFiscal)
class AlocacaoFiscalAdmin(admin.ModelAdmin):
    list_display = ('professor', 'sala', 'data_aplicacao', 'turno', 'salas_no_dia')
    list_filter = ('turno', 'sala__unidade', 'sala')
    search_fields = (
        'sala__nome', 'professor__perfil__user__username',
        'professor__perfil__user__first_name', 'professor__perfil__user__last_name',
    )
    date_hierarchy = 'data_aplicacao'
    autocomplete_fields = ['professor', 'sala']
    list_select_related = ('professor__perfil__user', 'sala__unidade')

    def get_queryset(self, request):
        # quantas salas o professor fiscaliza no mesmo dia (todos os turnos)
        no_dia = AlocacaoFiscal.objects.filter(
            professor=OuterRef('professor'), data_aplicacao=OuterRef('data_aplicacao'),
        ).order_by().values('professor').annotate(total=Count('pk')).values('total')
        return super().get_queryset(request).annotate(_salas_no_dia=Subquery(no_dia))

    @admin.display(description='Salas do professor no dia', ordering='_salas_no_dia')
    def salas_no_dia(self, obj):
        return obj._salas_no_dia


# ---------- 6. Notificações ----------

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'destinatario', 'lida', 'criada_em')
    list_filter = ('lida',)
    search_fields = ('titulo', 'mensagem', 'destinatario__username')
    autocomplete_fields = ['destinatario']
