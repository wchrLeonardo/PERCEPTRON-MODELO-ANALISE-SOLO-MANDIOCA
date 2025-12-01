# 🖥️ INSTRUÇÕES PARA EXECUTAR A GUI

## 🚀 Como Executar a Interface Gráfica

### Opção 1: GUI Principal (Recomendada)
```bash
python src/gui/app.py
```

### Opção 2: GUI Avançada
```bash  
python src/gui/app_advanced.py
```

## 🎯 Funcionalidades da GUI

### ✨ Interface Principal
- 🌾 **Título profissional** com tema agrícola
- 📊 **Status do sistema** em tempo real
- 📝 **Campos organizados** para entrada de dados
- 🎨 **Design moderno** com cores temáticas

### 📊 Entrada de Dados
- 🧪 **pH do Solo**: Campo numérico (ex: 6.0)
- ⚡ **Potássio**: Campo inteiro (ex: 120 mg/dm³)
- 💧 **Drenagem**: Botões de opção (Sim/Não)
- 🏔️ **Compactação**: Botões de opção (Ausente/Presente)

### 🔍 Controles
- 🟢 **ANALISAR SOLO**: Botão principal para análise
- 🗑️ **LIMPAR**: Limpa todos os campos
- 📝 **CARREGAR EXEMPLO**: Insere dados de teste

### 📈 Resultados
- 📋 **Relatório completo** com análise detalhada
- 🎯 **Nível de confiança** da predição
- 💡 **Recomendações técnicas** personalizadas
- 📊 **Dados processados** exibidos claramente

## 🛠️ Funcionalidades Técnicas

### 🤖 Sistema de IA
- ✅ **Carregamento automático** do modelo
- 🔄 **Treinamento em background** 
- ⚡ **Predição instantânea**
- 📊 **Validação de dados** robusta

### 🎨 Interface
- 🖼️ **Layout responsivo** 
- 🎨 **Cores temáticas** (verde agricultura)
- 📱 **Controles intuitivos**
- 🔒 **Validação de entrada**

### 📊 Relatórios
- 📈 **Análise detalhada** por fator
- 💡 **Recomendações agronômicas** específicas
- 🎯 **Confiança da predição**
- 📋 **Formato profissional**

## 🔧 Solução de Problemas

### Erro: "Módulo não encontrado"
```bash
pip install -r requirements.txt
```

### Erro: "Arquivo não encontrado"  
- ✅ Certifique-se que `data/entrada_mandioca.csv` está na pasta
- ✅ Execute dentro da pasta raiz do projeto

### Erro: "ImportError"
- ✅ Verifique se a estrutura de pastas está correta (`src/`, `data/`, etc.)
- ✅ Execute a partir da raiz do projeto

## 🎓 Exemplo de Uso

### 1. Executar GUI
```bash
# Na raiz do projeto
python src/gui/app.py
```

### 2. Aguardar Carregamento
- Status: "🔄 Carregando dados..."
- Status: "🤖 Treinando modelo..."  
- Status: "✅ Sistema pronto!"

### 3. Inserir Dados
- pH: 6.2
- Potássio: 155
- Drenagem: Sim
- Compactação: Ausente (Sim)

### 4. Analisar
- Clique em "🔍 ANALISAR SOLO"
- Veja resultado detalhado
- Leia recomendações

## 🌟 Recursos Especiais

### 🎯 Validação Inteligente
- Campos obrigatórios verificados
- Ranges válidos aplicados
- Mensagens de erro claras

### 📊 Análise Profissional
- Classificação por níveis (Excelente/Bom/Moderado/Problemático)
- Recomendações técnicas específicas
- Dosagens de corretivos sugeridas

### 🎨 UX/UI Moderna
- Cores harmoniosas
- Ícones intuitivos
- Layout organizado
- Feedback visual

---

## 🎉 Sistema Completo Pronto!

A GUI oferece uma experiência profissional e intuitiva para análise de solo, transformando seu excelente modelo de Perceptron em uma ferramenta prática para agricultores e técnicos!

**Execute `python src/gui/app.py` e teste agora! 🚀**
