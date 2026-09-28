---
id: diagrama_de_classes
title: Diagrama de Classes
---

## Diagrama de Classes

### Objetivo

O Diagrama de Classes é uma representação visual das classes, seus atributos, métodos e os relacionamentos entre elas. Ele é fundamental para a modelagem orientada a objetos e serve como base para a implementação do sistema.

### Componentes do Diagrama de Classes

Este documento define um modelo para:

1. **Inserção do Diagrama de Classes Conceitual** (visão de domínio).  
2. **Evolução para o Diagrama de Classes de Especificação** (visão de projeto).  

Ambos devem ser derivados de:

- Casos de uso;
- Diagrama de casos de uso;
- Documento de levantamento de requisitos;
- Protótipo de baixa fidelidade.

### Fontes de entrada obrigatórias

- **Levantamento de requisitos**: requisitos funcionais e não funcionais.
- **Casos de uso**: atores, fluxos principal e alternativos.
- **Diagrama de casos de uso**: escopo e fronteiras do sistema.
- **Protótipo de baixa fidelidade**: entidades percebidas na interface e regras de navegação.

### 1) Diagrama de Classes Conceitual

#### 1.1 Finalidade

Representar os principais conceitos do domínio do Sistema de Gestão do Teste Progresso, suas responsabilidades e os relacionamentos existentes entre eles, sem apresentar detalhes de implementação.

O modelo conceitual foi elaborado com base no Documento de Visão, Brainstorm e Casos de Uso do sistema.

#### 1.2 Escopo

O Diagrama de Classes Conceitual contempla os principais conceitos de negócio identificados para o Sistema de Gestão do Teste Progresso:

- Usuários;
- Perfis;
- Alunos;
- Professores;
- Coordenação;
- Cursos;
- Matérias;
- Matrículas;
- Unidades;
- Salas;
- Teste Progresso;
- Inscrições;
- Ensalamento;
- Alocação de professores fiscais;
- Resultados do Teste Progresso;
- Notificações.

O modelo contempla também os relacionamentos e as respectivas multiplicidades entre os conceitos.

#### 1.3 Notação mínima

Para cada classe conceitual são apresentados:

- **Nome**;
- **Descrição curta**;
- **Atributos de domínio**, sem especificação de tipos técnicos;
- **Relacionamentos** com suas respectivas multiplicidades;
- **Restrições de negócio**, quando aplicável.

Não são incluídos métodos, tipos técnicos de atributos, classes de controle, serviços, repositórios ou outros elementos relacionados à implementação do sistema.

#### 1.4 Rastreabilidade

| Classe Conceitual | Requisito(s) | Caso(s) de Uso | Tela/Protótipo |
|---|---|---|---|
| Usuario | BS01, BS02, BS03 | Criação de uma conta; Entrada do usuário | Tela de criação de conta / Entrada |
| Perfil | BS01, BS02, BS03 | Edição; Visualização | Tela de perfil |
| Aluno | BS02, BS03, BS05, BS09 | Inscrição; Organizar alunos nas salas; Lançar nota e aplicar bônus | Área do aluno |
| Professor | BS02, BS11, BS12 | Associar professores fiscais às salas | Área do professor |
| Coordenacao | BS02, BS06, BS07, BS11 | Organizar alunos nas salas; Associar professores fiscais às salas | Área da coordenação |
| Curso | BS04, BS05 | Cadastro de Curso e Matérias | Tela de cursos |
| Materia | BS04, BS05, BS13 | Cadastro de Curso e Matérias; Inscrição | Tela de matérias / Inscrição |
| Matricula | BS05 | Vínculo do Aluno com Curso e Matérias em curso | Tela de perfil do aluno |
| Unidade | BS06, BS08, BS13 | Cadastro de Unidade e Salas | Tela de unidades |
| Sala | BS07, BS08, BS09, BS10, BS12 | Organizar alunos nas salas; Associar professores fiscais às salas | Tela de salas / Ensalamento |
| TesteProgresso | BS09, BS10, BS13 | Inscrição; Organizar alunos nas salas; Lançar nota e aplicar bônus | Tela do Teste Progresso |
| Inscricao | BS09, BS13 | Inscrever-se no Teste Progresso e escolher matéria do bônus | Tela de inscrição |
| Ensalamento | BS09, BS10 | Organizar alunos nas salas | Tela de ensalamento |
| AlocacaoFiscal | BS11, BS12 | Associar professores fiscais às salas | Tela de alocação de fiscais |
| ResultadoTeste | BS13, BS14 | Lançar nota e aplicar bônus | Tela de resultados |
| Notificacao | BS13 | Visualização de notificações | Tela de notificações |

#### 1.5 Critérios de validação

- Cada classe possui vínculo com pelo menos um requisito ou caso de uso;
- As classes representam conceitos relevantes do domínio do Sistema de Gestão do Teste Progresso;
- Não são incluídas classes técnicas, como repositórios, controllers ou serviços;
- A terminologia utilizada está alinhada ao domínio do problema;
- Os relacionamentos entre as classes representam as associações identificadas nos Casos de Uso;
- As multiplicidades representam as regras de associação identificadas para o domínio;
- O modelo é consistente com o Documento de Visão, Brainstorm e Casos de Uso;
- O modelo não apresenta detalhes de implementação.





### 2) Transição para Diagrama de Classes de Especificação

#### 2.1 Objetivo
Refinar o modelo conceitual para uma estrutura orientada à implementação.

#### 2.2 Regras de refinamento

- Converter conceitos em classes de software quando aplicável;
- Definir tipos de atributos e visibilidade;
- Incluir operações principais;
- Aplicar estereótipos quando necessário (ex.: `<<entity>>`, `<<service>>`, `<<boundary>>`);
- Preservar rastreabilidade com requisitos e casos de uso.

#### 2.3 Itens esperados por classe

- **Nome da classe**;
- **Atributos** (`nome: tipo [visibilidade]`);
- **Métodos/operações** (`assinatura`);
- **Responsabilidade**;
- **Dependências e associações**;
- **Restrições/invariantes** (quando houver).


### 3) Diagrama de Classes de Especificação

#### 3.1 Conteúdo mínimo

- Classes de domínio e de apoio à aplicação;
- Interfaces relevantes;
- Associações, agregações/composições e heranças;
- Multiplicidades e navegabilidade;
- Operações alinhadas aos fluxos dos casos de uso.

#### 3.2 Rastreabilidade

| Classe de Especificação | Origem Conceitual | Requisito(s) | Caso(s) de Uso |
|---|---|---|---|
| `<ClasseSpec>` | `<ClasseConceitual>` | `RF-xx` | `UC-xx` |

#### 3.3 Critérios de qualidade

- Cobertura dos requisitos funcionais;
- Coesão alta e acoplamento controlado;
- Nomes consistentes com o domínio;
- Ausência de classes sem responsabilidade clara.


### 4) Estrutura de versionamento e revisão

- **Versão**: `v0.1`, `v0.2`...
- **Data**: `dd/mm/aaaa`
- **Autor(es)**: `<nome>`
- **Revisor(es)**: `<nome>`
- **Resumo da alteração**: `<descrição curta>`

### 5) Entregáveis

- Diagrama de Classes Conceitual (imagem + fonte);
- Diagrama de Classes de Especificação (imagem + fonte);
- Tabelas de rastreabilidade preenchidas;
- Registro de validação com equipe e stakeholders.
