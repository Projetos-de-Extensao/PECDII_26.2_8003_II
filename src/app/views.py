from rest_framework import viewsets
from .models import Sala, AlocacaoSala, Curso, Turma
from .serializers import SalaSerializer, AlocacaoSalaSerializer, CursoSerializer, TurmaSerializer


class SalaViewSet(viewsets.ModelViewSet):
    queryset = Sala.objects.all()
    serializer_class = SalaSerializer


class AlocacaoSalaViewSet(viewsets.ModelViewSet):
    queryset = AlocacaoSala.objects.all()
    serializer_class = AlocacaoSalaSerializer


class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer


class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer