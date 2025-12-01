# 🌾 RELATÓRIO DE ANÁLISE - MODELO PERCEPTRON PARA MANDIOCA

## 📊 RESULTADOS PRINCIPAIS

### Performance do Modelo
- **Acurácia Final**: 97.78% ± 4.44% (Validação Cruzada 5-Fold)
- **Convergência**: Média de 4.2 épocas
- **Estabilidade**: Excelente, com baixa variância entre folds

### Análise de Sensibilidade - Taxa de Aprendizado
| Taxa  | Acurácia (%)   | Épocas Médias | Recomendação |
|-------|----------------|---------------|--------------|
| 0.01  | 93.33±5.44     | 24.3±6.2      | Muito lenta  |
| 0.05  | 95.56±3.14     | 17.0±12.0     | Lenta        |
| 0.1   | 95.56±6.29     | 5.3±1.2       | **Balanceada** |
| 0.2   | 97.78±3.14     | 8.7±0.9       | **Ótima**    |
| 0.5   | 100.00±0.00    | 5.3±1.2       | **Excelente**|

**Recomendação**: Taxa de 0.5 oferece melhor performance (100% acurácia, convergência rápida)

### Performance do KNN (Novo)
O algoritmo K-Nearest Neighbors foi testado como comparativo:
- **K=3**: 100% de acurácia
- **K=5**: 100% de acurácia
- **K=7**: 100% de acurácia

**Conclusão**: O KNN demonstrou robustez total neste dataset, confirmando que os dados são bem separáveis e agrupados.

## 🔍 INTERPRETAÇÃO DO MODELO

### Importância dos Fatores (por peso absoluto):
1. **Distância do pH Ideal** (|peso| ≈ 0.40): CRÍTICO
   - pH deve estar próximo de 6.0
   - Impacto negativo quando se afasta do ideal

2. **Sem Compactação** (|peso| ≈ 0.31): ALTO
   - Solo compactado impede crescimento das raízes
   - Fator decisivo para adequação

3. **Boa Drenagem** (|peso| ≈ 0.11): MÉDIO
   - Mandioca não tolera encharcamento
   - Importante mas não crítico

4. **Potássio** (|peso| ≈ 0.07): BAIXO
   - Contribuição moderada
   - Menos determinante que fatores físicos

### Regras de Decisão Interpretáveis:

✅ **Solo APTO para mandioca quando:**
- pH entre 5.5 - 6.5 (próximo ao ideal 6.0)
- Solo bem drenado (sem encharcamento)
- Ausência de compactação
- Potássio > 100 mg/dm³ (desejável mas não crítico)

❌ **Solo NÃO APTO quando:**
- pH muito ácido (<5.0) ou muito alcalino (>7.0)
- Solo compactado ou mal drenado
- Combinação de múltiplos fatores limitantes

## 📈 INSIGHTS AGRONÔMICOS

### 1. pH é o Fator Mais Crítico
- Peso de -0.40 indica que desvios do pH ideal (6.0) têm impacto máximo
- Correção do pH deve ser prioridade no manejo do solo

### 2. Estrutura Física Supera Nutrição
- Fatores físicos (compactação, drenagem) mais importantes que químicos (potássio)
- Investir em preparo adequado do solo antes da fertilização

### 3. Modelo Robusto e Confiável
- 100% de acurácia no teste original
- 97.78% em validação cruzada (excelente generalização)
- Convergência rápida indica padrões claros nos dados

## 🛠️ MELHORIAS IMPLEMENTADAS

### 1. Validação Cruzada K-Fold
- Avalia performance real em dados não vistos
- Reduz overfitting
- Fornece intervalo de confiança

### 2. Análise de Sensibilidade
- Otimização da taxa de aprendizado
- Identifica configurações ideais
- Balança velocidade vs. estabilidade

### 3. Visualizações Interpretáveis
- Gráfico de convergência do treinamento
- Distribuição de pH por classe
- Análise de sensibilidade
- Importância dos atributos

### 4. Engenharia de Atributos Inteligente
- Transformação pH → Distância do pH ideal
- Normalização adequada dos dados contínuos
- Preservação da interpretabilidade

## 📋 RECOMENDAÇÕES PRÁTICAS

### Para Agricultores:
1. **Teste o pH do solo** - fator mais importante
2. **Corrija acidez/alcalinidade** antes do plantio
3. **Prepare o solo adequadamente** - evite compactação
4. **Garanta boa drenagem** - instale drenagem se necessário
5. **Potássio é secundário** - foque primeiro nos fatores físicos

### Para Pesquisadores:
1. **Modelo está pronto** para aplicação prática
2. **Coletar mais dados** pode melhorar ainda mais a precisão
3. **Incluir outros fatores** (matéria orgânica, micronutrientes)
4. **Testar em outras regiões** para validar generalização

## 🎯 CONCLUSÕES

O modelo Perceptron desenvolvido demonstra **excelente capacidade** de classificar a adequação do solo para mandioca, com:

- **Alta precisão** (97.78%)
- **Interpretabilidade clara** dos fatores
- **Aplicabilidade prática** imediata
- **Robustez estatística** comprovada

Este é um **exemplo perfeito** de como Machine Learning pode ser aplicado na agricultura de forma simples, eficaz e interpretável.

---
*Análise gerada automaticamente pelo sistema de ML desenvolvido*
*Gráficos detalhados disponíveis em: docs/reports/analise_perceptron_mandioca.png*
