# 🧠 Projeto de Análise Automatizada do Teste Torre de Londres

## 🎯 Objetivo do Sistema

O sistema foi desenvolvido para **avaliar automaticamente o desempenho de participantes** no **Teste Torre de Londres (ToL)**. Ele recebe arquivos com os dados de testes aplicados e calcula:

- A **quantidade mínima de movimentos necessários** para resolver cada tarefa do teste;
- A **pontuação do participante** com base na eficiência dos movimentos realizados.
## 🧠 O que é o Teste da Torre de Londres?

O **Teste da Torre de Londres** é uma tarefa clássica usada para avaliar **funções executivas**, como **planejamento**, **organização** e **controle inibitório**.

A atividade consiste em:

- Mover **bolas coloridas** entre **pinos de diferentes alturas**;
- Alcançar uma **configuração final específica**;
- Respeitar **restrições** como:
  - Apenas a bola do topo pode ser movida;
  - Há uma **quantidade máxima de bolas por pino**.

É amplamente utilizado em **neuropsicologia**, especialmente na avaliação de pessoas com distúrbios cognitivos, lesões cerebrais ou transtornos como TDAH e Parkinson.

---

## ⚙️ Como funciona o sistema

### 📥 Leitura dos dados

O sistema lê uma tabela contendo os seguintes campos para cada etapa do teste:

- `current`: estado inicial (como estavam dispostas as bolas no começo);
- `end`: estado final desejado;
- `step`: número de movimentos feitos pelo participante;
- `done`: indica se a tarefa foi concluída corretamente (`1`) ou não (`0`);
- `size`: altura máxima permitida dos pinos (quantas bolas cabem em cada um).

---

### 🔁 Cálculo dos movimentos mínimos

O sistema utiliza um algoritmo que simula todas as possíveis sequências de movimentos válidas e **encontra a mais curta** (em quantidade de ações) que leva do estado inicial ao estado final.

Esse cálculo considera:

- A **ordem das bolas**;
- A **altura máxima de cada pino**;
- Que **somente a bola do topo** pode ser movida (como em uma pilha).

Se não for possível atingir o estado final com as regras fornecidas, o sistema registra `-1` como resultado.

---

### 🧮 Pontuação do participante

A pontuação começa em **10 pontos por tarefa**. Para cada movimento além do mínimo necessário, um ponto é descontado.

Exemplo:
- Mínimo de movimentos: `4`
- Movimentos realizados: `6`  
→ Pontuação: `10 - (6 - 4) = 8 pontos`

Se o participante **não resolver corretamente** (`done = 0`) ou se a tarefa for **impossível** (`mínimo = -1`), a pontuação é `0`.

---

## ✅ Testes Automatizados

O projeto contém um conjunto de **testes automáticos com `pytest`** que têm como objetivo garantir que o sistema funcione corretamente em todas as situações importantes — simples, complexas, limites e inválidas.

Eles funcionam como uma "**prova matemática prática**" de que o algoritmo está fazendo o que se espera.

---

### 🔍 O que está sendo testado?

#### ✔️ Conversão de texto para estado (`string_para_estado`)

Garante que a entrada da planilha (como `|AB||C|`) é corretamente transformada em uma estrutura interna válida:
- Exemplo: `|AB||C|` → `[['A', 'B'], [], ['C']]`

Também são testadas entradas **inválidas**, para garantir que o sistema rejeite formatos incorretos.

---

#### ✔️ Normalização de estados (`normalizar_estados`)

Verifica se estados incompletos são automaticamente preenchidos com pinos vazios:
- Exemplo: Entrada `[['A'], ['B']]` → Resultado: `[['A'], ['B'], []]`

Isso garante que sempre haja **três pinos**, como no teste original.

---

#### ✔️ Cálculo dos movimentos mínimos (`movimentos_minimos`)

A parte mais crítica do sistema, testada com diversos cenários:

- Casos simples com 1 ou 2 bolas;
- Casos complexos com 3 ou 4 bolas;
- Casos simétricos (esquerda → direita e vice-versa);
- Casos impossíveis (por limitação da altura dos pinos);
- Casos com número exato conhecido de movimentos mínimos.

Exemplo de caso testado:
```python
([['R', 'G', 'B'], [], []], [[], [], ['R', 'G', 'B']], 3, 5)
```

> Significa reorganizar 3 bolas do primeiro pino para o último, com altura máxima de 3.  
> O sistema deve encontrar **exatamente 5 movimentos mínimos**. Se retornar outro valor, o teste falha.

---

### ✔️ Casos-limite e desempenho

Verifica se o sistema funciona corretamente em tarefas que exigem **muitos movimentos**, como **9 ou mais**.  
Isso assegura que o algoritmo **não entre em loop** nem trave com tarefas mais longas.

---

### 📌 Eficácia dos testes

Os testes cobrem:

- ✅ Casos simples (1 ou 2 bolas);
- ✅ Casos complexos (até 5 bolas);
- ✅ Casos simétricos (para verificar consistência);
- ✅ Casos inválidos (para testar robustez);
- ✅ Casos limite (para garantir desempenho).

Se **todos esses testes forem executados com sucesso**, podemos afirmar com confiança que:

> 🔐 **O algoritmo resolve corretamente qualquer situação realista do Teste Torre de Londres, respeitando todas as regras envolvidas.**

