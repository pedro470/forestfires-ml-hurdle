# Forest Fires — Modelagem Preditiva, Regularização L2 (Ridge) e Modelo Hurdle

Análise exploratória, engenharia de atributos e modelagem estatística/Machine Learning sobre o clássico dataset **Forest Fires** (*UCI Machine Learning Repository* — Parque Natural de Montesinho, Portugal, $N = 517$), investigando o problema de **inflação de zeros** na variável resposta (`area`) e comparando **Regressão Linear Ordinária (OLS)**, **Regressão Ridge (`RidgeCV`)** e um **Modelo em Duas Etapas (*Hurdle Model*)**.

---

## Principais Descobertas & Rigor Estatístico

1. **Inflação de Zeros e Alvo Semicontínuo:**
   - Embora a transformação $\log(1 + \text{area})$ reduza a assimetria global de $12{,}8$ para $1{,}2$, **247 dos 517 registros ($47{,}8\%$) possuem $\text{area} = 0{,}00\text{ ha}$** (incêndios com área queimada inferior a $0{,}01\text{ ha}$).
   - Isolando os $270$ incêndios com área positiva ($\text{area} > 0$), a distribuição de $\log(\text{area})$ torna-se praticamente normal (*skewness* $= 0{,}30$, teste de **Shapiro-Wilk** com $p \approx 0{,}24$ e transformação **Box-Cox** estimando $\lambda \approx 0$).

2. **Pipeline de Pré-processamento sem Vazamento de Dados (*Data Leakage*):**
   - Remoção de preditores com variância quase nula (`rain`, com $98{,}5\%$ de zeros).
   - Agrupamento de categorias raras em `month` (meses com $< 10$ ocorrências consolidados em `outros` para evitar ajuste de *dummies* em ruído amostral).
   - *One-Hot Encoding* (`drop_first=True`, gerando 22 preditores), divisão treino/teste ($80/20$) e padronização com `StandardScaler` encapsulado em `sklearn.pipeline.Pipeline` durante a validação cruzada de 10 dobras (`10-fold KFold`).

3. **Comparativo de Modelos (OLS vs. Ridge vs. Baseline):**

| Modelo | RMSE Treino | RMSE Teste | MAE Teste | $R^2$ Teste | CV RMSE (10-Fold) |
|---|---|---|---|---|---|
| **Baseline (`DummyRegressor` — média)** | `1,3746` | `1,4830` | `1,2028` | `-0,0006` | `1,3878 ± 0,1735` |
| **Regressão Linear (OLS)** | `1,3382` | `1,4610` | `1,1736` | `0,0288` | `1,4000 ± 0,1577` |
| **Regressão Ridge ($\alpha = 10^4$)** | `1,3721` | `1,4812` | `1,2018` | `0,0018` | `1,3869 ± 0,1729` |

   - O `RidgeCV` (testado em malha logarítmica de $200$ valores de $\alpha \in [10^{-3}, 10^4]$) converge para o teto da regularização ($\alpha = 10^4$), encolhendo os coeficientes para próximo de zero e demonstrando que o ganho aparente do OLS no *holdout* é ruído amostral.

4. **Decomposição em Duas Etapas (*Hurdle Model*):**
   - **Etapa 1 — Classificação Binária (`LogisticRegression`, $\text{area} > 0{,}01\text{ ha}$):** Avaliada via previsões fora da dobra (`cross_val_predict`, 10-fold), obtendo $\text{ROC-AUC} = 0{,}534$ e $\text{Acurácia} = 54{,}2\%$ (próximo ao baseline da classe majoritária de $52{,}2\%$).
   - **Etapa 2 — Regressão Condicional nos Positivos (`Ridge` sobre os 270 casos com $\text{area} > 0$):** $\text{RMSE} = 1{,}547$ contra $1{,}527$ da média condicional.
   - **Conclusão Técnica:** O modelo em duas partes comprova que as variáveis meteorológicas de ignição e os índices FWI isolados não contêm sinal linear suficiente para prever a extensão final do fogo sem variáveis operacionais e topográficas (tempo de resposta do combate, declividade e tipo de vegetação).

---

## Stack Tecnológica

- **Linguagem:** Python 3.12+
- **Ciência de Dados & Modelagem:** `pandas`, `numpy`, `scikit-learn` (`LinearRegression`, `Ridge`, `RidgeCV`, `LogisticRegression`, `DummyRegressor`, `StandardScaler`, `KFold`, `cross_val_score`, `cross_val_predict`, `make_pipeline`), `scipy.stats` (Shapiro-Wilk, Box-Cox)
- **Visualização & Relatórios Automatizados:** `matplotlib`, `seaborn`, `reportlab` e `Pillow` (geração programática do handout executivo em PDF)

---

## Estrutura do Repositório

- `analise_forestfires_v2.ipynb` — Notebook principal com toda a análise exploratória, testes de hipótese, pipelines de regressão e modelo Hurdle.
- `analise_forestfires_v2_executado.ipynb` — Versão executada com todas as saídas e gráficos renderizados.
- `extrair_figuras.py` — Script utilitário que extrai os gráficos em alta resolução (`.png`) diretamente dos metadados do notebook executado.
- `gerar_pdf_v2.py` — Gerador automatizado em `reportlab` que compila o relatório técnico diagramado.
- `relatorio_forestfires_v2.pdf` — Relatório técnico final em PDF pronto para leitura.
- `forestfires.csv` — Dataset original (*Cortez & Morais, 2007*).

---

## Como Reproduzir

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Extrair figuras do notebook executado e gerar o relatório em PDF
python extrair_figuras.py analise_forestfires_v2_executado.ipynb
python gerar_pdf_v2.py
```
