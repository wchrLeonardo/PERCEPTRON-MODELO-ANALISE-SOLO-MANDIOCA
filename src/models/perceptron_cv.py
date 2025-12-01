import random
import math
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# CLASSE PERCEPTRON APRIMORADA

class PerceptronAprimorado:
    def __init__(self, num_entradas, taxa_aprendizado=0.1):
        self.taxa_aprendizado = taxa_aprendizado
        self.pesos = [random.uniform(-0.5, 0.5) for _ in range(num_entradas)]
        self.bias = random.uniform(-0.5, 0.5)
        self.historico_pesos = []
        self.historico_erros = []

    def _funcao_ativacao_degrau(self, soma_ponderada):
        return 1 if soma_ponderada >= 0 else 0

    def prever(self, entradas):
        soma_ponderada = self.bias
        for i in range(len(self.pesos)):
            soma_ponderada += self.pesos[i] * entradas[i]
        return self._funcao_ativacao_degrau(soma_ponderada)

    def treinar(self, dados_treino, rotulos_treino, epocas=100, verbose=True):
        if verbose:
            print(f"--- Iniciando Treinamento com {epocas} épocas ---")
        
        for epoca in range(epocas):
            erros_epoca = 0
            # Salva estado dos pesos para análise
            self.historico_pesos.append(self.pesos.copy() + [self.bias])
            
            for entradas, rotulo_esperado in zip(dados_treino, rotulos_treino):
                previsao = self.prever(entradas)
                erro = rotulo_esperado - previsao
                if erro != 0:
                    erros_epoca += 1
                    self.bias += self.taxa_aprendizado * erro
                    for i in range(len(self.pesos)):
                        self.pesos[i] += self.taxa_aprendizado * erro * entradas[i]
            
            self.historico_erros.append(erros_epoca)
            
            if verbose and (epoca + 1) % 10 == 0:
                print(f"> Época {epoca + 1}/{epocas} - Erros: {erros_epoca}")

            if erros_epoca == 0:
                if verbose:
                    print(f"\n--- Treinamento concluído na época {epoca + 1}: modelo convergiu! ---")
                return epoca + 1
        
        if verbose:
            print("\n--- Treinamento finalizado (limite de épocas atingido). ---")
        return epocas

# FUNÇÕES DE PRÉ-PROCESSAMENTO

def carregar_dados_brutos(caminho_arquivo):
    """Lê um arquivo CSV e o converte para o formato bruto (strings)."""
    dataset = []
    with open(caminho_arquivo, 'r') as file:
        next(file) # Pula cabeçalho
        for linha in file:
            dataset.append(linha.strip().split(','))
    return dataset

def pre_processar_dados(dataset):
    """Converte, aplica engenharia de atributos e normaliza o dataset."""
    dados_processados = []
    
    # 1. Converter strings para números
    dados_numericos = []
    for linha in dataset:
        dados_numericos.append([float(linha[0]), int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4])])
    
    # Separa características (X) dos rótulos (y)
    X_bruto = [linha[:-1] for linha in dados_numericos]
    y = [linha[-1] for linha in dados_numericos]
    
    # 2. Engenharia de Atributos: Substituir pH pela distância ao ideal (6.0)
    for i in range(len(X_bruto)):
        ph_valor = X_bruto[i][0]
        distancia_ph = abs(ph_valor - 6.0)
        X_bruto[i][0] = distancia_ph
    
    # 3. Normalização Min-Max
    min_vals = [float('inf')] * 2
    max_vals = [float('-inf')] * 2
    
    for linha in X_bruto:
        for i in range(2):
            if linha[i] < min_vals[i]: min_vals[i] = linha[i]
            if linha[i] > max_vals[i]: max_vals[i] = linha[i]
            
    # Aplica a normalização
    X_normalizado = []
    for linha in X_bruto:
        linha_norm = []
        for i in range(2):
            if (max_vals[i] - min_vals[i]) == 0:
                norm_val = 0
            else:
                norm_val = (linha[i] - min_vals[i]) / (max_vals[i] - min_vals[i])
            linha_norm.append(norm_val)
        
        linha_norm.extend(linha[2:])
        X_normalizado.append(linha_norm)
        
    return X_normalizado, y, min_vals, max_vals

# FUNÇÕES DE ANÁLISE E VISUALIZAÇÃO
def validacao_cruzada_k_fold(X, y, k=5, taxa_aprendizado=0.1, epocas=200):
    """Implementa validação cruzada k-fold."""
    print(f"\n--- Validação Cruzada {k}-Fold ---")
    
    n = len(X)
    indices = list(range(n))
    random.shuffle(indices)
    
    fold_size = n // k
    acuracias = []
    epocas_convergencia = []
    
    for fold in range(k):
        print(f"\nFold {fold + 1}/{k}:")
        
        # Divisão dos dados
        inicio_teste = fold * fold_size
        fim_teste = inicio_teste + fold_size if fold < k-1 else n
        
        indices_teste = indices[inicio_teste:fim_teste]
        indices_treino = [i for i in indices if i not in indices_teste]
        
        X_treino = [X[i] for i in indices_treino]
        y_treino = [y[i] for i in indices_treino]
        X_teste = [X[i] for i in indices_teste]
        y_teste = [y[i] for i in indices_teste]
        
        # Treinamento
        perceptron = PerceptronAprimorado(len(X[0]), taxa_aprendizado)
        epocas_conv = perceptron.treinar(X_treino, y_treino, epocas, verbose=False)
        epocas_convergencia.append(epocas_conv)
        
        # Teste
        acertos = 0
        for i in range(len(X_teste)):
            previsao = perceptron.prever(X_teste[i])
            if previsao == y_teste[i]:
                acertos += 1
        
        acuracia = (acertos / len(X_teste)) * 100
        acuracias.append(acuracia)
        print(f"  Acurácia: {acuracia:.2f}% | Convergiu em: {epocas_conv} épocas")
    
    print(f"\n--- Resultados da Validação Cruzada ---")
    print(f"Acurácia Média: {np.mean(acuracias):.2f}% ± {np.std(acuracias):.2f}%")
    print(f"Épocas de Convergência Média: {np.mean(epocas_convergencia):.1f} ± {np.std(epocas_convergencia):.1f}")
    
    return acuracias, epocas_convergencia

def analise_sensibilidade_taxa_aprendizado(X, y, taxas=[0.01, 0.05, 0.1, 0.2, 0.5]):
    """Analisa como diferentes taxas de aprendizado afetam a performance."""
    print(f"\n--- Análise de Sensibilidade - Taxa de Aprendizado ---")
    
    resultados = {}
    
    for taxa in taxas:
        print(f"\nTestando taxa de aprendizado: {taxa}")
        acuracias, epocas = validacao_cruzada_k_fold(X, y, k=3, taxa_aprendizado=taxa, epocas=200)
        
        resultados[taxa] = {
            'acuracia_media': np.mean(acuracias),
            'acuracia_std': np.std(acuracias),
            'epocas_media': np.mean(epocas),
            'epocas_std': np.std(epocas)
        }
    
    # Exibe resultados
    print(f"\n--- Resumo da Análise de Sensibilidade ---")
    print(f"{'Taxa':<8} {'Acurácia (%)':<15} {'Épocas':<15}")
    print("-" * 40)
    for taxa, res in resultados.items():
        print(f"{taxa:<8} {res['acuracia_media']:.2f}±{res['acuracia_std']:.2f}    {res['epocas_media']:.1f}±{res['epocas_std']:.1f}")
    
    return resultados

def criar_visualizacoes(perceptron, X_original, y, dados_brutos, resultados_sensibilidade):
    """Cria visualizações do modelo e análises."""
    
    # Configuração para plots em português
    plt.rcParams['figure.figsize'] = (15, 12)
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Convergência do Treinamento
    ax1.plot(perceptron.historico_erros, 'b-', linewidth=2)
    ax1.set_title('Convergência do Treinamento', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Época')
    ax1.set_ylabel('Número de Erros')
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, len(perceptron.historico_erros))
    
    # 2. Distribuição do pH vs Adequação
    ph_values = [float(linha[0]) for linha in dados_brutos]
    apto_sim = [ph for ph, apto in zip(ph_values, y) if apto == 1]
    apto_nao = [ph for ph, apto in zip(ph_values, y) if apto == 0]
    
    ax2.hist(apto_nao, bins=10, alpha=0.7, label='Não Apto', color='red', edgecolor='black')
    ax2.hist(apto_sim, bins=10, alpha=0.7, label='Apto', color='green', edgecolor='black')
    ax2.axvline(x=6.0, color='blue', linestyle='--', linewidth=2, label='pH Ideal (6.0)')
    ax2.set_title('Distribuição de pH por Adequação', fontsize=14, fontweight='bold')
    ax2.set_xlabel('pH do Solo')
    ax2.set_ylabel('Frequência')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # 3. Análise de Sensibilidade
    taxas = list(resultados_sensibilidade.keys())
    acuracias = [resultados_sensibilidade[taxa]['acuracia_media'] for taxa in taxas]
    erros_acuracia = [resultados_sensibilidade[taxa]['acuracia_std'] for taxa in taxas]
    
    ax3.errorbar(taxas, acuracias, yerr=erros_acuracia, marker='o', linewidth=2, 
                capsize=5, capthick=2, markersize=8)
    ax3.set_title('Sensibilidade à Taxa de Aprendizado', fontsize=14, fontweight='bold')
    ax3.set_xlabel('Taxa de Aprendizado')
    ax3.set_ylabel('Acurácia Média (%)')
    ax3.grid(True, alpha=0.3)
    ax3.set_ylim(0, 105)
    
    # 4. Importância dos Atributos (baseada nos pesos absolutos)
    atributos = ['Distância pH Ideal', 'Potássio', 'Boa Drenagem', 'Sem Compactação']
    pesos_abs = [abs(peso) for peso in perceptron.pesos]
    
    colors = ['#ff7f0e', '#2ca02c', '#d62728', '#1f77b4']
    bars = ax4.bar(atributos, pesos_abs, color=colors, alpha=0.8, edgecolor='black')
    ax4.set_title('Importância dos Atributos (Pesos Absolutos)', fontsize=14, fontweight='bold')
    ax4.set_ylabel('|Peso|')
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(True, alpha=0.3, axis='y')
    
    # Adiciona valores nos barras
    for bar, peso in zip(bars, pesos_abs):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{peso:.3f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    caminho_grafico = os.path.join(base_dir, 'docs', 'reports', 'analise_perceptron_mandioca.png')
    plt.savefig(caminho_grafico, dpi=300, bbox_inches='tight')
    plt.show()

def relatorio_detalhado(perceptron, X, y, dados_brutos, acuracias_cv):
    """Gera um relatório detalhado do modelo."""
    print("\n" + "="*80)
    print("           RELATÓRIO DETALHADO - MODELO PERCEPTRON MANDIOCA")
    print("="*80)
    
    # Estatísticas do Dataset
    print(f"\n📊 ESTATÍSTICAS DO DATASET:")
    print(f"   • Total de exemplos: {len(X)}")
    print(f"   • Exemplos positivos (Apto): {sum(y)} ({sum(y)/len(y)*100:.1f}%)")
    print(f"   • Exemplos negativos (Não Apto): {len(y)-sum(y)} ({(len(y)-sum(y))/len(y)*100:.1f}%)")
    
    # Análise dos atributos originais
    ph_values = [float(linha[0]) for linha in dados_brutos]
    k_values = [int(linha[1]) for linha in dados_brutos]
    
    print(f"\n🌱 ANÁLISE DOS ATRIBUTOS ORIGINAIS:")
    print(f"   • pH: {min(ph_values):.1f} - {max(ph_values):.1f} (média: {np.mean(ph_values):.2f})")
    print(f"   • Potássio: {min(k_values)} - {max(k_values)} mg/dm³ (média: {np.mean(k_values):.1f})")
    print(f"   • Boa drenagem: {sum(int(linha[2]) for linha in dados_brutos)}/{len(dados_brutos)} exemplos")
    print(f"   • Sem compactação: {sum(int(linha[3]) for linha in dados_brutos)}/{len(dados_brutos)} exemplos")
    
    # Performance do modelo
    print(f"\n🎯 PERFORMANCE DO MODELO:")
    print(f"   • Acurácia Validação Cruzada: {np.mean(acuracias_cv):.2f}% ± {np.std(acuracias_cv):.2f}%")
    print(f"   • Convergência: {len(perceptron.historico_erros)} épocas")
    
    # Interpretação dos pesos
    atributos = ['Distância pH Ideal', 'Potássio Normalizado', 'Boa Drenagem', 'Sem Compactação']
    print(f"\n⚖️  INTERPRETAÇÃO DOS PESOS:")
    for i, (attr, peso) in enumerate(zip(atributos, perceptron.pesos)):
        impacto = "POSITIVO" if peso > 0 else "NEGATIVO"
        intensidade = "ALTO" if abs(peso) > 0.3 else "MÉDIO" if abs(peso) > 0.1 else "BAIXO"
        print(f"   • {attr:<20}: {peso:+.4f} ({impacto} - {intensidade})")
    print(f"   • Bias                : {perceptron.bias:+.4f}")
    
    # Regras de decisão interpretáveis
    print(f"\n📋 REGRAS INTERPRETÁVEIS PARA PLANTIO DE MANDIOCA:")
    print(f"   1. pH deve estar próximo de 6.0 (peso: {perceptron.pesos[0]:.3f})")
    print(f"   2. Solo deve ter boa drenagem (peso: {perceptron.pesos[2]:.3f})")
    print(f"   3. Solo NÃO deve estar compactado (peso: {perceptron.pesos[3]:.3f})")
    print(f"   4. Potássio contribui moderadamente (peso: {perceptron.pesos[1]:.3f})")
    
    print("\n" + "="*80)

# -----------------------------------------------------------------------------
# SCRIPT PRINCIPAL APRIMORADO
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("🌾 ANÁLISE COMPLETA - ADEQUAÇÃO DO SOLO PARA MANDIOCA 🌾")
    print("="*60)
    
    # Carregamento e pré-processamento
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    arquivo_csv = os.path.join(base_dir, 'data', 'entrada_mandioca.csv')
    
    dados_brutos = carregar_dados_brutos(arquivo_csv)
    X_processado, y_processado, min_vals, max_vals = pre_processar_dados(dados_brutos)
    
    print(f"✅ Dados carregados: {len(X_processado)} exemplos")
    
    # Treinamento do modelo principal
    print(f"\n🚀 TREINAMENTO DO MODELO PRINCIPAL")
    perceptron = PerceptronAprimorado(len(X_processado[0]), taxa_aprendizado=0.1)
    X_treino, y_treino = X_processado[:30], y_processado[:30]
    X_teste, y_teste = X_processado[30:], y_processado[30:]
    
    perceptron.treinar(X_treino, y_treino, epocas=200)
    
    # Teste inicial
    acertos = sum(1 for i in range(len(X_teste)) 
                  if perceptron.prever(X_teste[i]) == y_teste[i])
    acuracia_inicial = (acertos / len(X_teste)) * 100
    print(f"✅ Acurácia no conjunto de teste: {acuracia_inicial:.2f}%")
    
    # Validação cruzada
    acuracias_cv, epocas_cv = validacao_cruzada_k_fold(X_processado, y_processado, k=5)
    
    # Análise de sensibilidade
    resultados_sensibilidade = analise_sensibilidade_taxa_aprendizado(X_processado, y_processado)
    
    # Visualizações
    print(f"\n📊 Gerando visualizações...")
    criar_visualizacoes(perceptron, X_processado, y_processado, dados_brutos, resultados_sensibilidade)
    
    # Relatório final
    relatorio_detalhado(perceptron, X_processado, y_processado, dados_brutos, acuracias_cv)
    
    print(f"\n🎉 Análise completa finalizada!")
    print(f"📈 Gráficos salvos em: analise_perceptron_mandioca.png")
