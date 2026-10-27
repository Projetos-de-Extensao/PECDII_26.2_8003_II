# app/serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Sala, AlocacaoSala, Curso, Turma


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'unidade', 'nome', 'capacidade', 'ativa']


class AlocacaoSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlocacaoSala
        fields = ['id', 'aluno', 'turma', 'sala', 'data_aplicacao', 'turno']

    def validate(self, dados):
        # reaproveita as regras que já escrevemos no clean() do model
        if self.instance:
            atuais = {c: getattr(self.instance, c) for c in self.Meta.fields if c != 'id'}
            atuais.update(dados)
            dados = atuais
        alocacao = AlocacaoSala(**dados)
        if self.instance:
            alocacao.pk = self.instance.pk
        try:
            alocacao.clean()
        except DjangoValidationError as erro:
            raise serializers.ValidationError(erro.messages)
        return dados


class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = ['id', 'nome', 'alunos']


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ['id', 'numero', 'materia', 'curso', 'alunos']