# 🚀 PROJETO COMPLETO: ANÁLISE DE SOLO PARA MANDIOCA (PERCEPTRON & KNN)

## 📄 **RELATÓRIOS EM PDF**

> **🎯 [RELATÓRIO FINAL (PERCEPTRON)](./docs/reports/RELATORIO_PERCEPTRON_MANDIOCA_ABNT.pdf)**
>
> **🎯 [RELATÓRIO COMPARATIVO (KNN)](./docs/reports/RELATORIO_KNN_MANDIOCA_ABNT.pdf)**

### 📊 **Conteúdo dos Relatórios Técnicos (Normas ABNT)**
- ✅ **Introdução completa** com contextualização do problema
- ✅ **Metodologia detalhada** (Perceptron e KNN)
- ✅ **Base de dados** com exemplos e estatísticas
- ✅ **Resultados** com validação cruzada e análise comparativa
- ✅ **Discussão crítica** (vantagens, limitações, melhorias)
- ✅ **Conclusões** e aplicações práticas
- ✅ **Referências bibliográficas**

**📋 Desenvolvido por:**
- João Pedro Dias Barreto
- Leonardo Wicher Lopes Ferreira

---

## 🛠️ Configuração do Ambiente

Para garantir que todas as dependências funcionem corretamente, recomenda-se o uso de um ambiente virtual.

### 1. Criar e Ativar o Ambiente Virtual
```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual (Linux/Mac)
source venv/bin/activate

# Ativar o ambiente virtual (Windows)
venv\Scripts\activate
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

---

## 📁 Arquivos do Projeto

### 🧠 Modelos de IA
1.  **`src/models/knn.py` (NOVO)**: Implementação do algoritmo K-Nearest Neighbors (KNN) do zero.
    *   Testa K=3, 5 e 7.
    *   **Resultado: 100% de acurácia.**
2.  **`src/models/perceptron_cv.py`**: Perceptron com validação cruzada e gráficos.
3.  **`src/models/perceptron.py`**: Implementação base do Perceptron.

### 📝 Relatórios e Documentação
1.  **`src/utils/pdf_generator_knn.py`**: Gera o relatório comparativo em PDF.
2.  **`src/utils/pdf_generator_perceptron.py`**: Gera o relatório do Perceptron em PDF.
3.  **`docs/RELATORIO_COMPLETO.md`**: Versão em Markdown dos resultados.
4.  **`docs/INSTRUCOES_GUI.md`**: Manual da interface gráfica.

### 🖥️ Interfaces
1.  **`src/gui/app.py`**: Interface gráfica moderna (Recomendada).
2.  **`src/utils/cli.py`**: Interface via terminal.

---

## 🎯 COMO USAR

### 1. Executar Análise KNN (Novo)
```bash
python src/models/knn.py
```

### 2. Gerar Relatórios PDF
```bash
# Relatório KNN
python src/utils/pdf_generator_knn.py

# Relatório Perceptron
python src/utils/pdf_generator_perceptron.py
```

### 3. Usar a Interface Gráfica
```bash
python src/gui/app.py
```

---

## 🏆 RESULTADOS COMPARATIVOS

| Modelo | Acurácia | Características |
| :--- | :--- | :--- |
| **KNN (K=3,5,7)** | **100.00%** | Não-linear, baseado em instâncias, robusto. |
| **Perceptron** | **97.78%** | Linear, leve, interpretável. |

Ambos os modelos demonstraram excelente desempenho, validando a qualidade da base de dados e a aplicabilidade de ML na agricultura de precisão.

---

## 📞 CONTATO E SUPORTE

Para dúvidas sobre implementação, melhorias ou aplicações práticas, este projeto serve como base sólida para:
- Trabalhos acadêmicos em IA/ML
- Aplicações em agricultura de precisão  
- Estudos de caso em interpretabilidade de ML
- Desenvolvimento de sistemas de apoio à decisão rural

**Parabéns pelo excelente trabalho desenvolvido!** 🎉

---

*Projeto desenvolvido com foco em qualidade, aplicabilidade e impacto social.*
