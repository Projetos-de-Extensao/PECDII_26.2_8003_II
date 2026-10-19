---
id: dt
title: Design Thinking
---

## **Design Thinking**

### **1. Capa**

- Sistema de gestão do teste de progresso
- Bento, Carlos, Julia e Lucas
- 2026.2

---

### **2. Introdução**

- **Contexto do Projeto**: Ajudar a secretaria acadêmica a organizar a aloção dos recursos disponíveis para a realização do teste de progresso.
- **Objetivo**: Desenvolver um sistema capaz de auxiliar no planejamento e na alocação dos recursos necessários para a aplicação do Teste de Progresso.
- **Público-Alvo**: Alunos, Coordenção e Secretaria do Ibmec.
- **Escopo**: Cadastro e organização de alunos, professores e salas por curso e unidade para a aplicação do teste de progresso.

---

### **3. Fases do Design Thinking**

#### **3.1. Empatia**

- **Pesquisa**: A pesquisa inicial foi realizada a partir da análise do funcionamento do Teste de Progresso, da necessidade de organização dos recursos envolvidos e da análise de sistemas e aplicações relacionadas a avaliações e gestão acadêmica. Foi levado em consideração, para essa primeira parte de desenvolvimento do projeto, apenas o Ibmec Rio de Janeiro
- **Análise de sistemas similares**: foram estudados sistemas e aplicativos com função parecida com a nossa (alocação de alunos em salas para provas, escala de fiscais e agendamento de exames). Detalhes completos na [Pesquisa](pesquisa.md).

| Sistema | O que faz | O que podemos aproveitar | Diferença para o nosso |
|---|---|---|---|
| [Cal-CS-61A-Staff/seating](https://github.com/Cal-CS-61A-Staff/seating) (GitHub) | App Flask em que o admin escolhe as salas e atribui assentos; o aluno faz login e consulta o seu | Consulta do aluno por login, vendo só o que é dele | Atrelado ao login de uma disciplina; não trata fiscais nem várias unidades |
| [Exam-Scheduling-Management-System](https://github.com/dharun-narayanan/Exam-Scheduling-Management-System_Web-App) (GitHub) | Aloca sala e horário e também os professores fiscais; o professor confirma sua disponibilidade | Disponibilidade do professor e alocação de fiscais (o mais próximo do nosso) | Não prevê cronograma alterável pelo aluno nem bônus de nota |
| [ExamHall-SeatAllocator](https://github.com/Govind-S-B/ExamHall-SeatAllocator/blob/main/README.md) (GitHub) | Distribui alunos por matéria/turma, evita mesma matéria lado a lado e gera PDFs | Geração de listas em PDF para impressão | App desktop; sem fiscais e sem consulta pelo aluno |
| [Exam-Seat-Arrangement](https://github.com/afreenpoly/Exam-Seat-Arrangement) (GitHub) | Web app Python/MongoDB; importa horários e dados dos alunos e distribui os assentos | Importação de planilhas de alunos | Foco só em assentos |
| [UniTime](https://www.apereo.org/programs/software/unitime) (Apereo, código aberto) | Módulo de exames modelado como problema de restrições e otimização, com compartilhamento de salas com outros eventos | Tratar a alocação como problema de restrições e detectar conflitos | Sistema genérico e pesado; não é integrado ao login e às regras do Ibmec |
| [SALAS](https://repositorio.ufc.br/handle/riufc/68392) (UFC) | Distribui turmas em salas por capacidade, horário, acessibilidade e recursos | Considerar acessibilidade do aluno e recursos da sala | Aloca aulas, não provas |
| Portal do Teste de Progresso do Ibmec, Moodle e Flexge | Aplicação e resultados do teste (ver Pesquisa) | Dashboard e consulta de resultados | Não organizam salas e fiscais |

  Conclusão: na busca feita não encontramos sistema voltado à alocação de fiscais de provas presenciais em universidades brasileiras. Os que existem tratam só de assentos ou de aulas. O diferencial do nosso projeto é unir salas, fiscais, cronograma individual do aluno e notas/bônus em um só sistema.

- **Insights**: É necessário organizar os professores que farão o papel de fiscais em cada sala, a quantidade de alunos por sala, além de garantir que os alunos respeitarão o horário da realização da prova.
- **Personas**: Coordenador e Secretaria, Professor e Aluno. 
Sendo as necessidades do coordenador e secretaria organizar os recursos disponíveis (fiscais & salas). As necessidades do professor consultar sua sala e horário de aplicação do teste, e por fim, as necessidades principais do aluno são visualizar local e horário da prova e futuramente consultar sua nota.

#### **3.2. Definição**

- **Problema Central**: Como podemos facilitar a organização e a alocação dos recursos necessários para a aplicação do Teste de Progresso, considerando alunos, professores, salas, cursos e unidades?.
- **Pontos de Vista (POV)**: 
*Coordenador & Secretaria* : O coordenador precisa de uma forma centralizada de organizar alunos, professores e salas porque a aplicação do Teste de Progresso envolve diversos recursos e possíveis conflitos de alocação.
*Professor*: O professor precisa consultar de forma rápida sua sala, horário e alunos porque essas informações são essenciais para sua participação na aplicação do teste.
*Aluno*: O aluno precisa visualizar de forma simples e rápida seu local e horário de prova.

#### **3.3. Ideação**

- **Brainstorming**: 
	- cadastro de alunos;
	- cadastro de professores;
	- cadastro de salas;
	- cadastro de cursos;
	- cadastro de unidades;
	- criação do Teste de Progresso;
	- visualização dos recursos;
	- alocação de alunos;
	- alocação de professores;
	- verificação da capacidade das salas;
	- identificação de conflitos;
	- geração de alocação;
	- consulta por aluno;
	- consulta por sala;
	- consulta por professor;
	- dashboard da aplicação;
	- relatórios de alocação.

- **Seleção de Ideias**: Os critérios utilizados para a seleção do que será desenvolvido foi a opinião dos integrantes do grupo de desenvolvimento do projeto.
- **Ideias Selecionadas**:
	- Dashboard: Para apresentar uma visão geral da aplicação.
	- Cadastro de recursos para gerenciar: alunos; professores; salas; cursos e unidades.
	- Criação do Teste para definir: data; horário; unidades; cursos participantes.
	- Geração da alocação: Para distribuir os alunos e professores considerando a disponibilidade e capacidade das salas.
	- Visualização da alocação para consultar: sala; alunos; professor; curso; unidade.
	- Identificação de conflitos para informar situações como: sala com capacidade insuficiente; professor duplicado; aluno sem sala; sala indisponível.

#### **3.4. Prototipagem**

- **Descrição do Protótipo**: A primeira versão do protótipo de baixa fidelidade foi feita levando em consideração a simplicidade e eficiência da aplicação; foi feita uma versão digital.
- **Materiais Utilizados**: O protótipo de baixa fidelidade foi desenhado utilizando o "Figma".
- **Testes Realizados**: O fluxo do protótipo foi testado pelos integrantes do grupo utilizando os recursos disponíveis da aplicação utilizada para o desenvolvimento do mesmo - Figma.

#### **3.5. Teste**

*É necessário destacar que ainda não foram realizados testes com usuários; acreditamos que esta etapa deve ser deixada para o futuro*

- **Feedback dos Usuários**: O que os usuários acharam do protótipo.
- **Ajustes Realizados**: Mudanças feitas com base no feedback.
- **Resultados Finais**: Descrição da solução final.

---

### **4. Conclusão**

- **Resultados Obtidos**: O que foi alcançado com o projeto.
- **Próximos Passos**: O que ainda precisa ser feito ou implementado.
- **Aprendizados**: Lições aprendidas durante o processo.

---

### **5. Anexos**

- Fotos, gráficos, tabelas, transcrições de entrevistas, etc.

---

### **6. Slides** 

- [Apresentação no Canva](https://canva.link/6d0b2fs4olu0qmw)

