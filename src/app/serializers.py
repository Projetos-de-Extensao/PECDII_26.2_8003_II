# app/serializers.py
from rest_framework import serializers
from django.core.exceptions import ValidationError as DjangoValidationError
from .models import Sala, AlocacaoSala


class SalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sala
        fields = ['id', 'unidade', 'nome', 'capacidade', 'ativa']


class AlocacaoSalaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlocacaoSala
        fields = ['id', 'aluno', 'sala', 'data_aplicacao', 'turno']

    def validate(self, dados):
        # reaproveita as regras que já escrevemos no clean() do model
        alocacao = AlocacaoSala(**dados)
        if self.instance:
            alocacao.pk = self.instance.pk
        try:
            alocacao.clean()
        except DjangoValidationError as erro:
            raise serializers.ValidationError(erro.messages)
        return dados