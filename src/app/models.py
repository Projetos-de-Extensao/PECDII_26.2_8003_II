from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=6, decimal_places=2)
    descricao = models.TextField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Sala(models.Model):
    unidade = models.CharField(max_length=100)
    nome = models.CharField(max_length=50)
    capacidade = models.IntegerField()
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nome} - {self.unidade}"

class AlocacaoSala(models.Model):
    TURNOS = [
        ('M', 'Manhã'),
        ('T', 'Tarde'),
        ('N', 'Noite'),
    ]

    aluno = models.ForeignKey(User, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    data_aplicacao = models.DateField()
    turno = models.CharField(max_length=1, choices=TURNOS)

    def clean(self):
        if not self.sala_id or not self.aluno_id or not self.data_aplicacao or not self.turno:
            return

        ocupadas = AlocacaoSala.objects.filter(
            sala=self.sala,
            data_aplicacao=self.data_aplicacao,
            turno=self.turno,
        ).exclude(pk=self.pk).count()

        if ocupadas >= self.sala.capacidade:
            raise ValidationError("Esta sala já está cheia nesse dia e turno.")

        repetido = AlocacaoSala.objects.filter(
            aluno=self.aluno,
            data_aplicacao=self.data_aplicacao,
            turno=self.turno,
        ).exclude(pk=self.pk).exists()

        if repetido:
            raise ValidationError("Este aluno já tem uma sala nesse dia e turno.")

    def __str__(self):
        return f"{self.aluno} - {self.sala} ({self.data_aplicacao})"