from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SalaViewSet, AlocacaoSalaViewSet, CursoViewSet, TurmaViewSet, PerfilViewSet, AlunoViewSet, ProfessorViewSet,
    TesteProgressoViewSet, InscricaoViewSet, ResultadoTesteProgressoViewSet,
)

router = DefaultRouter()
router.register('salas', SalaViewSet)
router.register('alocacoes', AlocacaoSalaViewSet)
router.register('cursos', CursoViewSet)
router.register('turmas', TurmaViewSet)
router.register('perfis', PerfilViewSet)
router.register('alunos', AlunoViewSet)
router.register('professores', ProfessorViewSet)
router.register('testes', TesteProgressoViewSet)
router.register('inscricoes', InscricaoViewSet)
router.register('resultados', ResultadoTesteProgressoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
