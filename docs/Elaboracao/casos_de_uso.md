---
id: diagrama_de_casos de uso
title: Diagrama de Casos de Uso
---

## Casos de Uso

### Descrição:

- Contas
	- Criação
	- Entrada
	- Alteração
	- Recuperar Senha
	- Exclusão Lógica
	- Visualização

- Perfis
	- Edição
	- Pesquisar
	- Visualização
	- Vínculo do Aluno com Curso e Matérias em curso

- Inscrições (Teste Progresso)
	- Criação (aluno se inscreve e escolhe a matéria do bônus)
	- Alteração (troca da matéria escolhida)
	- Cancelamento
	- Visualização

- Notificações
	- Criação (aviso de sala/horário ao aluno e ao professor fiscal)
	- Visualização

- Cursos, Unidades e Salas
	- Cadastro de Curso e Matérias
	- Cadastro de Unidade e Salas
- Organização
	- Ensalamento dos alunos
	- Associação de professores fiscais às salas

### Criação de uma conta no sistema

* Atores:

	- Usuário
	- Sistema

- Pré-Condições:
	- Nenhuma

* Fluxo Básico:
    1. Usuário fornece e-mail, senha e confirmações
    2. Dados do Usuário são validados pelo Sistema
    3. Dados do Usuário são encriptados pelo Sistema
    4. Dados do Usuário são persistidos pelo Sistema
    5. Sistema gera um link com prazo de expiração
    6. Sistema envia e-mail de verificação, com o link, para o Usuário
    7. Usuário confirma o e-mail antes do link expirar
    8. Sistema confirma que o Cadastro do Usuário foi realizado com sucesso
    9. Sistema redireciona o Usuário para a página de Entrada

- Fluxos Alternativos:
	- 2a. E-mail do Usuário é inválido
		2a1. Sistema exibe mensagem de erro
	- 2b. Senha do Usuário não respeita regras de segurança
		- 2b1. Sistema exibe mensagem de erro
	- 3a. Usuário tenta confirmar o e-mail depois de o link expirar
		- 3a1. Sistema sugere que o Usuário realize um novo Cadastro

### Entrada do usuário no sistema

- Atores:
	- Usuário
	- Sistema

- Pré-Condições:
	Usuário deve estar cadastrado

- Fluxo Básico:
    - 1. Usuário fornece e-mail e senha
	- 2. Sistema autentica o Usuário
	- 3. Sistema redireciona o Usuário para a página inicial

- Fluxos Alternativos:
	- 2a. Dados do Usuário Inválidos
		- 2a1. Sistema exibe mensagem de erro
	- 3a. Primeio acesso do Usuário
		- 3a1. Sistema redireciona o Usuário para a página de edição de perfil

### Inscrever-se no Teste Progresso e escolher a matéria do bônus

- Atores:
	- Aluno
	- Sistema

- Pré-Condições:
	- Aluno cadastrado e autenticado
	- Período de inscrição aberto
	- Aluno matriculado em ao menos uma matéria

- Fluxo Básico:
	1. Aluno acessa a inscrição do Teste Progresso
	2. Sistema exibe as matérias em que o Aluno está cursando no momento
	3. Aluno seleciona uma única matéria para receber o bônus
	4. Sistema registra a inscrição vinculada à matéria escolhida
	5. Sistema exibe confirmação da inscrição ao Aluno

- Fluxos Alternativos:
	- 3a. Aluno deseja trocar a matéria escolhida
		- 3a1. Sistema permite alterar a escolha enquanto o período de inscrição estiver aberto
	- 2a. Aluno não possui nenhuma matéria em curso
		- 2a1. Sistema informa que não há matéria elegível e impede a inscrição

### Organizar alunos nas salas

- Atores:
	- Coordenação
	- Sistema

- Pré-Condições:
	- Período de inscrições encerrado
	- Unidades e salas cadastradas

- Fluxo Básico:
	1. Coordenação solicita a geração da organização dos alunos por sala
	2. Sistema distribui os alunos inscritos entre as salas disponíveis, respeitando a capacidade de cada sala
	3. Sistema disponibiliza a cada Aluno a sala e a unidade em que fará a prova

- Fluxos Alternativos:
	- 2a. Quantidade de alunos inscritos excede a capacidade total das salas
		- 2a1. Sistema alerta a Coordenação sobre a insuficiência de salas

### Associar professores fiscais às salas

- Atores:
	- Coordenação
	- Professor (atuando como fiscal)
	- Sistema

- Pré-Condições:
	- Alunos já organizados nas salas

- Fluxo Básico:
	1. Coordenação consulta as salas ocupadas
	2. Coordenação associa um Professor a cada sala, para atuar como fiscal
	3. Sistema notifica o Professor sobre a sala e o horário em que atuará como fiscal

- Fluxos Alternativos:
	- 2a. Não há professor disponível para alguma sala
		- 2a1. Sistema alerta a Coordenação

### Lançar nota e aplicar bônus na matéria escolhida

- Atores:
	- Professor (atuando como fiscal)
	- Coordenação
	- Sistema

- Pré-Condições:
	- Professor associado à sala como fiscal
	- Prova aplicada e presença registrada
	- Aluno com inscrição vinculada a uma matéria

- Fluxo Básico:
	1. Professor, atuando como fiscal, registra a presença dos alunos na sua sala
	2. Coordenação lança ou importa a nota do Teste Progresso de cada Aluno presente
	3. Sistema aplica a nota como bônus na média da matéria que o Aluno escolheu na inscrição
	4. Aluno consulta o resultado e o efeito do bônus na matéria escolhida

- Fluxos Alternativos:
	- 1a. Aluno inscrito não comparece
		- 1a1. Sistema marca ausência e não aplica bônus à matéria escolhida
	- 2a. Nota lançada fora da faixa válida
		- 2a1. Sistema exibe mensagem de erro e não aplica a nota
