---
id: diagrama_de_sequencia
title: Diagrama de Sequência
---

## Diagrama de Sequência

O Diagrama de Sequência é uma representação visual que mostra a interação entre objetos ou componentes ao longo do tempo. Ele é usado para modelar o comportamento dinâmico de um sistema, ilustrando como os objetos colaboram para realizar uma funcionalidade específica.

#### Objetivo

Definir um padrão para elaboração e registro dos Diagramas de Sequência, garantindo rastreabilidade com:

- Casos de Uso;
- Diagrama de Casos de Uso;
- Documento de Levantamento de Requisitos;
- Protótipo de Baixa Fidelidade.

#### Instruções de Preenchimento

1. Selecione um Caso de Uso prioritário.
2. Identifique os requisitos funcionais e regras de negócio relacionados.
3. Mapeie as telas/fluxos no protótipo de baixa fidelidade.
4. Modele a interação entre ator(es), fronteira, controle e entidade.
5. Valide consistência com o fluxo principal e fluxos alternativos.

---

### 1. Identificação

- **Caso de Uso:** Inscrever-se no Teste Progresso e escolher matéria do bônus
- **ID do Caso de Uso:** UC03
- **Ator(es):** Aluno, Sistema
- **Prioridade:** Alta
- **Responsável:** Bento, Carlos, Julia e Lucas
- **Data:** 27/09/2026

### 2. Referências

- **Requisitos relacionados (ID):** BS05, BS13
- **Diagrama de Caso de Uso (link/imagem):** Diagrama de Casos de Uso do Sistema de Gestão do Teste Progresso
- **Protótipo de Baixa Fidelidade (tela/fluxo):** Tela de Inscrição no Teste Progresso
- **Regra(s) de negócio associada(s):**
  - O aluno deve estar cadastrado e autenticado;
  - O período de inscrição deve estar aberto;
  - O aluno deve estar matriculado em pelo menos uma matéria;
  - O aluno deve escolher exatamente uma matéria para receber o bônus;
  - A matéria escolhida pode ser alterada enquanto o período de inscrição estiver aberto.

### 3. Cenário Modelado

- **Objetivo do cenário:** Permitir que o aluno realize sua inscrição no Teste Progresso e escolha uma matéria para receber o bônus.
- **Pré-condições:**
  - O aluno possui uma conta cadastrada;
  - O aluno está autenticado no sistema;
  - O período de inscrição está aberto;
  - O aluno está matriculado em pelo menos uma matéria.
- **Pós-condições:**
  - A inscrição do aluno no Teste Progresso é registrada;
  - A matéria escolhida para o bônus fica vinculada à inscrição;
  - O sistema apresenta uma confirmação ao aluno.
- **Gatilho de início:** O aluno acessa a funcionalidade de inscrição no Teste Progresso.

### 4. Participantes (Lifelines)

- **Ator:** Aluno
- **Boundary (Interface/Tela):** Tela de Inscrição
- **Control (Orquestração):** Controle de Inscrição
- **Entity (Dados/Serviços):**
  - Aluno;
  - TesteProgresso;
  - Materia;
  - Inscricao.
- **Sistemas externos (se houver):** Nenhum.

### 5. Fluxo Principal (mensagens)

| **Passo** | **Remetente** | **Destinatário** | **Mensagem/Ação** | **Tipo (sync/async/retorno)** |
| --------- | ------------- | ---------------- | ----------------- | ----------------------------- |
| 1 | Aluno | Tela de Inscrição | Solicita inscrição no Teste Progresso | sync |
| 2 | Tela de Inscrição | Controle de Inscrição | Solicita dados disponíveis para inscrição | sync |
| 3 | Controle de Inscrição | TesteProgresso | Consulta situação do período de inscrição | sync |
| 4 | TesteProgresso | Controle de Inscrição | Retorna período de inscrição disponível | retorno |
| 5 | Controle de Inscrição | Aluno | Consulta matérias em que está matriculado | sync |
| 6 | Aluno | Controle de Inscrição | Retorna matérias disponíveis para seleção | retorno |
| 7 | Controle de Inscrição | Tela de Inscrição | Apresenta matérias disponíveis | retorno |
| 8 | Tela de Inscrição | Aluno | Exibe matérias disponíveis para escolha | retorno |
| 9 | Aluno | Tela de Inscrição | Seleciona uma matéria para receber o bônus | sync |
| 10 | Tela de Inscrição | Controle de Inscrição | Envia matéria escolhida | sync |
| 11 | Controle de Inscrição | Materia | Valida matéria selecionada | sync |
| 12 | Materia | Controle de Inscrição | Retorna confirmação da matéria válida | retorno |
| 13 | Controle de Inscrição | Inscricao | Registra a inscrição e a matéria escolhida | sync |
| 14 | Inscricao | Controle de Inscrição | Retorna confirmação do registro | retorno |
| 15 | Controle de Inscrição | Tela de Inscrição | Informa que a inscrição foi realizada com sucesso | retorno |
| 16 | Tela de Inscrição | Aluno | Apresenta confirmação da inscrição e da matéria escolhida | retorno |

### 6. Fluxos Alternativos e Exceções

| **ID** | **Condição** | **Descrição do fluxo** | **Impacto** |
| ------ | ------------ | ---------------------- | ----------- |
| A1 | O aluno altera a matéria escolhida durante o período de inscrição | O aluno seleciona outra matéria. A Tela de Inscrição envia a nova escolha ao Controle de Inscrição, que atualiza a matéria vinculada à inscrição. | A matéria escolhida anteriormente é substituída pela nova matéria. |
| A2 | O aluno não possui matérias em curso | O sistema verifica que não existem matérias disponíveis para o aluno. | A inscrição não pode ser realizada e o sistema informa a situação ao aluno. |
| E1 | O período de inscrição está encerrado | O Controle de Inscrição verifica que o período não está mais aberto. | A inscrição não é realizada e o aluno recebe uma mensagem informando que o período está encerrado. |
| E2 | O aluno não seleciona uma matéria | O aluno tenta concluir a inscrição sem escolher uma matéria para o bônus. | A inscrição não é concluída e o sistema solicita a seleção de uma matéria. |

### 7. Regras de Negócio Aplicadas

- **RN-01:** O aluno deve estar cadastrado e autenticado para realizar a inscrição.
- **RN-02:** A inscrição somente pode ser realizada durante o período definido para o Teste Progresso.
- **RN-03:** O aluno deve estar matriculado em pelo menos uma matéria para realizar a inscrição.
- **RN-04:** O aluno deve escolher exatamente uma matéria para receber o bônus.
- **RN-05:** A matéria escolhida pode ser alterada enquanto o período de inscrição estiver aberto.
- **RN-06:** A inscrição deve permanecer vinculada ao aluno, ao Teste Progresso e à matéria escolhida.

### 8. Pontos de Validação

- [x] Fluxo compatível com Caso de Uso;
- [x] Mensagens consistentes com os requisitos identificados;
- [x] Alternativas e exceções representadas;
- [x] Participantes aderentes à arquitetura;
- [x] Correspondência com o fluxo de inscrição do sistema;
- [x] Regras de negócio representadas no fluxo;
- [x] Interações organizadas temporalmente;
- [x] Não foram incluídos componentes externos não previstos no sistema.

### 9. Artefatos

- **Imagem do Diagrama de Sequência:** gerada a partir do código PlantUML;
- **Arquivo fonte (PlantUML):** `docs/Elaboracao/diagrama_de_sequencia.puml`;
- **Versão:** 1.0.
