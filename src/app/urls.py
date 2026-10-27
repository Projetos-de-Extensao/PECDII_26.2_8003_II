from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalaViewSet, AlocacaoSalaViewSet, CursoViewSet, TurmaViewSet

router = DefaultRouter()
router.register('salas', SalaViewSet)
router.register('alocacoes', AlocacaoSalaViewSet)
router.register('cursos', CursoViewSet)
router.register('turmas', TurmaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]