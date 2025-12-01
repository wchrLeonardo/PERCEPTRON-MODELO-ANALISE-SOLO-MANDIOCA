import random
import math

# -----------------------------------------------------------------------------
# CLASSE PERCEPTRON (sem alterações na lógica principal)
# -----------------------------------------------------------------------------
class Perceptron:
    def __init__(self, num_entradas, taxa_aprendizado=0.1):
        self.taxa_aprendizado = taxa_aprendizado
        self.pesos = [random.uniform(-0.5, 0.5) for _ in range(num_entradas)]
        self.bias = random.uniform(-0.5, 0.5)

    def _funcao_ativacao_degrau(self, soma_ponderada):
        return 1 if soma_ponderada >= 0 else 0

    def prever(self, entradas):
        soma_ponderada = self.bias
        for i in range(len(self.pesos)):
            soma_ponderada += self.pesos[i] * entradas[i]
        return self._funcao_ativacao_degrau(soma_ponderada)

    def treinar(self, dados_treino, rotulos_treino, epocas=100):
        print(f"--- Iniciando Treinamento com {epocas} épocas ---")
        for epoca in range(epocas):
            erros_epoca = 0
            for entradas, rotulo_esperado in zip(dados_treino, rotulos_treino):
                previsao = self.prever(entradas)
                erro = rotulo_esperado - previsao
                if erro != 0:
                    erros_epoca += 1
                    self.bias += self.taxa_aprendizado * erro
                    for i in range(len(self.pesos)):
                        self.pesos[i] += self.taxa_aprendizado * erro * entradas[i]
            
            if (epoca + 1) % 10 == 0: # Imprime o progresso a cada 10 épocas
                 print(f"> Época {epoca + 1}/{epocas} - Erros: {erros_epoca}")

            if erros_epoca == 0:
                print(f"\n--- Treinamento concluído na época {epoca + 1}: modelo convergiu! ---")
                return
        print("\n--- Treinamento finalizado (limite de épocas atingido). ---")

# -----------------------------------------------------------------------------
# FUNÇÕES DE PRÉ-PROCESSAMENTO DOS DADOS
# -----------------------------------------------------------------------------
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
    Converte, aplica engenharia de atributos e normaliza o dataset.
    Esta é a etapa "inteligente" que transforma os dados brutos em algo
    que o Perceptron pode aprender eficientemente.
    """
    dados_processados = []
    
    # 1. Converter strings para números
    dados_numericos = []
    for linha in dataset:
        # pH (float), Potassio (int), Drenagem (int), Compactacao (int), Apto (int)
        dados_numericos.append([float(linha[0]), int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4])])
    
    # Separa características (X) dos rótulos (y)
    X_bruto = [linha[:-1] for linha in dados_numericos]
    y = [linha[-1] for linha in dados_numericos]
    
    # 2. Engenharia de Atributos: Substituir pH pela distância ao ideal (6.0)
    for i in range(len(X_bruto)):
        ph_valor = X_bruto[i][0]
        distancia_ph = abs(ph_valor - 6.0)
        X_bruto[i][0] = distancia_ph # Substitui o pH original
    
    # 3. Normalização Min-Max para os atributos contínuos
    # Precisamos encontrar o min/max de cada coluna (atributo)
    # Apenas para a distância do pH e Potássio
    min_vals = [float('inf')] * 2
    max_vals = [float('-inf')] * 2
    
    for linha in X_bruto:
        for i in range(2): # Itera sobre os 2 primeiros atributos
            if linha[i] < min_vals[i]: min_vals[i] = linha[i]
            if linha[i] > max_vals[i]: max_vals[i] = linha[i]
            
    # Aplica a normalização
    X_normalizado = []
    for linha in X_bruto:
        linha_norm = []
        # Normaliza 'distancia_ph' e 'Potassio'
        for i in range(2):
            # Evita divisão por zero se todos os valores forem iguais
            if (max_vals[i] - min_vals[i]) == 0:
                norm_val = 0
            else:
                norm_val = (linha[i] - min_vals[i]) / (max_vals[i] - min_vals[i])
            linha_norm.append(norm_val)
        
        # Adiciona os atributos binários que não precisam de normalização
        linha_norm.extend(linha[2:])
        X_normalizado.append(linha_norm)
        
    print("Dados pré-processados e normalizados com sucesso.")
    return X_normalizado, y

# -----------------------------------------------------------------------------
# SCRIPT PRINCIPAL
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import os
    # Caminho relativo para o arquivo CSV
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    arquivo_csv = os.path.join(base_dir, 'data', 'entrada_mandioca.csv')
    dados_brutos = carregar_dados_brutos(arquivo_csv)

    # Pré-processamento dos dados
    X_processado, y_processado = pre_processar_dados(dados_brutos)

    # Divisão entre treino (30 exemplos) e teste (restante)
    X_treino, y_treino = X_processado[:30], y_processado[:30]
    X_teste, y_teste = X_processado[30:], y_processado[30:]

    print(f"Base de dados carregada: {len(X_treino)} exemplos de treino e {len(X_teste)} de teste.")
    
    # Instanciação e Treinamento
    num_features = len(X_treino[0])
    perceptron = Perceptron(num_entradas=num_features, taxa_aprendizado=0.1)
    perceptron.treinar(X_treino, y_treino, epocas=200) # Aumentamos as épocas para garantir convergência
    
    # Teste do Modelo
    print("\n--- Iniciando Teste do Modelo ---")
    acertos = 0
    for i in range(len(X_teste)):
        entradas_teste = X_teste[i]
        rotulo_real = y_teste[i]
        
        previsao = perceptron.prever(entradas_teste)
        if previsao == rotulo_real:
            acertos += 1
        
        # Mostra os dados originais para melhor interpretação
        dados_originais = dados_brutos[30+i][:-1]
        status = "CORRETO" if previsao == rotulo_real else "INCORRETO"
        print(f"Dados Originais: {dados_originais} -> Previsto: {previsao} | Real: {rotulo_real} ({status})")

    # Cálculo da acurácia
    acuracia = (acertos / len(X_teste)) * 100
    print("\n--- Resultados Finais ---")
    print(f"Pesos Finais: {[round(p, 4) for p in perceptron.pesos]}")
    print(f"Bias Final: {round(perceptron.bias, 4)}")
    print(f"Total de testes: {len(X_teste)}")
    print(f"Acertos: {acertos}")
    print(f"Acurácia: {acuracia:.2f}%")