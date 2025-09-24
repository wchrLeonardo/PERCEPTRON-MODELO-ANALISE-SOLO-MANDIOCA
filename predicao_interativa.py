import random
from treinamento_aprimorado import PerceptronAprimorado, pre_processar_dados, carregar_dados_brutos

def predizer_solo_interativo():
    """Permite ao usuário testar o modelo com novos dados de solo."""
    
    # Carrega e treina o modelo
    print("🌾 SISTEMA DE PREDIÇÃO - ADEQUAÇÃO DO SOLO PARA MANDIOCA")
    print("=" * 60)
    print("Carregando modelo...")
    
    dados_brutos = carregar_dados_brutos('entrada_mandioca.csv')
    X_processado, y_processado, min_vals, max_vals = pre_processar_dados(dados_brutos)
    
    # Treina o modelo com todos os dados disponíveis
    perceptron = PerceptronAprimorado(len(X_processado[0]), taxa_aprendizado=0.5)
    perceptron.treinar(X_processado, y_processado, epocas=100, verbose=False)
    
    print("✅ Modelo carregado e treinado!")
    print("\nInsira os dados do seu solo:")
    
    while True:
        try:
            # Coleta dados do usuário
            print("\n" + "-" * 50)
            ph = float(input("pH do solo (ex: 6.0): "))
            potassio = int(input("Potássio mg/dm³ (ex: 120): "))
            drenagem = int(input("Boa drenagem? (1=Sim, 0=Não): "))
            compactacao = int(input("Solo sem compactação? (1=Sim, 0=Não): "))
            
            # Validação básica
            if not (3.0 <= ph <= 9.0):
                print("⚠️  pH deve estar entre 3.0 e 9.0")
                continue
            if not (0 <= potassio <= 500):
                print("⚠️  Potássio deve estar entre 0 e 500 mg/dm³")
                continue
            if drenagem not in [0, 1] or compactacao not in [0, 1]:
                print("⚠️  Drenagem e Compactação devem ser 0 ou 1")
                continue
            
            # Pré-processamento dos dados do usuário
            distancia_ph = abs(ph - 6.0)
            
            # Normalização usando os mesmos min/max do treinamento
            ph_norm = (distancia_ph - min_vals[0]) / (max_vals[0] - min_vals[0]) if max_vals[0] != min_vals[0] else 0
            k_norm = (potassio - min_vals[1]) / (max_vals[1] - min_vals[1]) if max_vals[1] != min_vals[1] else 0
            
            entrada_processada = [ph_norm, k_norm, drenagem, compactacao]
            
            # Predição
            resultado = perceptron.prever(entrada_processada)
            
            # Cálculo da confiança (baseado na distância da fronteira de decisão)
            soma_ponderada = perceptron.bias
            for i, peso in enumerate(perceptron.pesos):
                soma_ponderada += peso * entrada_processada[i]
            
            confianca = abs(soma_ponderada)  # Quanto maior, mais confiante
            
            # Resultado
            print("\n" + "=" * 50)
            if resultado == 1:
                print("✅ RESULTADO: SOLO APTO PARA MANDIOCA!")
                print(f"🎯 Confiança: {min(confianca * 100, 100):.1f}%")
            else:
                print("❌ RESULTADO: SOLO NÃO APTO PARA MANDIOCA")
                print(f"🎯 Confiança: {min(confianca * 100, 100):.1f}%")
            
            # Análise detalhada
            print("\n📊 ANÁLISE DETALHADA:")
            
            # pH
            if abs(ph - 6.0) < 0.5:
                print(f"✅ pH {ph:.1f}: EXCELENTE (próximo ao ideal 6.0)")
            elif abs(ph - 6.0) < 1.0:
                print(f"⚠️  pH {ph:.1f}: BOM (razoavelmente próximo ao ideal)")
            else:
                print(f"❌ pH {ph:.1f}: PROBLEMÁTICO (muito distante do ideal 6.0)")
            
            # Potássio
            if potassio >= 120:
                print(f"✅ Potássio {potassio} mg/dm³: ADEQUADO")
            elif potassio >= 80:
                print(f"⚠️  Potássio {potassio} mg/dm³: MODERADO")
            else:
                print(f"❌ Potássio {potassio} mg/dm³: BAIXO")
            
            # Drenagem
            print(f"{'✅' if drenagem == 1 else '❌'} Drenagem: {'BOA' if drenagem == 1 else 'RUIM'}")
            
            # Compactação
            print(f"{'✅' if compactacao == 1 else '❌'} Compactação: {'AUSENTE' if compactacao == 1 else 'PRESENTE'}")
            
            # Recomendações
            print("\n💡 RECOMENDAÇÕES:")
            if resultado == 0:
                recomendacoes = []
                if abs(ph - 6.0) > 0.5:
                    if ph < 6.0:
                        recomendacoes.append("• Aplicar calcário para corrigir acidez")
                    else:
                        recomendacoes.append("• Aplicar enxofre ou matéria orgânica para baixar pH")
                
                if drenagem == 0:
                    recomendacoes.append("• Implementar sistema de drenagem")
                    recomendacoes.append("• Construir canteiros elevados")
                
                if compactacao == 0:
                    recomendacoes.append("• Fazer subsolagem para descompactar")
                    recomendacoes.append("• Evitar tráfego pesado no solo úmido")
                
                if potassio < 100:
                    recomendacoes.append("• Aplicar fertilizante potássico (cloreto ou sulfato de potássio)")
                
                for rec in recomendacoes:
                    print(rec)
            else:
                print("• Solo está adequado! Proceda com o plantio.")
                print("• Mantenha as boas práticas de manejo.")
            
            # Pergunta se quer continuar
            print("\n" + "=" * 50)
            continuar = input("Testar outro solo? (s/n): ").lower()
            if continuar not in ['s', 'sim', 'y', 'yes']:
                break
                
        except ValueError:
            print("❌ Erro: Digite apenas números nos valores solicitados!")
        except KeyboardInterrupt:
            print("\n\n👋 Sistema encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    print("\n🎉 Obrigado por usar o Sistema de Predição de Solo para Mandioca!")
    print("📊 Para análises mais detalhadas, consulte: RELATORIO_COMPLETO.md")

if __name__ == "__main__":
    predizer_solo_interativo()
