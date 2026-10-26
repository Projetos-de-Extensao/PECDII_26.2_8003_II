from rest_framework import viewsets
from .models import Sala, AlocacaoSala
from .serializers import SalaSerializer, AlocacaoSalaSerializer


class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer


class AlocacaoSalaViewSet(viewsets.ModelViewSet):
    queryset = AlocacaoSala.objects.all()
    serializer_class = AlocacaoSalaSerializer