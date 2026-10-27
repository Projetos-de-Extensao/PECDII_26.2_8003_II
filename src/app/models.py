from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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

    aluno = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE, null=True, blank=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    data_aplicacao = models.DateField()
    turno = models.CharField(max_length=1, choices=TURNOS)

    def alunos_ids(self):
        if self.aluno_id:
            return {self.aluno_id}
        if self.turma_id:
            return set(self.turma.alunos.values_list('id', flat=True))
        return set()

    def clean(self):
        if bool(self.aluno_id) == bool(self.turma_id):
            raise ValidationError("Informe um aluno ou uma turma (apenas um dos dois).")

        if not self.sala_id or not self.data_aplicacao or not self.turno:
            return

        alunos = self.alunos_ids()

        mesmo_horario = AlocacaoSala.objects.filter(
            data_aplicacao=self.data_aplicacao,
            turno=self.turno,
        ).exclude(pk=self.pk)

        ocupadas = sum(len(a.alunos_ids()) for a in mesmo_horario.filter(sala=self.sala))

        if ocupadas + len(alunos) > self.sala.capacidade:
            if self.aluno_id:
                raise ValidationError("Esta sala já está cheia nesse dia e turno.")
            raise ValidationError("Esta sala não comporta todos os alunos da turma nesse dia e turno.")

        for outra in mesmo_horario:
            if alunos & outra.alunos_ids():
                if self.aluno_id:
                    raise ValidationError("Este aluno já tem uma sala nesse dia e turno.")
                raise ValidationError("Algum aluno desta turma já tem uma sala nesse dia e turno.")

    def __str__(self):
        return f"{self.aluno or self.turma} - {self.sala} ({self.data_aplicacao})"

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    alunos = models.ManyToManyField(User, related_name='cursos', blank=True)

    def __str__(self):
        return self.nome

class Turma(models.Model):
    numero = models.IntegerField()
    materia = models.CharField(max_length=100, blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='turmas')
    alunos = models.ManyToManyField(User, related_name='turmas', blank=True)

    def __str__(self):
        return f"Turma {self.numero} - {self.curso}"