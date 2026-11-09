from rest_framework import viewsets
from .models import (
    Sala, AlocacaoSala, Curso, Turma, Perfil, Aluno, Professor,
    TesteProgresso, Inscricao, ResultadoTesteProgresso,
)
from .serializers import (
    SalaSerializer, AlocacaoSalaSerializer, CursoSerializer, TurmaSerializer,
    PerfilSerializer, AlunoSerializer, ProfessorSerializer,
    TesteProgressoSerializer, InscricaoSerializer, ResultadoTesteProgressoSerializer,
)


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

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer


class TesteProgressoViewSet(viewsets.ModelViewSet):
    queryset = TesteProgresso.objects.all()
    serializer_class = TesteProgressoSerializer

    def get_queryset(self):
        TesteProgresso.finalizar_vencidos()
        return super().get_queryset()


class InscricaoViewSet(viewsets.ModelViewSet):
    queryset = Inscricao.objects.all()
    serializer_class = InscricaoSerializer


class ResultadoTesteProgressoViewSet(viewsets.ModelViewSet):
    queryset = ResultadoTesteProgresso.objects.all()
    serializer_class = ResultadoTesteProgressoSerializer