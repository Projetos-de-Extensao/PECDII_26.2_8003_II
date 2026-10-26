from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalaViewSet, AlocacaoSalaViewSet

router = DefaultRouter()
router.register('salas', SalaViewSet)
router.register('alocacoes', AlocacaoSalaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]