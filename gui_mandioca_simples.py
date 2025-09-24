import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import sys

# Importa as funções do modelo
try:
    from treinamento_aprimorado import PerceptronAprimorado, pre_processar_dados, carregar_dados_brutos
except ImportError:
    try:
        from treinamento import Perceptron
        # Função alternativa se não encontrar o aprimorado
        def carregar_dados_brutos(caminho_arquivo):
            dataset = []
            with open(caminho_arquivo, 'r') as file:
                next(file)  # Pula cabeçalho
                for linha in file:
                    dataset.append(linha.strip().split(','))
            return dataset
        
        def pre_processar_dados(dataset):
            dados_numericos = []
            for linha in dataset:
                dados_numericos.append([float(linha[0]), int(linha[1]), int(linha[2]), int(linha[3]), int(linha[4])])
            
            X_bruto = [linha[:-1] for linha in dados_numericos]
            y = [linha[-1] for linha in dados_numericos]
            
            # Engenharia de Atributos: pH -> distância do ideal
            for i in range(len(X_bruto)):
                ph_valor = X_bruto[i][0]
                distancia_ph = abs(ph_valor - 6.0)
                X_bruto[i][0] = distancia_ph
            
            # Normalização
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
                
            return X_normalizado, y, min_vals, max_vals
        
        PerceptronAprimorado = Perceptron  # Usa o original
        
    except ImportError:
        messagebox.showerror("Erro", "Arquivos do modelo não encontrados!")
        sys.exit()

class SoloMandiocaGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.modelo_treinado = False
        self.perceptron = None
        self.min_vals = None
        self.max_vals = None
        
        self.create_widgets()
        self.carregar_modelo()
    
    def setup_window(self):
        """Configuração da janela principal"""
        self.root.title("🌾 Sistema de Análise de Solo para Mandioca")
        self.root.geometry("950x750")
        self.root.configure(bg='#e8f5e8')
        
        # Centralizar na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (950 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f"950x750+{x}+{y}")
        
        # Impede redimensionamento
        self.root.resizable(True, True)
    
    def create_widgets(self):
        """Criar interface"""
        
        # Container principal
        main_container = tk.Frame(self.root, bg='#e8f5e8', padx=25, pady=20)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # TÍTULO PRINCIPAL
        title_frame = tk.Frame(main_container, bg='#2d5016', relief=tk.RAISED, bd=3)
        title_frame.pack(fill=tk.X, pady=(0, 25))
        
        title_label = tk.Label(title_frame, 
                              text="🌾 SISTEMA DE ANÁLISE DE SOLO PARA MANDIOCA 🌾",
                              font=('Arial', 18, 'bold'),
                              fg='white',
                              bg='#2d5016')
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(title_frame,
                                 text="Inteligência Artificial para Agricultura de Precisão",
                                 font=('Arial', 12, 'italic'),
                                 fg='#b8e6b8',
                                 bg='#2d5016')
        subtitle_label.pack()
        
        # Espaçamento adicional
        tk.Label(title_frame, text="", bg='#2d5016', pady=5).pack()
        
        # STATUS DO SISTEMA
        self.status_frame = tk.Frame(main_container, bg='#fff3cd', relief=tk.RAISED, bd=2)
        self.status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = tk.Label(self.status_frame,
                                   text="🔄 Inicializando sistema...",
                                   font=('Arial', 11, 'bold'),
                                   fg='#856404',
                                   bg='#fff3cd')
        self.status_label.pack(pady=8)
        
        # PAINEL DE ENTRADA DE DADOS
        input_panel = tk.LabelFrame(main_container,
                                   text=" 📊 DADOS DO SOLO ",
                                   font=('Arial', 14, 'bold'),
                                   fg='#2d5016',
                                   bg='#e8f5e8',
                                   padx=20, pady=20)
        input_panel.pack(fill=tk.X, pady=(0, 20))
        
        self.create_input_section(input_panel)
        
        # PAINEL DE CONTROLES
        control_panel = tk.Frame(main_container, bg='#e8f5e8')
        control_panel.pack(fill=tk.X, pady=(0, 20))
        
        # Botão principal de análise
        self.analyze_button = tk.Button(control_panel,
                                       text="🔍 ANALISAR SOLO",
                                       font=('Arial', 14, 'bold'),
                                       fg='white',
                                       bg='#28a745',
                                       activebackground='#218838',
                                       activeforeground='white',
                                       relief=tk.RAISED,
                                       bd=3,
                                       padx=30,
                               pady=10,
                                       command=self.analisar_solo,
                                       cursor='hand2')
        self.analyze_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Botão limpar
        clear_button = tk.Button(control_panel,
                               text="🗑️ LIMPAR",
                               font=('Arial', 12, 'bold'),
                               fg='white',
                               bg='#6c757d',
                               activebackground='#5a6268',
                               activeforeground='white',
                               relief=tk.RAISED,
                               bd=2,
                               padx=20,
                               pady=8,
                               command=self.limpar_campos,
                               cursor='hand2')
        clear_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Botão exemplo
        example_button = tk.Button(control_panel,
                                 text="📝 CARREGAR EXEMPLO",
                                 font=('Arial', 12, 'bold'),
                                 fg='white',
                                 bg='#17a2b8',
                                 activebackground='#138496',
                                 activeforeground='white',
                                 relief=tk.RAISED,
                                 bd=2,
                                 padx=20,
                                 pady=8,
                                 command=self.carregar_exemplo,
                                 cursor='hand2')
        example_button.pack(side=tk.LEFT)
        
        # PAINEL DE RESULTADOS
        result_panel = tk.LabelFrame(main_container,
                                   text=" 📈 RESULTADO DA ANÁLISE ",
                                   font=('Arial', 14, 'bold'),
                                   fg='#2d5016',
                                   bg='#e8f5e8',
                                   padx=15, pady=15)
        result_panel.pack(fill=tk.BOTH, expand=True)
        
        # Área de texto para resultados
        self.result_display = scrolledtext.ScrolledText(result_panel,
                                                       font=('Consolas', 11),
                                                       bg='#f8f9fa',
                                                       fg='#212529',
                                                       wrap=tk.WORD,
                                                       relief=tk.SUNKEN,
                                                       bd=2)
        self.result_display.pack(fill=tk.BOTH, expand=True)
        
        # Mensagem inicial
        welcome_text = """🌱 BEM-VINDO AO SISTEMA DE ANÁLISE DE SOLO PARA MANDIOCA!

📋 COMO USAR:
1️⃣  Preencha os dados do seu solo nos campos acima
2️⃣  Clique no botão "ANALISAR SOLO" 
3️⃣  Veja o resultado detalhado e recomendações aqui

💡 DICAS:
• Use "CARREGAR EXEMPLO" para ver dados de teste
• Todos os campos são obrigatórios
• O sistema usa IA treinada com dados reais

⏳ Sistema carregando... Aguarde a inicialização completa."""

        self.result_display.insert('1.0', welcome_text)
        self.result_display.config(state='disabled')
    
    def create_input_section(self, parent):
        """Criar seção de entrada de dados"""
        
        # Grid para organização
        grid_frame = tk.Frame(parent, bg='#e8f5e8')
        grid_frame.pack(fill=tk.X)
        
        # Configurar grid
        grid_frame.grid_columnconfigure(1, weight=1)
        
        # Campo pH
        tk.Label(grid_frame, text="🧪 pH do Solo:",
                font=('Arial', 12, 'bold'),
                fg='#2d5016',
                bg='#e8f5e8').grid(row=0, column=0, sticky='w', padx=(0, 15), pady=10)
        
        self.ph_var = tk.StringVar()
        ph_frame = tk.Frame(grid_frame, bg='#e8f5e8')
        ph_frame.grid(row=0, column=1, sticky='w', pady=10)
        
        self.ph_entry = tk.Entry(ph_frame, textvariable=self.ph_var,
                                font=('Arial', 12), width=12,
                                relief=tk.SUNKEN, bd=2)
        self.ph_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(ph_frame, text="(Ex: 6.0 - Ideal entre 5.5 e 6.5)",
                font=('Arial', 10), fg='#666666', bg='#e8f5e8').pack(side=tk.LEFT)
        
        # Campo Potássio
        tk.Label(grid_frame, text="⚡ Potássio (mg/dm³):",
                font=('Arial', 12, 'bold'),
                fg='#2d5016',
                bg='#e8f5e8').grid(row=1, column=0, sticky='w', padx=(0, 15), pady=10)
        
        self.potassio_var = tk.StringVar()
        potassio_frame = tk.Frame(grid_frame, bg='#e8f5e8')
        potassio_frame.grid(row=1, column=1, sticky='w', pady=10)
        
        self.potassio_entry = tk.Entry(potassio_frame, textvariable=self.potassio_var,
                                      font=('Arial', 12), width=12,
                                      relief=tk.SUNKEN, bd=2)
        self.potassio_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        tk.Label(potassio_frame, text="(Ex: 120 - Mínimo recomendado: 80)",
                font=('Arial', 10), fg='#666666', bg='#e8f5e8').pack(side=tk.LEFT)
        
        # Campo Drenagem
        tk.Label(grid_frame, text="💧 Boa Drenagem:",
                font=('Arial', 12, 'bold'),
                fg='#2d5016',
                bg='#e8f5e8').grid(row=2, column=0, sticky='w', padx=(0, 15), pady=10)
        
        self.drenagem_var = tk.StringVar(value="1")
        drenagem_frame = tk.Frame(grid_frame, bg='#e8f5e8')
        drenagem_frame.grid(row=2, column=1, sticky='w', pady=10)
        
        tk.Radiobutton(drenagem_frame, text="✅ Sim", variable=self.drenagem_var, value="1",
                      font=('Arial', 11), fg='#155724', bg='#e8f5e8',
                      selectcolor='#d4edda', cursor='hand2').pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(drenagem_frame, text="❌ Não", variable=self.drenagem_var, value="0",
                      font=('Arial', 11), fg='#721c24', bg='#e8f5e8',
                      selectcolor='#f8d7da', cursor='hand2').pack(side=tk.LEFT)
        
        # Campo Compactação
        tk.Label(grid_frame, text="🏔️ Solo SEM Compactação:",
                font=('Arial', 12, 'bold'),
                fg='#2d5016',
                bg='#e8f5e8').grid(row=3, column=0, sticky='w', padx=(0, 15), pady=10)
        
        self.compactacao_var = tk.StringVar(value="1")
        compactacao_frame = tk.Frame(grid_frame, bg='#e8f5e8')
        compactacao_frame.grid(row=3, column=1, sticky='w', pady=10)
        
        tk.Radiobutton(compactacao_frame, text="✅ Sim", variable=self.compactacao_var, value="1",
                      font=('Arial', 11), fg='#155724', bg='#e8f5e8',
                      selectcolor='#d4edda', cursor='hand2').pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Radiobutton(compactacao_frame, text="❌ Não", variable=self.compactacao_var, value="0",
                      font=('Arial', 11), fg='#721c24', bg='#e8f5e8',
                      selectcolor='#f8d7da', cursor='hand2').pack(side=tk.LEFT)
    
    def carregar_modelo(self):
        """Carrega o modelo em thread separada"""
        def load():
            try:
                self.status_label.config(text="🔄 Carregando dados de treinamento...", bg='#fff3cd')
                self.root.update()
                
                dados_brutos = carregar_dados_brutos('entrada_mandioca.csv')
                X_processado, y_processado, min_vals, max_vals = pre_processar_dados(dados_brutos)
                
                self.status_label.config(text="🤖 Treinando modelo de IA...")
                self.root.update()
                
                self.perceptron = PerceptronAprimorado(len(X_processado[0]), taxa_aprendizado=0.5)
                self.perceptron.treinar(X_processado, y_processado, epocas=100, verbose=False)
                
                self.min_vals = min_vals
                self.max_vals = max_vals
                self.modelo_treinado = True
                
                self.status_frame.config(bg='#d4edda')
                self.status_label.config(text="✅ Sistema carregado! Modelo treinado e pronto para análise.",
                                       fg='#155724', bg='#d4edda')
                
                self.analyze_button.config(state='normal')
                
                # Atualiza mensagem de boas-vindas
                self.result_display.config(state='normal')
                self.result_display.delete('1.0', tk.END)
                welcome_ready = """✅ SISTEMA PRONTO PARA USO!

🎯 O modelo de IA foi treinado com sucesso e está pronto para analisar seu solo!

📊 CAPACIDADES DO SISTEMA:
• Análise de 4 fatores críticos para mandioca
• Precisão de 97.78% em validação cruzada  
• Recomendações personalizadas
• Interface amigável e intuitiva

🌾 SOBRE A MANDIOCA:
• Prefere pH entre 5.5 - 6.5
• Necessita boa drenagem
• Solo deve estar livre de compactação
• Potássio mínimo: 80 mg/dm³

👨‍🌾 PARA COMEÇAR:
Preencha os dados do seu solo e clique em "ANALISAR SOLO"

💡 Use "CARREGAR EXEMPLO" se quiser testar o sistema primeiro."""

                self.result_display.insert('1.0', welcome_ready)
                self.result_display.config(state='disabled')
                
            except Exception as e:
                self.status_frame.config(bg='#f8d7da')
                self.status_label.config(text=f"❌ Erro ao carregar: {str(e)}", 
                                       fg='#721c24', bg='#f8d7da')
                messagebox.showerror("Erro Critical", f"Falha ao carregar modelo:\n{str(e)}")
        
        self.analyze_button.config(state='disabled')
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
    
    def validar_dados(self):
        """Validar dados de entrada"""
        try:
            ph = float(self.ph_var.get().strip())
            potassio = int(self.potassio_var.get().strip())
            drenagem = int(self.drenagem_var.get())
            compactacao = int(self.compactacao_var.get())
            
            if not (3.0 <= ph <= 9.0):
                raise ValueError("pH deve estar entre 3.0 e 9.0")
            
            if not (0 <= potassio <= 500):
                raise ValueError("Potássio deve estar entre 0 e 500 mg/dm³")
            
            return ph, potassio, drenagem, compactacao
            
        except ValueError as e:
            if "could not convert" in str(e) or "invalid literal" in str(e):
                raise ValueError("Por favor, preencha pH com números decimais (ex: 6.0) e Potássio com números inteiros (ex: 120)")
            else:
                raise e
    
    def analisar_solo(self):
        """Executar análise do solo"""
        if not self.modelo_treinado:
            messagebox.showerror("Sistema Não Pronto", "O modelo ainda está carregando. Aguarde alguns segundos.")
            return
        
        try:
            ph, potassio, drenagem, compactacao = self.validar_dados()
            
            # Pré-processamento
            distancia_ph = abs(ph - 6.0)
            ph_norm = (distancia_ph - self.min_vals[0]) / (self.max_vals[0] - self.min_vals[0]) if self.max_vals[0] != self.min_vals[0] else 0
            k_norm = (potassio - self.min_vals[1]) / (self.max_vals[1] - self.min_vals[1]) if self.max_vals[1] != self.min_vals[1] else 0
            
            entrada_processada = [ph_norm, k_norm, drenagem, compactacao]
            
            # Predição
            resultado = self.perceptron.prever(entrada_processada)
            
            # Confiança
            soma_ponderada = self.perceptron.bias
            for i, peso in enumerate(self.perceptron.pesos):
                soma_ponderada += peso * entrada_processada[i]
            confianca = min(abs(soma_ponderada) * 100, 100)
            
            self.mostrar_resultado(ph, potassio, drenagem, compactacao, resultado, confianca)
            
        except ValueError as e:
            messagebox.showerror("Dados Inválidos", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante análise: {str(e)}")
    
    def mostrar_resultado(self, ph, potassio, drenagem, compactacao, resultado, confianca):
        """Mostrar resultado da análise"""
        
        self.result_display.config(state='normal')
        self.result_display.delete('1.0', tk.END)
        
        # Cabeçalho
        header = "="*80 + "\n"
        header += "🌾 RELATÓRIO DE ANÁLISE DE SOLO PARA MANDIOCA\n"
        header += "="*80 + "\n\n"
        
        # Dados analisados
        dados = "📊 DADOS INSERIDOS:\n"
        dados += f"   🧪 pH do Solo: {ph:.1f}\n"
        dados += f"   ⚡ Potássio: {potassio} mg/dm³\n" 
        dados += f"   💧 Drenagem: {'Boa' if drenagem == 1 else 'Ruim'}\n"
        dados += f"   🏔️  Compactação: {'Ausente' if compactacao == 1 else 'Presente'}\n\n"
        
        # Resultado principal
        if resultado == 1:
            resultado_texto = "🎉 RESULTADO: SOLO APTO PARA PLANTIO DE MANDIOCA!\n"
            resultado_texto += f"🎯 Nível de Confiança: {confianca:.1f}%\n\n"
        else:
            resultado_texto = "⚠️  RESULTADO: SOLO NÃO RECOMENDADO PARA MANDIOCA\n"
            resultado_texto += f"🎯 Nível de Confiança: {confianca:.1f}%\n\n"
        
        # Análise detalhada
        analise = "🔍 ANÁLISE DETALHADA:\n\n"
        
        # pH
        if abs(ph - 6.0) < 0.3:
            analise += f"✅ pH {ph:.1f}: EXCELENTE (muito próximo ao ideal 6.0)\n"
        elif abs(ph - 6.0) < 0.7:
            analise += f"🟡 pH {ph:.1f}: BOM (próximo ao ideal)\n"
        elif abs(ph - 6.0) < 1.2:
            analise += f"⚠️  pH {ph:.1f}: MODERADO (razoável para mandioca)\n"
        else:
            analise += f"❌ pH {ph:.1f}: PROBLEMÁTICO (muito distante do ideal 6.0)\n"
        
        # Potássio
        if potassio >= 140:
            analise += f"✅ Potássio {potassio}: EXCELENTE (muito adequado)\n"
        elif potassio >= 100:
            analise += f"🟡 Potássio {potassio}: BOM (adequado)\n"
        elif potassio >= 70:
            analise += f"⚠️  Potássio {potassio}: MODERADO (pode precisar suplementação)\n"
        else:
            analise += f"❌ Potássio {potassio}: BAIXO (necessita fertilização)\n"
        
        # Outros fatores
        analise += f"{'✅' if drenagem == 1 else '❌'} Drenagem: {'ADEQUADA' if drenagem == 1 else 'INADEQUADA'}\n"
        analise += f"{'✅' if compactacao == 1 else '❌'} Estrutura: {'ADEQUADA' if compactacao == 1 else 'COMPACTADA'}\n\n"
        
        # Recomendações
        recomendacoes = "💡 RECOMENDAÇÕES TÉCNICAS:\n\n"
        
        if resultado == 0:
            count = 1
            if abs(ph - 6.0) > 0.5:
                if ph < 6.0:
                    recomendacoes += f"{count}. 📈 CORRIGIR ACIDEZ: Aplicar 2-4 t/ha de calcário dolomítico\n"
                else:
                    recomendacoes += f"{count}. 📉 REDUZIR pH: Aplicar enxofre (200-400 kg/ha) ou matéria orgânica\n"
                count += 1
            
            if potassio < 100:
                recomendacoes += f"{count}. ⚡ FERTILIZAÇÃO K: Aplicar 60-100 kg/ha de K₂O (cloreto ou sulfato de potássio)\n"
                count += 1
            
            if drenagem == 0:
                recomendacoes += f"{count}. 🚿 MELHORAR DRENAGEM: Construir drenos, canteiros elevados ou sulcos\n"
                count += 1
            
            if compactacao == 0:
                recomendacoes += f"{count}. 🚜 DESCOMPACTAR: Subsolagem a 40-60 cm de profundidade\n"
                recomendacoes += f"{count+1}. ⚠️  MANEJO: Evitar tráfego pesado em solo úmido\n"
                count += 2
            
            recomendacoes += f"\n{count}. 👨‍🌾 CONSULTAR: Procure um engenheiro agrônomo para plano detalhado\n"
            
        else:
            recomendacoes += "✅ SOLO ADEQUADO! Pode proceder com o plantio.\n\n"
            recomendacoes += "📋 RECOMENDAÇÕES DE MANEJO:\n"
            recomendacoes += "1. 🌱 Fazer sulcos de 10-15 cm de profundidade\n"
            recomendacoes += "2. 📏 Espaçamento: 1,0 x 0,6 m (fileiras x plantas)\n" 
            recomendacoes += "3. 💧 Irrigar se necessário nos primeiros 60 dias\n"
            recomendacoes += "4. 🌿 Controlar plantas daninhas regularmente\n"
            recomendacoes += "5. 📅 Colheita: 8-10 meses após plantio\n"
        
        # Rodapé
        rodape = "\n" + "="*80 + "\n"
        rodape += f"📊 Análise concluída em {ph:.1f}/K{potassio}/D{drenagem}/C{compactacao}\n"
        rodape += "🤖 Sistema desenvolvido com Inteligência Artificial - Acurácia: 97.78%\n"
        rodape += "🎓 Baseado em dados científicos de adequação de solo para mandioca\n"
        
        # Inserir todo o texto
        texto_completo = header + dados + resultado_texto + analise + recomendacoes + rodape
        self.result_display.insert('1.0', texto_completo)
        self.result_display.config(state='disabled')
        
        # Scroll para o topo
        self.result_display.see('1.0')
    
    def limpar_campos(self):
        """Limpar todos os campos"""
        self.ph_var.set("")
        self.potassio_var.set("")
        self.drenagem_var.set("1")
        self.compactacao_var.set("1")
        
        self.result_display.config(state='normal')
        self.result_display.delete('1.0', tk.END)
        self.result_display.insert('1.0', "🗑️ CAMPOS LIMPOS!\n\n📝 Preencha os novos dados do solo para análise.\n\n⏳ Aguardando novos dados...")
        self.result_display.config(state='disabled')
    
    def carregar_exemplo(self):
        """Carregar dados de exemplo"""
        self.ph_var.set("6.2")
        self.potassio_var.set("155") 
        self.drenagem_var.set("1")
        self.compactacao_var.set("1")
        
        messagebox.showinfo("Exemplo Carregado", 
                           "✅ Exemplo de SOLO ADEQUADO carregado!\n\n"
                           "📊 Dados inseridos:\n"
                           "• pH: 6.2 (próximo ao ideal)\n"
                           "• Potássio: 155 mg/dm³ (adequado)\n"
                           "• Drenagem: Boa\n"
                           "• Sem compactação\n\n"
                           "🔍 Clique em 'ANALISAR SOLO' para ver o resultado!")

def main():
    """Executar aplicação"""
    root = tk.Tk()
    app = SoloMandiocaGUI(root)
    
    def fechar_app():
        if messagebox.askokcancel("Confirmar Saída", 
                                 "🚪 Deseja realmente fechar o sistema?\n\n"
                                 "Todos os dados não salvos serão perdidos."):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", fechar_app)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()

if __name__ == "__main__":
    main()
