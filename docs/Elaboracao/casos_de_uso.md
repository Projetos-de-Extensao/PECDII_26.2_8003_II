---
id: diagrama_de_casos de uso
title: Diagrama de Casos de Uso
---

## Casos de Uso

### Descrição:

- Unidades
	- Cadastro
- Salas
	- Cadastro
- Cursos
	- Cadastro
- Professores
	- Cadastro
- Alunos
	- Cadastro
- Autenticação
	- Login institucional (e-mail/conta da faculdade) — Administrador, Professor e Aluno
- Teste de Progresso
	- Criação
	- Consulta
- Cronograma do Teste (Local e Horário)
	- Confirmação (padrão = aula normal do dia)
	- Alteração de local e/ou horário (o Aluno só altera o próprio cronograma)
- Bônus
	- Escolha da matéria para receber o bônus (Aluno)
- Alocação
	- Automática
	- Identificação de Conflitos
	- Ajuste Manual
	- Geração de Lista
	- Dashboard
- Aplicação da Prova e Resultado
	- Notificação de sala/horário (Aluno e Professor fiscal)
	- Registro de presença
	- Lançamento de nota e aplicação do bônus na matéria escolhida

### Atores

- **Administrador** (Coordenação Acadêmica): acessa com seu e-mail/conta institucional da faculdade; responsável pelos cadastros, pela criação do Teste de Progresso e pela alocação de recursos.
- **Professor**: acessa com seu e-mail/conta institucional da faculdade; consultado quanto à disponibilidade; atua como fiscal em uma sala, registrando presença e participando do lançamento de nota.
- **Aluno**: acessa com sua conta institucional da faculdade (mesmo login usado nos demais sistemas acadêmicos); por padrão realiza o teste no local e horário da sua aula normal no dia do teste, mas pode alterar manualmente local e/ou horário, se houver vaga; só pode visualizar/alterar o **próprio** cronograma, nunca o de outro aluno; escolhe uma matéria em curso para receber o bônus de nota do resultado do teste.
- **Sistema**: executa validações, cálculo de alocação e detecção de conflitos.
- **Sistema Acadêmico da Faculdade** (ator externo): autentica as credenciais institucionais de todos os usuários (Administrador, Professor e Aluno) via portal/SSO da faculdade; o sistema de Teste de Progresso não armazena senha de ninguém.

### Diagrama de Casos de Uso (PlantUML)

```puml
@startuml TesteProgresso_CasosDeUso

left to right direction
skinparam actorStyle awesome

actor Administrador as "Administrador (Coordenação)"
actor Professor
actor Aluno
actor "Sistema Acadêmico\n(Faculdade)" as SA

rectangle "Alocação do Teste de Progresso" {
  usecase (Fazer Login\n(e-mail institucional)) as UC00
  usecase (Cadastrar Recursos\n(Unidade / Sala / Curso / Professor / Aluno)) as UC01
  usecase (Criar Teste de Progresso) as UC02
  usecase (Consultar Testes Criados) as UC03
  usecase (Realizar Alocação Automática) as UC04
  usecase (Identificar Conflitos de Alocação) as UC05
  usecase (Ajustar Alocação Manualmente) as UC06
  usecase (Informar Disponibilidade) as UC07
  usecase (Confirmar Cronograma do Teste\n(padrão: local/horário da aula normal)) as UC08
  usecase (Alterar Cronograma do Teste\n(local e/ou horário, próprio cronograma)) as UC09
  usecase (Escolher Matéria\npara Bônus) as UC11
  usecase (Notificar Aluno e Professor\n(Sala/Horário)) as UC12
  usecase (Registrar Presença) as UC13
  usecase (Lançar Nota e Aplicar Bônus\nna Matéria Escolhida) as UC14

  Administrador --> UC00
  Administrador --> UC01
  Administrador --> UC14
  Professor --> UC00
  Professor --> UC13
  Aluno --> UC00
  UC00 --> SA

  UC00 ..> UC02 : <<extend>>
  UC00 ..> UC07 : <<include>>
  UC00 ..> UC08 : <<include>>
  UC02 ..> UC03 : <<extend>>
  UC02 ..> UC08 : <<include>>
  UC08 ..> UC09 : <<extend>>
  UC08 ..> UC11 : <<include>>
  UC08 ..> UC04 : <<include>>
  UC04 ..> UC05 : <<include>>
  UC05 ..> UC06 : <<extend>>
  UC04 ..> UC12 : <<include>>
  UC07 ..> UC04 : <<include>>
  UC13 ..> UC14 : <<include>>
}

note right of UC02
  **Pré-condição**: unidades, salas, cursos,
  professores e alunos já cadastrados.
  **Pós-condição**: alocação consolidada e
  sem conflitos pendentes.
end note

note bottom of UC09
  Só é permitido se houver vaga (capacidade)
  no local/horário escolhido, e somente
  para o cronograma do próprio Aluno logado.
end note

note bottom of UC14
  Bônus só é aplicado se houver presença
  registrada e matéria de bônus escolhida
  pelo Aluno.
end note

@enduml
```

**Relacionamentos:**

- `<<extend>>` (Fazer Login → Criar Teste de Progresso): login é pré-requisito opcionalmente acionado antes da criação do teste (Administrador).
- `<<include>>` (Fazer Login → Informar Disponibilidade): o Professor só informa disponibilidade depois de autenticado com o e-mail institucional.
- `<<include>>` (Fazer Login → Confirmar Cronograma do Teste): o Aluno só acessa/confirma seu cronograma depois de autenticado com o e-mail institucional, e apenas o seu próprio (nunca o de outro aluno).
- `<<extend>>` (Criar Teste de Progresso → Consultar Testes Criados): consulta ao histórico é um fluxo alternativo, não obrigatório.
- `<<include>>` (Criar Teste de Progresso → Confirmar Cronograma do Teste): toda criação de teste aciona a definição do cronograma (local e horário) de cada aluno, cujo padrão é o local/horário da aula normal do aluno no dia do teste.
- `<<extend>>` (Confirmar Cronograma do Teste → Alterar Cronograma do Teste): só ocorre quando o aluno opta manualmente por outro local e/ou horário, sujeito à disponibilidade de vaga, e restrito ao próprio cronograma.
- `<<include>>` (Confirmar Cronograma do Teste → Realizar Alocação Automática): a alocação usa o cronograma confirmado de cada aluno (padrão ou alterado).
- `<<include>>` (Confirmar Cronograma do Teste → Escolher Matéria para Bônus): ao confirmar o cronograma, o Aluno também escolhe (ou mantém) a matéria que receberá o bônus.
- `<<include>>` (Realizar Alocação Automática → Identificar Conflitos de Alocação): toda alocação gerada precisa ser validada.
- `<<extend>>` (Identificar Conflitos de Alocação → Ajustar Alocação Manualmente): só ocorre quando há conflito.
- `<<include>>` (Realizar Alocação Automática → Notificar Aluno e Professor): concluída a alocação, o sistema avisa cada aluno e cada professor fiscal sobre sala/horário.
- `<<include>>` (Informar Disponibilidade → Realizar Alocação Automática): a alocação depende da disponibilidade informada pelos professores.
- `<<include>>` (Registrar Presença → Lançar Nota e Aplicar Bônus): só é possível lançar a nota/bônus de um Aluno cuja presença já foi registrada pelo Professor fiscal.

---

## Autenticação

### Fazer Login (E-mail Institucional)

* Atores:
	- Administrador
	- Professor
	- Aluno
	- Sistema Acadêmico da Faculdade

- Pré-Condições:
	- Usuário (Administrador, Professor ou Aluno) possui conta ativa no sistema acadêmico da faculdade
	- Usuário já está cadastrado no sistema de Teste de Progresso com o mesmo e-mail/matrícula institucional

* Fluxo Básico:
    1. Usuário acessa a tela de login e informa seu e-mail institucional e senha da faculdade
    2. Sistema encaminha as credenciais para autenticação no Sistema Acadêmico da Faculdade
    3. Sistema Acadêmico valida as credenciais e retorna a identidade autenticada (e-mail/matrícula) e o papel do usuário (Administrador, Professor ou Aluno)
    4. Sistema localiza o cadastro correspondente a partir da identidade autenticada
    5. Sistema libera o acesso de acordo com o perfil: Administrador → painel administrativo; Professor → disponibilidade e salas; Aluno → horário do teste e inscrição em horário alternativo

- Fluxos Alternativos:
	- 3a. Credenciais inválidas
		- 3a1. Sistema Acadêmico rejeita a autenticação e o Sistema exibe mensagem de erro
	- 3b. Sistema Acadêmico da Faculdade indisponível
		- 3b1. Sistema exibe mensagem de erro e permite nova tentativa
	- 4a. Identidade autenticada não corresponde a nenhum cadastro no sistema de Teste de Progresso
		- 4a1. Sistema exibe mensagem de erro e orienta o usuário a contatar a Coordenação

---

## Cadastros

### Cadastrar Unidade

* Atores:
	- Administrador

- Pré-Condições:
	- Nenhuma

* Fluxo Básico:
    1. Administrador informa nome, endereço e unidade
    2. Sistema valida os dados informados
    3. Sistema persiste a Unidade cadastrada
    4. Sistema confirma o cadastro

- Fluxos Alternativos:
	- 2a. Dados obrigatórios não preenchidos
		- 2a1. Sistema exibe mensagem de erro

### Cadastrar Sala

* Atores:
	- Administrador

- Pré-Condições:
	- Unidade cadastrada

* Fluxo Básico:
    1. Administrador informa número, capacidade e unidade da sala
    2. Sistema valida os dados informados
    3. Sistema persiste a Sala, associada à Unidade
    4. Sistema confirma o cadastro

- Fluxos Alternativos:
	- 1a. Unidade informada não existe
		- 1a1. Sistema exibe mensagem de erro
	- 3a. Administrador marca a sala como indisponível
		- 3a1. Sistema impede que a sala seja usada em alocações futuras

### Cadastrar Curso

* Atores:
	- Administrador

- Pré-Condições:
	- Unidade cadastrada

* Fluxo Básico:
    1. Administrador informa nome do curso e unidade
    2. Sistema valida os dados informados
    3. Sistema persiste o Curso, associado à Unidade
    4. Sistema confirma o cadastro

- Fluxos Alternativos:
	- 1a. Unidade informada não existe
		- 1a1. Sistema exibe mensagem de erro

### Cadastrar Aluno

* Atores:
	- Administrador

- Pré-Condições:
	- Curso cadastrado

* Fluxo Básico:
    1. Administrador informa matrícula, nome, curso, período e turma do aluno
    2. Sistema valida os dados informados (matrícula única)
    3. Sistema persiste o Aluno, associado ao Curso
    4. Sistema confirma o cadastro

- Fluxos Alternativos:
	- 2a. Matrícula já cadastrada
		- 2a1. Sistema exibe mensagem de erro
	- 1a. Curso informado não existe
		- 1a1. Sistema exibe mensagem de erro

### Cadastrar Professor

* Atores:
	- Administrador

- Pré-Condições:
	- Unidade cadastrada

* Fluxo Básico:
    1. Administrador informa nome e unidade do professor
    2. Sistema valida os dados informados
    3. Sistema persiste o Professor, associado à Unidade
    4. Sistema confirma o cadastro

- Fluxos Alternativos:
	- 1a. Unidade informada não existe
		- 1a1. Sistema exibe mensagem de erro

### Informar Disponibilidade

* Atores:
	- Professor

- Pré-Condições:
	- Professor cadastrado
	- Professor autenticado via "Fazer Login (E-mail Institucional)" *«include»*

* Fluxo Básico:
    1. Professor informa horários e datas disponíveis
    2. Sistema valida os dados informados
    3. Sistema atualiza a disponibilidade do Professor

- Fluxos Alternativos:
	- 2a. Conflito com disponibilidade já registrada
		- 2a1. Sistema exibe mensagem de erro

---

## Planejamento

### Criar Teste de Progresso

* Atores:
	- Administrador
	- Sistema

- Pré-Condições:
	- Unidades e cursos participantes cadastrados

* Fluxo Básico:
    1. Administrador informa data, duração e um ou mais locais/horários/turnos oferecidos no dia
    2. Administrador seleciona unidades e cursos participantes
    3. Sistema valida os dados informados
    4. Sistema persiste o Teste de Progresso
    5. Sistema aciona "Confirmar Cronograma do Teste" *«include»* para cada aluno participante

- Fluxos Alternativos:
	- 3a. Já existe um teste na mesma data/horário para a mesma unidade
		- 3a1. Sistema exibe mensagem de erro
	- 5a. Administrador opta por "Consultar Testes Criados" *«extend»*

### Confirmar Cronograma do Teste

* Atores:
	- Aluno
	- Sistema

- Pré-Condições:
	- Teste de Progresso criado, com um ou mais locais/horários/turnos oferecidos
	- Aluno matriculado em turma com local e horário de aula normal definidos

* Fluxo Básico:
    1. Sistema identifica o local (unidade/sala) e o horário da aula normal do Aluno no dia do teste
    2. Sistema atribui esse local e horário como cronograma padrão do Aluno para o teste
    3. Aluno realiza "Fazer Login (E-mail Institucional)" *«include»* e visualiza **apenas o seu próprio** cronograma (local e horário) atribuído
    4. Sistema aciona "Realizar Alocação Automática" *«include»* com o cronograma confirmado

- Fluxos Alternativos:
	- 1a. Aluno não possui aula normal no dia do teste (ex.: dia sem grade para o seu curso/período)
		- 1a1. Sistema exige que o Aluno escolha manualmente local e horário via "Alterar Cronograma do Teste"
	- 2a. Aluno deseja realizar o teste em local e/ou horário diferente do padrão
		- 2a1. Sistema aciona "Alterar Cronograma do Teste" *«extend»*

### Alterar Cronograma do Teste (Local e/ou Horário)

* Atores:
	- Aluno
	- Sistema

- Pré-Condições:
	- Aluno autenticado (login institucional) e cronograma padrão já definido (ou pendente, se o Aluno não possui aula no dia)
	- Teste de Progresso possui mais de um local e/ou horário/turno disponível
	- Alteração restrita ao cronograma do próprio Aluno autenticado

* Fluxo Básico:
    1. Aluno consulta os locais e horários/turnos oferecidos para o Teste de Progresso
    2. Aluno seleciona um local e/ou horário alternativo diferente do seu padrão
    3. Sistema verifica se há vaga disponível (capacidade de sala) no local/horário alternativo, considerando o curso/turma do Aluno
    4. Sistema confirma a alteração do cronograma do Aluno para o local/horário escolhido
    5. Sistema atualiza o cronograma do Aluno para o teste, substituindo o padrão

- Fluxos Alternativos:
	- 3a. Não há vaga disponível no local/horário alternativo escolhido
		- 3a1. Sistema exibe mensagem de erro e mantém o cronograma padrão (ou pendente) do Aluno
	- 2a. Aluno tenta alterar o cronograma após o prazo limite de alteração
		- 2a1. Sistema exibe mensagem de erro e mantém o cronograma padrão do Aluno
	- 2b. Aluno tenta acessar ou alterar o cronograma de outro aluno (ex.: manipulando um identificador na requisição)
		- 2b1. Sistema nega o acesso, pois o Aluno autenticado só pode alterar o próprio cronograma

### Escolher Matéria para Bônus

* Atores:
	- Aluno
	- Sistema

- Pré-Condições:
	- Aluno autenticado via "Fazer Login (E-mail Institucional)"
	- Aluno matriculado em ao menos uma matéria no período corrente
	- Período de escolha aberto (vinculado ao Teste de Progresso)

* Fluxo Básico:
    1. Aluno acessa a área de inscrição do Teste de Progresso
    2. Sistema exibe as matérias em que o Aluno está matriculado no momento
    3. Aluno seleciona uma única matéria para receber o bônus de nota
    4. Sistema registra a escolha vinculada à matrícula do Aluno no Teste de Progresso
    5. Sistema exibe confirmação da escolha ao Aluno

- Fluxos Alternativos:
	- 2a. Aluno não possui nenhuma matéria em curso
		- 2a1. Sistema informa que não há matéria elegível; o Aluno ainda participa do teste, porém sem bônus vinculado
	- 3a. Aluno deseja trocar a matéria escolhida
		- 3a1. Sistema permite alterar a escolha enquanto o período estiver aberto
	- 3b. Aluno tenta escolher/trocar a matéria após o prazo limite
		- 3b1. Sistema exibe mensagem de erro e mantém a escolha anterior (ou nenhuma)

### Consultar Testes Criados

* Atores:
	- Administrador

- Pré-Condições:
	- Ao menos um Teste de Progresso cadastrado

* Fluxo Básico:
    1. Administrador acessa a lista de testes criados
    2. Sistema exibe testes com data, unidades, cursos e status da alocação

- Fluxos Alternativos:
	- 2a. Nenhum teste cadastrado
		- 2a1. Sistema exibe mensagem informativa

---

## Alocação

### Realizar Alocação Automática de Recursos

* Atores:
	- Administrador
	- Sistema

- Pré-Condições:
	- Teste de Progresso criado
	- Cronograma (local e horário) de cada aluno confirmado (padrão ou alterado)
	- Alunos, salas e professores cadastrados e disponíveis para a data do teste

* Fluxo Básico:
    1. Administrador seleciona o Teste de Progresso
    2. Sistema separa os alunos por curso/período e por cronograma (local e horário) confirmado
    3. Sistema verifica salas disponíveis por unidade e horário
    4. Sistema verifica capacidade de cada sala
    5. Sistema verifica professores disponíveis
    6. Sistema gera a alocação (aluno → sala, professor → sala)
    7. Sistema aciona "Identificar Conflitos de Alocação" *«include»*
    8. Sistema exibe o resultado consolidado da alocação

- Fluxos Alternativos:
	- 3a. Não há salas suficientes na unidade
		- 3a1. Sistema exibe alerta de capacidade insuficiente
	- 5a. Não há professores suficientes disponíveis
		- 5a1. Sistema exibe alerta e sugere ajuste manual

### Identificar Conflitos de Alocação

* Atores:
	- Sistema
	- Administrador

- Pré-Condições:
	- Alocação gerada (automática ou manual)

* Fluxo Básico:
    1. Sistema valida a alocação gerada
    2. Sistema verifica: sala com capacidade insuficiente, professor em duas salas, sala ocupada, professor indisponível, aluno sem sala, aluno duplicado
    3. Sistema lista os conflitos encontrados (ou confirma "0 conflitos")
    4. Administrador visualiza a lista de conflitos

- Fluxos Alternativos:
	- 3a. Existem conflitos
		- 3a1. Sistema aciona "Ajustar Alocação Manualmente" *«extend»*

### Ajustar Alocação Manualmente

* Atores:
	- Administrador

- Pré-Condições:
	- Conflitos identificados na alocação

* Fluxo Básico:
    1. Administrador seleciona o conflito a resolver
    2. Administrador reatribui sala, professor ou aluno manualmente
    3. Sistema revalida a alocação
    4. Sistema atualiza o status do conflito

- Fluxos Alternativos:
	- 2a. Ajuste proposto gera novo conflito
		- 2a1. Sistema exibe mensagem de erro e mantém a alocação anterior

---

## Aplicação da Prova e Resultado

### Notificar Aluno e Professor (Sala/Horário)

* Atores:
	- Sistema

- Pré-Condições:
	- Alocação automática concluída sem conflitos pendentes

* Fluxo Básico:
    1. Sistema identifica, para cada Aluno alocado, o local e o horário definidos
    2. Sistema envia notificação ao Aluno com unidade, sala e horário do teste
    3. Sistema identifica, para cada Professor fiscal, a sala e o horário atribuídos
    4. Sistema envia notificação ao Professor com sala e horário em que atuará como fiscal

- Fluxos Alternativos:
	- 1a. Alocação é ajustada manualmente após o envio inicial ("Ajustar Alocação Manualmente")
		- 1a1. Sistema reenvia a notificação com os dados atualizados

### Registrar Presença

* Atores:
	- Professor (atuando como fiscal)
	- Sistema

- Pré-Condições:
	- Professor associado à sala como fiscal (via alocação)
	- Teste de Progresso em aplicação (data/horário da sala do Professor)

* Fluxo Básico:
    1. Professor acessa a lista de alunos alocados na sua sala
    2. Professor marca presença ou ausência de cada Aluno
    3. Sistema registra a presença vinculada ao Aluno e ao Teste de Progresso

- Fluxos Alternativos:
	- 2a. Aluno alocado não comparece
		- 2a1. Sistema marca ausência; nenhum bônus será aplicado à matéria escolhida por esse Aluno

### Lançar Nota e Aplicar Bônus na Matéria Escolhida

* Atores:
	- Administrador
	- Professor (atuando como fiscal)
	- Sistema

- Pré-Condições:
	- Presença do Aluno já registrada ("Registrar Presença")
	- Aluno com matéria de bônus escolhida ("Escolher Matéria para Bônus"), quando aplicável

* Fluxo Básico:
    1. Administrador lança ou importa a nota do Teste de Progresso de cada Aluno presente
    2. Sistema valida a nota informada
    3. Sistema aplica a nota como bônus na média da matéria que o Aluno escolheu
    4. Aluno consulta o resultado e o efeito do bônus na matéria escolhida

- Fluxos Alternativos:
	- 1a. Aluno inscrito não compareceu ("Registrar Presença" marcou ausência)
		- 1a1. Sistema não aplica bônus a nenhuma matéria para esse Aluno
	- 2a. Nota lançada fora da faixa válida
		- 2a1. Sistema exibe mensagem de erro e não aplica a nota
	- 3a. Aluno não escolheu matéria de bônus
		- 3a1. Sistema registra a nota do teste sem aplicar bônus a nenhuma matéria

---

## Acompanhamento

### Gerar Lista de Salas/Alunos

* Atores:
	- Administrador
	- Professor

- Pré-Condições:
	- Alocação sem conflitos pendentes

* Fluxo Básico:
    1. Administrador ou Professor seleciona o Teste de Progresso
    2. Sistema gera a lista de alunos por sala, curso e unidade
    3. Sistema disponibiliza a lista para impressão/exportação

### Visualizar Dashboard do Teste

* Atores:
	- Administrador

- Pré-Condições:
	- Teste de Progresso criado

* Fluxo Básico:
    1. Administrador acessa o dashboard do Teste de Progresso
    2. Sistema exibe indicadores consolidados: total de alunos, cursos, unidades, salas, professores, alunos alocados, salas utilizadas e conflitos

- Fluxos Alternativos:
	- 2a. Existem conflitos não resolvidos
		- 2a1. Sistema destaca o número de conflitos em alerta
