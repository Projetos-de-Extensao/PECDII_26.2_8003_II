from django.contrib import admin
from django.utils.html import format_html

# Seções na ordem de cadastro: cada classe depende das anteriores.
# (object_name do modelo, nome exibido, dependências)
SECOES = [
    ('1. Estrutura', [
        ('Unidade', 'Unidades', ''),
        ('Sala', 'Salas', 'Unidade'),
        ('Curso', 'Cursos', 'Unidade (opcional)'),
        ('Turma', 'Turmas', 'Curso'),
    ]),
    ('2. Pessoas', [
        ('User', 'Usuários', ''),
        ('Perfil', 'Perfis', 'Usuário'),
        ('Aluno', 'Alunos', 'Perfil e Curso'),
        ('Professor', 'Professores', 'Perfil'),
    ]),
    ('3. Teste de Progresso', [
        ('TesteProgresso', 'Testes de Progresso', ''),
        ('Inscricao', 'Inscrições', 'Teste com inscrições abertas e Aluno'),
        ('ResultadoTesteProgresso', 'Resultados do Teste de Progresso', 'Inscrição de teste finalizado'),
    ]),
    ('4. Alocações', [
        ('AlocacaoSala', 'Alocações de salas', 'Sala e (Inscrição ou Turma)'),
        ('AlocacaoFiscal', 'Alocações de fiscais', 'Professor e Sala'),
    ]),
    ('5. Notificações', [
        ('Notificacao', 'Notificações', 'Usuário'),
    ]),
    ('Administração do sistema', [
        ('Group', 'Grupos de permissão', ''),
    ]),
]


class TesteProgressoAdminSite(admin.AdminSite):
    site_header = 'Administração do Teste de Progresso'
    site_title = 'Teste de Progresso'
    index_title = 'Cadastre na ordem das seções: cada item depende dos anteriores'

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        if app_label:
            return app_list

        disponiveis = {m['object_name']: m for app in app_list for m in app['models']}
        secoes = []
        for titulo, itens in SECOES:
            modelos = []
            for object_name, nome, dependencia in itens:
                modelo = disponiveis.pop(object_name, None)
                if modelo is None:
                    continue
                modelo = dict(modelo)
                if dependencia:
                    modelo['name'] = format_html(
                        '{} <small style="opacity:.65;font-weight:normal">&larr; {}</small>', nome, dependencia
                    )
                else:
                    modelo['name'] = nome
                modelos.append(modelo)
            if modelos:
                secoes.append(self._secao(titulo, modelos))

        if disponiveis:  # modelos novos ainda fora do mapa nao somem do menu
            secoes.append(self._secao('Outros', sorted(disponiveis.values(), key=lambda m: m['name'])))
        return secoes

    @staticmethod
    def _secao(titulo, modelos):
        return {
            'name': titulo,
            'app_label': titulo.lower().replace(' ', '_').replace('.', ''),
            'app_url': '',
            'has_module_perms': True,
            'models': modelos,
        }
