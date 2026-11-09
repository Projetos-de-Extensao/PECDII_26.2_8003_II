from django.db import models

from django.contrib.auth.models import User

from django.core.exceptions import ValidationError

from django.core.validators import MinValueValidator, RegexValidator

from django.utils import timezone


class Unidade(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    endereco = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nome


class Sala(models.Model):
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, related_name='salas')
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

    inscricao = models.ForeignKey('Inscricao', on_delete=models.CASCADE, null=True, blank=True)
    turma = models.ForeignKey('Turma', on_delete=models.CASCADE, null=True, blank=True)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE)
    data_aplicacao = models.DateField()
    turno = models.CharField(max_length=1, choices=TURNOS)

    def alunos_ids(self):
        if self.inscricao_id:
            return {self.inscricao.aluno.perfil.user_id}
        if self.turma_id:
            return set(self.turma.alunos.values_list('id', flat=True))
        return set()

    def clean(self):
        if bool(self.inscricao_id) == bool(self.turma_id):
            raise ValidationError("Informe uma inscrição ou uma turma (apenas um dos dois).")

        if not self.sala_id or not self.data_aplicacao or not self.turno:
            return

        alunos = self.alunos_ids()
        mesmo_horario = AlocacaoSala.objects.filter(
            data_aplicacao=self.data_aplicacao,
            turno=self.turno,
        ).exclude(pk=self.pk)

        ocupadas = sum(len(a.alunos_ids()) for a in mesmo_horario.filter(sala=self.sala))
        if ocupadas + len(alunos) > self.sala.capacidade:
            if self.inscricao_id:
                raise ValidationError("Esta sala já está cheia nesse dia e turno.")
            raise ValidationError("Esta sala não comporta todos os alunos da turma nesse dia e turno.")

        for outra in mesmo_horario:
            if alunos & outra.alunos_ids():
                if self.inscricao_id:
                    raise ValidationError("Este aluno já tem uma sala nesse dia e turno.")
                raise ValidationError("Algum aluno desta turma já tem uma sala nesse dia e turno.")

    def __str__(self):
        return f"{self.inscricao or self.turma} - {self.sala} ({self.data_aplicacao})"


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    unidade = models.ForeignKey(Unidade, on_delete=models.PROTECT, null=True, blank=True, related_name='cursos')
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

class Perfil(models.Model):
    TIPOS = [
        ('A', 'Aluno'),
        ('P', 'Professor'),
        ('C', 'Coordenação'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPOS)
    telefone = models.CharField(max_length=20, blank=True)

    class Meta:
        verbose_name_plural = "Perfis"

    def __str__(self):
        return f"{self.user.username} ({self.get_tipo_display()})"

class Aluno(models.Model):
    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    numero_matricula = models.CharField(
        max_length=12,
        unique=True,
        validators=[RegexValidator(r'^\d{12}$', 'A matrícula deve ter exatamente 12 dígitos numéricos.')],
    )
    curso = models.ForeignKey('Curso', on_delete=models.PROTECT)
    periodo = models.IntegerField(default=1)

    def clean(self):
        if self.perfil_id and self.perfil.tipo != 'A':
            raise ValidationError("O perfil escolhido não é do tipo Aluno.")

    def __str__(self):
        return f"{self.perfil.user.username} - {self.numero_matricula}"

class Professor(models.Model):
    TITULACOES = [
        ('G', 'Graduação'),
        ('E', 'Especialização'),
        ('M', 'Mestrado'),
        ('D', 'Doutorado'),
    ]

    perfil = models.OneToOneField(Perfil, on_delete=models.CASCADE)
    titulacao = models.CharField(max_length=1, choices=TITULACOES)
    area_atuacao = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = "Professores"

    def clean(self):
        if self.perfil_id and self.perfil.tipo != 'P':
            raise ValidationError("O perfil escolhido não é do tipo Professor.")

    def __str__(self):
        return f"{self.perfil.user.username} ({self.get_titulacao_display()})"


class TesteProgresso(models.Model):
    STATUS = [
        ('P', 'Planejado'),
        ('A', 'Inscrições abertas'),
        ('F', 'Finalizado'),
        ('C', 'Cancelado'),
    ]

    data = models.DateField()
    descricao = models.TextField(blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default='P')

    class Meta:
        verbose_name_plural = "Testes de Progresso"

    @classmethod
    def finalizar_vencidos(cls):
        return cls.objects.filter(
            status__in=['P', 'A'], data__lt=timezone.localdate(),
        ).update(status='F')

    def atualizar_status(self):
        if self.status in ('P', 'A') and self.data < timezone.localdate():
            self.status = 'F'
            self.save(update_fields=['status'])

    def __str__(self):
        return f"Teste de Progresso {self.data}"


class Inscricao(models.Model):
    teste = models.ForeignKey(TesteProgresso, on_delete=models.CASCADE, related_name='inscricoes')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='inscricoes')

    class Meta:
        verbose_name = "Inscrição"
        verbose_name_plural = "Inscrições"
        constraints = [
            models.UniqueConstraint(fields=['teste', 'aluno'], name='inscricao_unica_por_teste'),
        ]

    def clean(self):
        if not self.teste_id:
            return

        self.teste.atualizar_status()
        inalterada = self.pk and Inscricao.objects.filter(pk=self.pk, teste_id=self.teste_id).exists()
        if not inalterada and self.teste.status != 'A':
            raise ValidationError("Este teste não está com as inscrições abertas.")

    def __str__(self):
        return f"{self.aluno} - {self.teste}"


class ResultadoTesteProgresso(models.Model):
    inscricao = models.OneToOneField(Inscricao, on_delete=models.CASCADE, related_name='resultado')
    nota = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])

    class Meta:
        verbose_name = "Resultado do Teste de Progresso"
        verbose_name_plural = "Resultados do Teste de Progresso"

    def clean(self):
        if not self.inscricao_id:
            return

        teste = self.inscricao.teste
        teste.atualizar_status()
        if teste.status != 'F':
            raise ValidationError("O resultado só pode ser lançado depois que o teste for finalizado.")

    def __str__(self):
        return f"{self.inscricao}: {self.nota}"
