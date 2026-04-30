# 🏭 Sistema de Automação Digital — Gestão de Peças, Qualidade e Armazenamento

Protótipo desenvolvido em **Python** para a disciplina de **Algoritmos e Lógica de Programação** (UniFECAF), simulando um sistema de controle de produção e qualidade em uma linha de montagem industrial.

O projeto contém **duas versões** com a mesma lógica:

- **`main.py`** — versão Python para terminal (entrega oficial do trabalho).
- **`index.html`** — versão web com a mesma lógica em JavaScript, hospedável no Netlify/Vercel para demonstração.

---

## 📋 Sobre o Projeto

O sistema automatiza o processo de inspeção e armazenamento de peças produzidas, substituindo a conferência manual por uma rotina lógica que:

- Cadastra peças com seus dados (id, peso, cor, comprimento).
- Avalia automaticamente se a peça é **aprovada** ou **reprovada** segundo critérios de qualidade.
- Armazena as peças aprovadas em **caixas com capacidade limitada (10 peças)**.
- **Fecha** a caixa ao atingir a capacidade e **inicia uma nova** automaticamente.
- Gera **relatórios consolidados** com totais, motivos de reprovação e quantidade de caixas utilizadas.

---

## ✅ Critérios de Aprovação

Para uma peça ser aprovada, ela deve atender **simultaneamente** aos três critérios:

| Critério | Faixa aceita |
| --- | --- |
| **Peso** | entre 95g e 105g |
| **Cor** | azul **ou** verde |
| **Comprimento** | entre 10cm e 20cm |

Se qualquer critério falhar, a peça é reprovada e o sistema registra **todos os motivos** (não só o primeiro).

---

## 🧠 Como o Sistema Funciona

Menu interativo no terminal com 5 opções:

1. **Cadastrar nova peça** — solicita os dados, avalia e, se aprovada, coloca na caixa atual.
2. **Listar peças aprovadas/reprovadas** — mostra todas as peças, separadas por status.
3. **Remover peça cadastrada** — remove pelo ID e reorganiza as caixas.
4. **Listar caixas fechadas** — mostra cada caixa fechada e a caixa em montagem.
5. **Gerar relatório final** — relatório consolidado da operação.
0. **Sair** — encerra o programa.

---

## 🚀 Como Executar (Versão Python — Terminal)

### Pré-requisitos
- **Python 3.7+** instalado.
- Nenhuma biblioteca externa (apenas a biblioteca padrão).

### Passo a passo

1. Clone ou baixe o repositório:
   ```bash
   git clone <URL-DO-REPOSITORIO>
   cd Gestao_de_Pecas
   ```

2. Verifique a versão do Python:
   ```bash
   python --version
   ```

3. Execute:
   ```bash
   python main.py
   ```

4. Use o menu interativo digitando o número da opção e pressionando **Enter**.

---

## 🌐 Como Hospedar a Versão Web (Netlify ou Vercel)

A versão web (`index.html`) é um arquivo único, sem backend, sem instalação — só HTML + CSS + JavaScript. Os dados ficam salvos no navegador (localStorage).

### Opção 1 — Netlify (mais simples)

1. Acesse [https://app.netlify.com/drop](https://app.netlify.com/drop).
2. **Arraste a pasta do projeto** para a página.
3. Pronto — o Netlify gera um link tipo `https://nome-aleatorio.netlify.app`.

### Opção 2 — Vercel

1. Crie conta em [https://vercel.com](https://vercel.com).
2. Conecte o repositório do GitHub (após fazer push).
3. A Vercel detecta automaticamente como site estático e publica.

### Opção 3 — GitHub Pages

1. Suba o projeto para um repositório no GitHub.
2. Em **Settings → Pages**, selecione `main` como branch.
3. O site fica disponível em `https://seu-usuario.github.io/Gestao_de_Pecas/`.

---

## 💻 Exemplos de Entrada e Saída (Versão Python)

### Exemplo 1 — Peça aprovada
```
Escolha uma opção: 1

--- Cadastro de Nova Peça ---
ID da peça: P001
Peso (g): 100
Cor: azul
Comprimento (cm): 15

  ✅ Peça 'P001' APROVADA.
```

### Exemplo 2 — Peça reprovada (múltiplos motivos)
```
ID da peça: P006
Peso (g): 85
Cor: rosa
Comprimento (cm): 5

  ❌ Peça 'P006' REPROVADA. Motivos:
     - peso fora do intervalo (85.0g, esperado 95.0-105.0g)
     - cor não permitida ('rosa', esperado azul ou verde)
     - comprimento fora do intervalo (5.0cm, esperado 10.0-20.0cm)
```

### Exemplo 3 — Fechamento automático de caixa
```
  ✅ Peça 'P010' APROVADA.
  📦 Caixa #1 fechada com 10 peças. Iniciando nova caixa.
```

### Exemplo 4 — Relatório final
```
=======================================================
           RELATÓRIO CONSOLIDADO DE PRODUÇÃO
=======================================================

Total de peças processadas: 6
  ✅ Aprovadas: 2
  ❌ Reprovadas: 4

Detalhamento das reprovações:
  - Peça 'P002':
      · peso fora do intervalo (90.0g, esperado 95.0-105.0g)
  ...

Resumo por tipo de falha:
  · peso fora do intervalo: 2 ocorrência(s)
  · cor não permitida: 2 ocorrência(s)
  · comprimento fora do intervalo: 2 ocorrência(s)

Armazenamento:
  📦 Caixas fechadas: 0
  📋 Peças na caixa atual (não fechada): 2/10
  Total de caixas utilizadas: 1

Taxa de aprovação: 33.3%
=======================================================
```

---

## 📁 Estrutura do Projeto

```
.
├── main.py        # Versão Python (terminal) — entrega oficial
├── index.html     # Versão web (Netlify/Vercel) — bônus para o pitch
└── README.md      # Este arquivo
```

---

## 🛠 Boas Práticas Aplicadas

- **Constantes nomeadas** no topo (`PESO_MIN`, `CAPACIDADE_CAIXA`, etc.) — facilita manutenção.
- **Funções pequenas com responsabilidade única** — cada opção do menu é uma função.
- **Validação de entrada** com `try/except` para evitar quebras.
- **Separação clara** entre regra de negócio, armazenamento e interface.
- **Comentários e docstrings** explicando cada bloco lógico.
- **Estruturas de dados nativas** (listas e dicionários) — sem dependências externas.

---

## 🔭 Reflexão Final — Expansão para Cenário Real

Este protótipo é a base lógica de um sistema industrial de verdade. Em produção, ele poderia ser expandido com:

- **Sensores físicos** (balança, câmera, sensor a laser) substituindo o input manual.
- **Visão computacional / IA** classificando cor e detectando defeitos visuais.
- **Banco de dados** (PostgreSQL, MongoDB) para histórico de longo prazo.
- **Dashboard web** em tempo real com indicadores de qualidade (OEE, FPY).
- **Integração MES/ERP** alimentando o sistema corporativo automaticamente.
- **Alertas** quando a taxa de reprovação ultrapassa um limite.

---

## 📚 Referências

- Disciplina **Algoritmos e Lógica de Programação** — UniFECAF
- [Documentação oficial do Python](https://docs.python.org/3/)
- [Comunidade Python Brasil](https://python.org.br/)
