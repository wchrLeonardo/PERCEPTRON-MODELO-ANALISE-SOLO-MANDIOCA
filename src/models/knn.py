import math
import operator


# FUNÇÕES DE PRÉ-PROCESSAMENTO (Reutilizadas/Adaptadas)
def carregar_dados_brutos(caminho_arquivo):
    """Lê um arquivo CSV e o converte para o formato bruto (strings)."""
    dataset = []
    with open(caminho_arquivo, 'r') as file:
        next(file) # Pula cabeçalho
        for linha in file:
            dataset.append(linha.strip().split(','))
    return dataset

def pre_processar_dados(dataset):
    """
    Converte e normaliza o dataset.
    Mantém a mesma lógica do Perceptron para comparabilidade.
    """
    dados_numericos = []
    for linha in dataset:
        # pH (float), Potassio (int), Drenagem (int), Compactacao (int), Apto (int)
        dados_numericos.append([float(linha[0]), int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4])])
    
    # Separa características (X) dos rótulos (y)
    X_bruto = [linha[:-1] for linha in dados_numericos]
    y = [linha[-1] for linha in dados_numericos]
    
    # Engenharia de Atributos: Substituir pH pela distância ao ideal (6.0)
    for i in range(len(X_bruto)):
        ph_valor = X_bruto[i][0]
        distancia_ph = abs(ph_valor - 6.0)
        X_bruto[i][0] = distancia_ph 
    
    # Normalização Min-Max
    min_vals = [float('inf')] * 2
    max_vals = [float('-inf')] * 2
    
    for linha in X_bruto:
        for i in range(2): 
            if linha[i] < min_vals[i]: min_vals[i] = linha[i]
            if linha[i] > max_vals[i]: max_vals[i] = linha[i]
            
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
        
    return X_normalizado, y


# IMPLEMENTAÇÃO DO KNN
def distancia_euclidiana(instancia1, instancia2):
    distancia = 0
    for i in range(len(instancia1)):
        distancia += pow((instancia1[i] - instancia2[i]), 2)
    return math.sqrt(distancia)

def get_vizinhos(X_treino, y_treino, instancia_teste, k):
    distancias = []
    for i in range(len(X_treino)):
        dist = distancia_euclidiana(instancia_teste, X_treino[i])
        distancias.append((y_treino[i], dist))
    
    # Ordena pelas distâncias (menor para maior)
    distancias.sort(key=operator.itemgetter(1))
    
    vizinhos = []
    for i in range(k):
        vizinhos.append(distancias[i][0])
    return vizinhos

def prever_classificacao(vizinhos):
    votos = {}
    for x in vizinhos:
        if x in votos:
            votos[x] += 1
        else:
            votos[x] = 1
    
    # Retorna a classe com mais votos
    votos_ordenados = sorted(votos.items(), key=operator.itemgetter(1), reverse=True)
    return votos_ordenados[0][0]

def avaliar_modelo(X_treino, y_treino, X_teste, y_teste, k):
    acertos = 0
    for i in range(len(X_teste)):
        vizinhos = get_vizinhos(X_treino, y_treino, X_teste[i], k)
        resultado = prever_classificacao(vizinhos)
        if resultado == y_teste[i]:
            acertos += 1
    
    acuracia = (acertos / len(X_teste)) * 100
    return acuracia, acertos


# SCRIPT PRINCIPAL
if __name__ == "__main__":
    import os
    # Caminho relativo para o arquivo CSV
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    arquivo_csv = os.path.join(base_dir, 'data', 'entrada_mandioca.csv')
    dados_brutos = carregar_dados_brutos(arquivo_csv)
    X_processado, y_processado = pre_processar_dados(dados_brutos)

    # Divisão Treino/Teste (mesma do Perceptron para comparação justa)
    X_treino, y_treino = X_processado[:30], y_processado[:30]
    X_teste, y_teste = X_processado[30:], y_processado[30:]

    print(f"Dataset carregado: {len(X_treino)} treino, {len(X_teste)} teste")
    print("-" * 50)

    valores_k = [3, 5, 7]
    resultados = {}

    for k in valores_k:
        acuracia, acertos = avaliar_modelo(X_treino, y_treino, X_teste, y_teste, k)
        resultados[k] = acuracia
        print(f"K = {k}: Acurácia = {acuracia:.2f}% ({acertos}/{len(X_teste)} acertos)")
    
    print("-" * 50)
    melhor_k = max(resultados.items(), key=operator.itemgetter(1))
    print(f"Melhor K: {melhor_k[0]} com {melhor_k[1]:.2f}% de acurácia")
