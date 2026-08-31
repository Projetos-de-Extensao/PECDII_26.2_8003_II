---
id: pesquisa
title: Pesquisa
---

# Pesquisa
### **1. Capa**

- Tema: 
- Data: 2026.1
- Stakeholder: Pro-Reitoria Acadêmica

---

### **2. Pesquisa**

1. Contexto do projeto
Os três pontos definidos para a pesquisa:
•	Teste de progresso: alocação de recursos, salas, professores, cursos e alunos
•	Funcionalidades
•	Aplicativos similares (GitHub)
Portanto, a aplicação pode ser entendida como um sistema de gerenciamento e planejamento do Teste de Progresso do Ibmec, principalmente para ajudar a instituição a organizar a aplicação da prova.
 
2. O que é o Teste de Progresso?
O Teste de Progresso é uma avaliação que acompanha a evolução acadêmica do aluno durante a graduação. Diferentemente de uma prova tradicional, ele procura avaliar conhecimentos e competências acumulados ao longo do curso.
No caso do Ibmec, isso é especialmente relevante porque o próprio Ibmec informa que o Teste de Progresso é aplicado a todos os alunos de graduação e funciona como um mapeamento de competências gerais e específicas. A instituição também relaciona o teste à preparação para avaliações como o ENADE. (Ibmec)
Uma característica importante é que o resultado pode ser utilizado não apenas para avaliar o aluno, mas também para avaliar o próprio curso e identificar pontos que precisam ser melhorados. Estudos sobre Teste de Progresso destacam justamente essa utilização dos resultados para gestão acadêmica e identificação de lacunas de aprendizagem. (SciELO)
Para o projeto de vocês
Isso significa que o sistema não deveria pensar somente:
"Qual aluno fará a prova?"
Mas também:
"Onde essa prova será realizada, quem aplicará, quantos alunos participarão, quais cursos estarão envolvidos e quais recursos são necessários?"
É aí que entra a alocação de recursos.
 
3. Alocação de recursos
A principal dificuldade que o sistema pode resolver é transformar a aplicação do Teste de Progresso em um problema de alocação e otimização de recursos.
Os principais recursos seriam:
🏫 Salas
O sistema precisa saber:
•	quais salas estão disponíveis;
•	em qual unidade estão;
•	capacidade de cada sala;
•	horário disponível;
•	quais salas estão ocupadas;
•	quantidade de alunos que podem ser colocados em cada sala.
No Ibmec Barra, por exemplo, a unidade possui 33 salas de aula e 28 laboratórios, além de auditório. (Ibmec)
👨‍🏫 Professores
O sistema poderia controlar:
•	professores disponíveis;
•	horários disponíveis;
•	unidade;
•	quantidade máxima de salas que podem supervisionar;
•	distribuição dos professores entre as salas.
Por exemplo:
Sala 101 → Professor A
Sala 102 → Professor B
Sala 103 → Professor C
Assim, o sistema evita que uma sala fique sem fiscal ou que um professor seja alocado em dois lugares simultaneamente.
👩‍🎓 Alunos
Para cada aluno, seria interessante armazenar:
•	matrícula;
•	nome;
•	curso;
•	período;
•	unidade;
•	turma;
•	sala atribuída;
•	situação no teste.
Isso permite organizar automaticamente os alunos.
Por exemplo:
Curso	Alunos	Sala
Administração	35	101
Direito	40	102
Ciência de Dados e IA	30	103
Engenharia de Software	38	104
 
4. Cursos do Ibmec Rio de Janeiro
Aqui existe um ponto importante para o banco de dados.
O site do Ibmec apresenta diferentes unidades no Rio de Janeiro, incluindo Barra da Tijuca e Botafogo.
Unidade Barra
A documentação oficial do Ibmec lista:
1.	Administração
2.	Arquitetura e Urbanismo
3.	Análise e Desenvolvimento de Sistemas
4.	Ciências Econômicas
5.	Ciência de Dados e Inteligência Artificial
6.	Publicidade e Propaganda
7.	Direito
8.	Engenharia Civil
9.	Engenharia da Computação
10.	Engenharia Mecânica
11.	Engenharia de Produção
12.	Engenharia de Software
13.	Relações Internacionais
Ou seja, 13 cursos de graduação na unidade Barra nessa relação. (Blog IBMEC)
Há confirmação recente de vários desses cursos no material institucional de 2025/2026, incluindo Engenharia Mecânica, Engenharia de Software, Engenharia da Computação, Engenharia de Produção, Arquitetura, Publicidade, Direito etc. (Ibmec)
Unidade Botafogo
A documentação institucional lista:
1.	Administração
2.	Ciências Contábeis
3.	Ciências Econômicas
4.	Direito
5.	Relações Internacionais
Portanto, 5 cursos de graduação. (Blog IBMEC) – adicionar CDIA
Para o modelo do projeto, eu recomendaria não deixar os cursos "fixos" no código. Eles devem ser entidades no banco, associadas a uma unidade. Assim, se o Ibmec mudar a oferta de cursos, o sistema continua funcionando.
 
5. Como transformar isso em um sistema
Uma estrutura inicial poderia ser:
UNIDADE
   │
   ├── SALAS
   │
   └── CURSOS
          │
          └── ALUNOS

PROFESSORES
      │
      ↓
APLICAÇÃO DO TESTE
      │
      ├── Unidade
      ├── Sala
      ├── Professor/Fiscal
      ├── Curso
      ├── Alunos
      └── Horário
Ou, pensando no banco de dados:
Unidade
id_unidade
nome
endereco
Sala
id_sala
numero
capacidade
id_unidade
Curso
id_curso
nome
id_unidade
Aluno
id_aluno
nome
matricula
periodo
id_curso
Professor
id_professor
nome
id_unidade
Teste
id_teste
data
horario_inicio
horario_fim
Alocação
Essa seria uma das entidades mais importantes:
id_alocacao
id_teste
id_sala
id_professor
E uma outra relação poderia ligar alunos à alocação:
id_alocacao
id_aluno
 
6. Funcionalidades
Com base no problema, eu dividiria as funcionalidades em administrativas, alocação e acompanhamento.
1. Cadastro de unidades
Permitir cadastrar:
•	unidade;
•	endereço;
•	quantidade de salas;
•	capacidade.
2. Cadastro de salas
Permitir:
•	cadastrar sala;
•	informar capacidade;
•	informar unidade;
•	marcar sala como disponível/indisponível.
3. Cadastro de cursos
Permitir:
•	cadastrar curso;
•	associar curso a uma unidade;
•	consultar quantidade de alunos por curso.
4. Cadastro de alunos
Permitir:
•	cadastrar aluno;
•	associar ao curso;
•	informar período;
•	consultar participação no teste.
5. Cadastro de professores
Permitir:
•	cadastrar professor;
•	associar à unidade;
•	informar disponibilidade.
6. Criação do Teste de Progresso
O administrador poderia informar:
•	data;
•	horário;
•	duração;
•	unidades participantes;
•	cursos participantes.
7. Alocação automática
Essa provavelmente seria a principal funcionalidade do projeto.
O sistema receberia:
500 alunos + 15 salas + 15 professores
e tentaria encontrar uma distribuição válida.
Por exemplo:
500 alunos
     ↓
separar por curso/período
     ↓
verificar salas disponíveis
     ↓
verificar capacidade
     ↓
verificar professores disponíveis
     ↓
gerar alocação
     ↓
resultado final
8. Identificação de conflitos
O sistema deveria detectar situações como:
•	sala com capacidade insuficiente;
•	professor alocado em duas salas;
•	sala ocupada;
•	professor indisponível;
•	aluno sem sala;
•	aluno duplicado;
•	quantidade de alunos maior que a capacidade disponível.
9. Geração da lista de salas
Exemplo:
Aluno	Curso	Unidade	Sala
João	Administração	Barra	101
Maria	Direito	Barra	102
Pedro	Ciência de Dados	Barra	103
10. Dashboard
Um painel poderia mostrar:
TESTE DE PROGRESSO — 10/09/2026

Alunos:       1.250
Cursos:          13
Unidades:         2
Salas:           35
Professores:     40

Alunos alocados: 1.250
Salas utilizadas: 32
Conflitos:         0
O próprio Ibmec já utiliza uma lógica de painel para o Teste de Progresso, com consulta de resultados individuais e indicadores consolidados por curso, unidade e período.
Isso é uma ótima referência para o projeto.
 
7. Aplicativos/sistemas similares
Não encontrei um aplicativo público exatamente igual ao que vocês estão propondo, mas existem sistemas e plataformas que oferecem funcionalidades semelhantes.
1. Portal de Teste de Progresso do Ibmec
É provavelmente a referência mais importante para vocês.
O portal possui:
•	consulta individual de desempenho;
•	histórico;
•	certificados;
•	indicadores consolidados;
•	acompanhamento por curso;
•	acompanhamento por unidade;
•	acompanhamento por período;
•	recorte comparativo com ENADE. (tp.econ.rio.br)
O que podemos aproveitar como referência: dashboard e organização dos resultados.
 
2. Moodle
O Moodle é uma plataforma educacional bastante utilizada para aplicação de avaliações.
Em experiências de Teste de Progresso, ele já foi utilizado para:
•	disponibilizar questões;
•	aplicar provas;
•	controlar duração;
•	randomizar questões;
•	armazenar resultados.
Um estudo sobre Teste de Progresso relata a utilização do Moodle para aplicação das avaliações, inclusive com distribuição aleatória das questões. (PubMed Central (PMC))
Diferença: Moodle é principalmente um LMS/ambiente educacional. O projeto de vocês teria como foco a gestão e alocação dos recursos físicos e humanos da prova.
 
3. Flexge
A Flexge possui uma funcionalidade chamada Progress Test, permitindo acompanhar a evolução do aluno ao longo do tempo e aplicar o teste individualmente ou para grupos. (knowledge.flexge.com)
Funcionalidades interessantes como referência:
•	aplicação individual;
•	aplicação para grupos;
•	acompanhamento de desempenho;
•	código de acesso;
•	histórico.
 
8. O diferencial do projeto de vocês
O mais interessante é que o projeto não precisa tentar ser apenas mais uma plataforma de prova.
Existem plataformas que já fazem:
criar questões → aplicar prova → corrigir → mostrar nota.
O problema que vocês podem atacar é diferente:
Como organizar a infraestrutura necessária para aplicar o Teste de Progresso para centenas/milhares de alunos em diferentes unidades?
Isso transforma o projeto em um problema de gestão + banco de dados + otimização.
Por exemplo:
Entrada:
2 unidades
13 cursos
1.500 alunos
50 professores
40 salas
Sistema calcula:
Quais salas usar?
Quantos alunos por sala?
Quais professores serão fiscais?
Qual professor ficará em qual sala?
Qual aluno ficará em qual sala?
Existe algum conflito?
Saída:
UNIDADE BARRA

Sala 101
Professor: Carlos
40 alunos

Sala 102
Professor: Ana
38 alunos

Sala 103
Professor: João
40 alunos

...

UNIDADE BOTAFOGO

Sala 201
Professor: Maria
35 alunos
Em uma frase, eu definiria o projeto assim:
Sistema de gerenciamento e alocação de recursos para a aplicação do Teste de Progresso do Ibmec, permitindo distribuir alunos, professores e salas entre cursos e unidades, detectar conflitos e gerar uma visão consolidada da aplicação.
Fontes principais: Issue #2 do projeto no GitHub · Repositório do projeto · Graduação Ibmec · Unidades Ibmec.

