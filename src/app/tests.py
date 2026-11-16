"""Testes das regras de negócio do app.

Rodar (dentro da pasta src, com a .venv ativada):

    python manage.py test

Cada teste usa um banco temporário: o db.sqlite3 não é tocado.
As regras vivem no clean() dos modelos, por isso os testes chamam full_clean().
"""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from .models import (
    Unidade, Sala, Curso, Turma, Perfil, Aluno, Professor,
    TesteProgresso, Inscricao, ResultadoTesteProgresso,
    AlocacaoSala, AlocacaoFiscal,
)


class BaseTestCase(TestCase):
    """Cria o cenário mínimo e alguns atalhos para os testes."""

    @classmethod
    def setUpTestData(cls):
        cls.hoje = timezone.localdate()
        cls.unidade = Unidade.objects.create(nome='Botafogo')
        cls.curso = Curso.objects.create(nome='Direito', unidade=cls.unidade)
        cls.sala = Sala.objects.create(unidade=cls.unidade, nome='201', capacidade=5)
        cls._contador = 0

    @classmethod
    def novo_aluno(cls):
        cls._contador += 1
        user = User.objects.create(username=f'aluno{cls._contador}')
        perfil = Perfil.objects.create(user=user, tipo='A')
        return Aluno.objects.create(
            perfil=perfil, numero_matricula=f'{cls._contador:012d}', curso=cls.curso,
        )

    @classmethod
    def novo_professor(cls):
        cls._contador += 1
        user = User.objects.create(username=f'prof{cls._contador}')
        perfil = Perfil.objects.create(user=user, tipo='P')
        return Professor.objects.create(perfil=perfil, titulacao='M')

    def novo_teste(self, status='A', dias=3):
        return TesteProgresso.objects.create(data=self.hoje + timedelta(days=dias), status=status)

    def inscrever(self, aluno=None, teste=None):
        aluno = aluno or self.novo_aluno()
        teste = teste or self.novo_teste()
        return Inscricao.objects.create(teste=teste, aluno=aluno)

    def turma_com_alunos(self, quantidade, numero=1):
        turma = Turma.objects.create(numero=numero, curso=self.curso)
        turma.alunos.set(self.novo_aluno().perfil.user for _ in range(quantidade))
        return turma

    def alocacao(self, sala=None, turno='M', **kwargs):
        return AlocacaoSala(
            sala=sala or self.sala, data_aplicacao=self.hoje, turno=turno, **kwargs,
        )


class AlocacaoSalaTests(BaseTestCase):
    def test_exige_inscricao_ou_turma(self):
        with self.assertRaises(ValidationError):
            self.alocacao().full_clean()

    def test_nao_aceita_inscricao_e_turma_juntas(self):
        turma = self.turma_com_alunos(1)
        with self.assertRaises(ValidationError):
            self.alocacao(inscricao=self.inscrever(), turma=turma).full_clean()

    def test_aceita_so_inscricao(self):
        self.alocacao(inscricao=self.inscrever()).full_clean()

    def test_aceita_so_turma(self):
        self.alocacao(turma=self.turma_com_alunos(3)).full_clean()

    def test_turma_maior_que_a_capacidade_e_recusada(self):
        turma = self.turma_com_alunos(6)  # a sala comporta 5
        with self.assertRaises(ValidationError):
            self.alocacao(turma=turma).full_clean()

    def test_turma_do_tamanho_da_capacidade_e_aceita(self):
        self.alocacao(turma=self.turma_com_alunos(5)).full_clean()

    def test_sala_cheia_recusa_nova_inscricao(self):
        sala = Sala.objects.create(unidade=self.unidade, nome='pequena', capacidade=1)
        self.alocacao(sala=sala, inscricao=self.inscrever()).save()
        with self.assertRaises(ValidationError):
            self.alocacao(sala=sala, inscricao=self.inscrever()).full_clean()

    def test_capacidade_conta_alunos_de_turma_ja_alocada(self):
        self.alocacao(turma=self.turma_com_alunos(4)).save()
        with self.assertRaises(ValidationError):
            self.alocacao(turma=self.turma_com_alunos(2, numero=2)).full_clean()

    def test_sala_cheia_aceita_outro_turno(self):
        sala = Sala.objects.create(unidade=self.unidade, nome='pequena', capacidade=1)
        self.alocacao(sala=sala, inscricao=self.inscrever()).save()
        self.alocacao(sala=sala, turno='T', inscricao=self.inscrever()).full_clean()

    def test_mesmo_aluno_nao_pode_estar_em_duas_salas_no_mesmo_horario(self):
        outra_sala = Sala.objects.create(unidade=self.unidade, nome='202', capacidade=5)
        inscricao = self.inscrever()
        self.alocacao(inscricao=inscricao).save()
        with self.assertRaises(ValidationError):
            self.alocacao(sala=outra_sala, inscricao=inscricao).full_clean()

    def test_mesmo_aluno_pode_ter_sala_em_outro_turno(self):
        outra_sala = Sala.objects.create(unidade=self.unidade, nome='202', capacidade=5)
        inscricao = self.inscrever()
        self.alocacao(inscricao=inscricao).save()
        self.alocacao(sala=outra_sala, turno='T', inscricao=inscricao).full_clean()

    def test_editar_a_propria_alocacao_nao_conta_como_conflito(self):
        alocacao = self.alocacao(inscricao=self.inscrever())
        alocacao.save()
        alocacao.full_clean()


class InscricaoTests(BaseTestCase):
    def test_aceita_quando_o_teste_esta_com_inscricoes_abertas(self):
        Inscricao(teste=self.novo_teste('A'), aluno=self.novo_aluno()).full_clean()

    def test_recusa_teste_planejado(self):
        with self.assertRaises(ValidationError):
            Inscricao(teste=self.novo_teste('P'), aluno=self.novo_aluno()).full_clean()

    def test_recusa_teste_finalizado(self):
        with self.assertRaises(ValidationError):
            Inscricao(teste=self.novo_teste('F'), aluno=self.novo_aluno()).full_clean()

    def test_recusa_teste_cancelado(self):
        with self.assertRaises(ValidationError):
            Inscricao(teste=self.novo_teste('C'), aluno=self.novo_aluno()).full_clean()

    def test_recusa_teste_aberto_com_data_vencida(self):
        # o status é atualizado antes da checagem: data passou -> já está finalizado
        teste = self.novo_teste('A', dias=-1)
        with self.assertRaises(ValidationError):
            Inscricao(teste=teste, aluno=self.novo_aluno()).full_clean()

    def test_aluno_nao_pode_se_inscrever_duas_vezes_no_mesmo_teste(self):
        aluno, teste = self.novo_aluno(), self.novo_teste('A')
        Inscricao.objects.create(teste=teste, aluno=aluno)
        with self.assertRaises(ValidationError):
            Inscricao(teste=teste, aluno=aluno).full_clean()

    def test_inscricao_existente_continua_valida_depois_que_o_teste_fecha(self):
        inscricao = self.inscrever()
        TesteProgresso.objects.filter(pk=inscricao.teste_id).update(status='F')
        inscricao.refresh_from_db()
        inscricao.full_clean()


class ResultadoTests(BaseTestCase):
    def test_aceita_resultado_de_teste_finalizado(self):
        inscricao = self.inscrever(teste=self.novo_teste('F'))
        ResultadoTesteProgresso(inscricao=inscricao, nota=Decimal('8.5')).full_clean()

    def test_recusa_resultado_de_teste_com_inscricoes_abertas(self):
        inscricao = self.inscrever(teste=self.novo_teste('A'))
        with self.assertRaises(ValidationError):
            ResultadoTesteProgresso(inscricao=inscricao, nota=Decimal('8.5')).full_clean()

    def test_recusa_nota_negativa(self):
        inscricao = self.inscrever(teste=self.novo_teste('F'))
        with self.assertRaises(ValidationError):
            ResultadoTesteProgresso(inscricao=inscricao, nota=Decimal('-1')).full_clean()

    def test_resultado_de_teste_aberto_com_data_vencida_e_aceito(self):
        # a data passou: o teste é finalizado automaticamente e o resultado pode ser lançado
        teste = self.novo_teste('A', dias=-1)
        inscricao = Inscricao.objects.create(teste=teste, aluno=self.novo_aluno())
        ResultadoTesteProgresso(inscricao=inscricao, nota=Decimal('7')).full_clean()
        teste.refresh_from_db()
        self.assertEqual(teste.status, 'F')


class FinalizacaoAutomaticaTests(BaseTestCase):
    def test_finaliza_testes_planejados_e_abertos_com_data_vencida(self):
        planejado = self.novo_teste('P', dias=-1)
        aberto = self.novo_teste('A', dias=-1)
        self.assertEqual(TesteProgresso.finalizar_vencidos(), 2)
        for teste in (planejado, aberto):
            teste.refresh_from_db()
            self.assertEqual(teste.status, 'F')

    def test_nao_finaliza_teste_de_hoje_nem_futuro(self):
        hoje = self.novo_teste('A', dias=0)
        futuro = self.novo_teste('A', dias=5)
        self.assertEqual(TesteProgresso.finalizar_vencidos(), 0)
        for teste in (hoje, futuro):
            teste.refresh_from_db()
            self.assertEqual(teste.status, 'A')

    def test_nao_mexe_em_teste_cancelado(self):
        cancelado = self.novo_teste('C', dias=-1)
        TesteProgresso.finalizar_vencidos()
        cancelado.refresh_from_db()
        self.assertEqual(cancelado.status, 'C')

    def test_atualizar_status_finaliza_a_instancia(self):
        teste = self.novo_teste('A', dias=-1)
        teste.atualizar_status()
        self.assertEqual(teste.status, 'F')


class AlocacaoFiscalTests(BaseTestCase):
    def test_professor_nao_pode_ser_fiscal_de_duas_salas_no_mesmo_horario(self):
        professor = self.novo_professor()
        outra_sala = Sala.objects.create(unidade=self.unidade, nome='202', capacidade=5)
        AlocacaoFiscal.objects.create(professor=professor, sala=self.sala, data_aplicacao=self.hoje, turno='M')
        with self.assertRaises(ValidationError):
            AlocacaoFiscal(
                professor=professor, sala=outra_sala, data_aplicacao=self.hoje, turno='M',
            ).full_clean()

    def test_professor_pode_ser_fiscal_em_outro_turno(self):
        professor = self.novo_professor()
        AlocacaoFiscal.objects.create(professor=professor, sala=self.sala, data_aplicacao=self.hoje, turno='M')
        AlocacaoFiscal(
            professor=professor, sala=self.sala, data_aplicacao=self.hoje, turno='T',
        ).full_clean()


class PerfilTests(BaseTestCase):
    def test_aluno_exige_perfil_do_tipo_aluno(self):
        user = User.objects.create(username='coord')
        perfil = Perfil.objects.create(user=user, tipo='C')
        with self.assertRaises(ValidationError):
            Aluno(perfil=perfil, numero_matricula='999999999999', curso=self.curso).full_clean()

    def test_professor_exige_perfil_do_tipo_professor(self):
        aluno = self.novo_aluno()
        with self.assertRaises(ValidationError):
            Professor(perfil=aluno.perfil, titulacao='M').full_clean()
