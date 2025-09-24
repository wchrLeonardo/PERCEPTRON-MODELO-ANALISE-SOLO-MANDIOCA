import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import os
import sys

# Importa as funções do modelo
try:
    from treinamento_aprimorado import PerceptronAprimorado, pre_processar_dados, carregar_dados_brutos
except ImportError:
    messagebox.showerror("Erro", "Arquivo 'treinamento_aprimorado.py' não encontrado!")
    sys.exit()

class SoloMandiocaGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_style()
        self.modelo_treinado = False
        self.perceptron = None
        self.min_vals = None
        self.max_vals = None
        
        # Criar interface
        self.create_widgets()
        self.carregar_modelo()
    
    def setup_window(self):
        """Configuração básica da janela"""
        self.root.title("🌾 Sistema de Análise de Solo para Mandioca")
        self.root.geometry("900x800")
        self.root.configure(bg='#f0f8ff')
        
        # Centralizar janela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"900x800+{x}+{y}")
        
        # Ícone (se disponível)
        try:
            self.root.iconbitmap("icone.ico")
        except:
            pass
    
    def setup_style(self):
        """Configuração dos estilos personalizados"""
        self.style = ttk.Style()
        
        # Configurar tema
        self.style.theme_use('clam')
        
        # Estilos personalizados
        self.style.configure('Title.TLabel', 
                           font=('Arial', 20, 'bold'), 
                           foreground='#2c5f2d', 
                           background='#f0f8ff')
        
        self.style.configure('Subtitle.TLabel', 
                           font=('Arial', 12, 'bold'), 
                           foreground='#2c5f2d', 
                           background='#f0f8ff')
        
        self.style.configure('Info.TLabel', 
                           font=('Arial', 10), 
                           foreground='#333333', 
                           background='#f0f8ff')
        
        self.style.configure('Success.TButton', 
                           font=('Arial', 11, 'bold'),
                           foreground='white')
        
        self.style.map('Success.TButton',
                      background=[('active', '#45a049'), ('!active', '#4CAF50')])
        
        self.style.configure('Warning.TButton', 
                           font=('Arial', 11, 'bold'),
                           foreground='white')
        
        self.style.map('Warning.TButton',
                      background=[('active', '#f44336'), ('!active', '#ff5722')])
    
    def create_widgets(self):
        """Criar todos os widgets da interface"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#f0f8ff', padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, 
                               text="🌾 SISTEMA DE ANÁLISE DE SOLO PARA MANDIOCA", 
                               style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Subtitle
        subtitle_label = ttk.Label(main_frame, 
                                 text="Determine se o solo está adequado para o plantio de mandioca",
                                 style='Subtitle.TLabel')
        subtitle_label.pack(pady=(0, 20))
        
        # Status do modelo
        self.status_frame = tk.Frame(main_frame, bg='#f0f8ff')
        self.status_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.status_label = ttk.Label(self.status_frame, 
                                    text="🔄 Carregando modelo...", 
                                    style='Info.TLabel')
        self.status_label.pack()
        
        # Frame de entrada de dados
        input_frame = tk.LabelFrame(main_frame, 
                                   text=" 📊 Dados do Solo ", 
                                   font=('Arial', 12, 'bold'),
                                   bg='#f0f8ff',
                                   fg='#2c5f2d',
                                   padx=15, pady=15)
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Grid para organizar inputs
        self.create_input_fields(input_frame)
        
        # Frame de botões
        button_frame = tk.Frame(main_frame, bg='#f0f8ff')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botão de análise
        self.analyze_btn = ttk.Button(button_frame, 
                                    text="🔍 ANALISAR SOLO", 
                                    style='Success.TButton',
                                    command=self.analisar_solo)
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão limpar
        clear_btn = ttk.Button(button_frame, 
                             text="🗑️ LIMPAR", 
                             command=self.limpar_campos)
        clear_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão de exemplo
        example_btn = ttk.Button(button_frame, 
                               text="📝 EXEMPLO", 
                               command=self.carregar_exemplo)
        example_btn.pack(side=tk.LEFT)
        
        # Frame de resultados
        result_frame = tk.LabelFrame(main_frame, 
                                   text=" 📈 Resultado da Análise ", 
                                   font=('Arial', 12, 'bold'),
                                   bg='#f0f8ff',
                                   fg='#2c5f2d',
                                   padx=15, pady=15)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        # Área de resultado
        self.result_text = scrolledtext.ScrolledText(result_frame, 
                                                   height=15, 
                                                   width=80,
                                                   font=('Consolas', 10),
                                                   bg='#ffffff',
                                                   fg='#333333',
                                                   wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Texto inicial
        self.result_text.insert(tk.END, 
                               "🌱 Bem-vindo ao Sistema de Análise de Solo para Mandioca!\n\n"
                               "📋 Instruções:\n"
                               "1. Preencha os dados do seu solo nos campos acima\n"
                               "2. Clique em 'ANALISAR SOLO' para obter o resultado\n"
                               "3. Veja as recomendações personalizadas aqui\n\n"
                               "💡 Dica: Use o botão 'EXEMPLO' para ver dados de teste\n\n"
                               "⏳ Aguardando dados para análise...")
    
    def create_input_fields(self, parent):
        """Criar campos de entrada de dados"""
        
        # Grid configuration
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_columnconfigure(3, weight=1)
        
        # pH
        ttk.Label(parent, text="🧪 pH do Solo:", font=('Arial', 11, 'bold')).grid(
            row=0, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 15))
        
        self.ph_var = tk.StringVar()
        self.ph_entry = ttk.Entry(parent, textvariable=self.ph_var, font=('Arial', 11), width=15)
        self.ph_entry.grid(row=0, column=1, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(parent, text="(Ex: 6.0)", font=('Arial', 9), foreground='gray').grid(
            row=0, column=2, sticky=tk.W, padx=(5, 20), pady=(0, 15))
        
        # Potássio
        ttk.Label(parent, text="⚡ Potássio (mg/dm³):", font=('Arial', 11, 'bold')).grid(
            row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 15))
        
        self.potassio_var = tk.StringVar()
        self.potassio_entry = ttk.Entry(parent, textvariable=self.potassio_var, font=('Arial', 11), width=15)
        self.potassio_entry.grid(row=1, column=1, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(parent, text="(Ex: 120)", font=('Arial', 9), foreground='gray').grid(
            row=1, column=2, sticky=tk.W, padx=(5, 20), pady=(0, 15))
        
        # Drenagem
        ttk.Label(parent, text="💧 Boa Drenagem:", font=('Arial', 11, 'bold')).grid(
            row=2, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 15))
        
        self.drenagem_var = tk.StringVar(value="1")
        drenagem_frame = tk.Frame(parent, bg='#f0f8ff')
        drenagem_frame.grid(row=2, column=1, sticky=tk.W, pady=(0, 15))
        
        ttk.Radiobutton(drenagem_frame, text="✅ Sim", variable=self.drenagem_var, 
                       value="1", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(drenagem_frame, text="❌ Não", variable=self.drenagem_var, 
                       value="0", style='Info.TLabel').pack(side=tk.LEFT)
        
        # Compactação
        ttk.Label(parent, text="🏔️ Solo sem Compactação:", font=('Arial', 11, 'bold')).grid(
            row=3, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 15))
        
        self.compactacao_var = tk.StringVar(value="1")
        compactacao_frame = tk.Frame(parent, bg='#f0f8ff')
        compactacao_frame.grid(row=3, column=1, sticky=tk.W, pady=(0, 15))
        
        ttk.Radiobutton(compactacao_frame, text="✅ Sim", variable=self.compactacao_var, 
                       value="1", style='Info.TLabel').pack(side=tk.LEFT, padx=(0, 15))
        ttk.Radiobutton(compactacao_frame, text="❌ Não", variable=self.compactacao_var, 
                       value="0", style='Info.TLabel').pack(side=tk.LEFT)
    
    def carregar_modelo(self):
        """Carrega o modelo em thread separada"""
        def load_model():
            try:
                self.status_label.config(text="🔄 Carregando dados...")
                self.root.update()
                
                # Carrega dados
                dados_brutos = carregar_dados_brutos('entrada_mandioca.csv')
                X_processado, y_processado, min_vals, max_vals = pre_processar_dados(dados_brutos)
                
                self.status_label.config(text="🤖 Treinando modelo...")
                self.root.update()
                
                # Treina modelo
                self.perceptron = PerceptronAprimorado(len(X_processado[0]), taxa_aprendizado=0.5)
                self.perceptron.treinar(X_processado, y_processado, epocas=100, verbose=False)
                
                self.min_vals = min_vals
                self.max_vals = max_vals
                self.modelo_treinado = True
                
                self.status_label.config(text="✅ Modelo carregado com sucesso! Pronto para análise.")
                self.analyze_btn.config(state='normal')
                
            except Exception as e:
                self.status_label.config(text=f"❌ Erro ao carregar modelo: {str(e)}")
                messagebox.showerror("Erro", f"Falha ao carregar o modelo:\n{str(e)}")
        
        # Desabilita botão enquanto carrega
        self.analyze_btn.config(state='disabled')
        
        # Executa em thread separada
        thread = threading.Thread(target=load_model)
        thread.daemon = True
        thread.start()
    
    def validar_entrada(self):
        """Valida os dados de entrada"""
        try:
            ph = float(self.ph_var.get())
            potassio = int(self.potassio_var.get())
            drenagem = int(self.drenagem_var.get())
            compactacao = int(self.compactacao_var.get())
            
            # Validações
            if not (3.0 <= ph <= 9.0):
                raise ValueError("pH deve estar entre 3.0 e 9.0")
            
            if not (0 <= potassio <= 500):
                raise ValueError("Potássio deve estar entre 0 e 500 mg/dm³")
            
            if drenagem not in [0, 1] or compactacao not in [0, 1]:
                raise ValueError("Valores de drenagem e compactação inválidos")
            
            return ph, potassio, drenagem, compactacao
            
        except ValueError as e:
            if "could not convert" in str(e):
                raise ValueError("Por favor, preencha todos os campos com valores numéricos válidos")
            else:
                raise e
    
    def analisar_solo(self):
        """Realiza a análise do solo"""
        if not self.modelo_treinado:
            messagebox.showerror("Erro", "Modelo ainda não foi carregado!")
            return
        
        try:
            # Valida entrada
            ph, potassio, drenagem, compactacao = self.validar_entrada()
            
            # Pré-processamento
            distancia_ph = abs(ph - 6.0)
            ph_norm = (distancia_ph - self.min_vals[0]) / (self.max_vals[0] - self.min_vals[0]) if self.max_vals[0] != self.min_vals[0] else 0
            k_norm = (potassio - self.min_vals[1]) / (self.max_vals[1] - self.min_vals[1]) if self.max_vals[1] != self.min_vals[1] else 0
            
            entrada_processada = [ph_norm, k_norm, drenagem, compactacao]
            
            # Predição
            resultado = self.perceptron.prever(entrada_processada)
            
            # Cálculo da confiança
            soma_ponderada = self.perceptron.bias
            for i, peso in enumerate(self.perceptron.pesos):
                soma_ponderada += peso * entrada_processada[i]
            
            confianca = min(abs(soma_ponderada) * 100, 100)
            
            # Exibe resultado
            self.exibir_resultado(ph, potassio, drenagem, compactacao, resultado, confianca)
            
        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro durante análise: {str(e)}")
    
    def exibir_resultado(self, ph, potassio, drenagem, compactacao, resultado, confianca):
        """Exibe o resultado da análise"""
        
        # Limpa área de resultado
        self.result_text.delete(1.0, tk.END)
        
        # Header
        self.result_text.insert(tk.END, "="*70 + "\n")
        self.result_text.insert(tk.END, "🌾 RESULTADO DA ANÁLISE DE SOLO PARA MANDIOCA\n")
        self.result_text.insert(tk.END, "="*70 + "\n\n")
        
        # Dados inseridos
        self.result_text.insert(tk.END, "📊 DADOS ANALISADOS:\n")
        self.result_text.insert(tk.END, f"   • pH: {ph:.1f}\n")
        self.result_text.insert(tk.END, f"   • Potássio: {potassio} mg/dm³\n")
        self.result_text.insert(tk.END, f"   • Drenagem: {'Boa' if drenagem == 1 else 'Ruim'}\n")
        self.result_text.insert(tk.END, f"   • Compactação: {'Ausente' if compactacao == 1 else 'Presente'}\n\n")
        
        # Resultado principal
        if resultado == 1:
            self.result_text.insert(tk.END, "🎉 RESULTADO FINAL: SOLO APTO PARA MANDIOCA!\n")
            self.result_text.insert(tk.END, f"🎯 Confiança: {confianca:.1f}%\n\n")
            cor_resultado = "#4CAF50"
        else:
            self.result_text.insert(tk.END, "⚠️  RESULTADO FINAL: SOLO NÃO APTO PARA MANDIOCA\n")
            self.result_text.insert(tk.END, f"🎯 Confiança: {confianca:.1f}%\n\n")
            cor_resultado = "#f44336"
        
        # Análise detalhada
        self.result_text.insert(tk.END, "🔍 ANÁLISE DETALHADA:\n\n")
        
        # pH
        if abs(ph - 6.0) < 0.5:
            self.result_text.insert(tk.END, f"✅ pH {ph:.1f}: EXCELENTE (próximo ao ideal 6.0)\n")
        elif abs(ph - 6.0) < 1.0:
            self.result_text.insert(tk.END, f"⚠️  pH {ph:.1f}: BOM (razoavelmente próximo ao ideal)\n")
        else:
            self.result_text.insert(tk.END, f"❌ pH {ph:.1f}: PROBLEMÁTICO (muito distante do ideal 6.0)\n")
        
        # Potássio
        if potassio >= 120:
            self.result_text.insert(tk.END, f"✅ Potássio {potassio} mg/dm³: ADEQUADO\n")
        elif potassio >= 80:
            self.result_text.insert(tk.END, f"⚠️  Potássio {potassio} mg/dm³: MODERADO\n")
        else:
            self.result_text.insert(tk.END, f"❌ Potássio {potassio} mg/dm³: BAIXO\n")
        
        # Drenagem
        self.result_text.insert(tk.END, f"{'✅' if drenagem == 1 else '❌'} Drenagem: {'BOA' if drenagem == 1 else 'RUIM'}\n")
        
        # Compactação
        self.result_text.insert(tk.END, f"{'✅' if compactacao == 1 else '❌'} Compactação: {'AUSENTE' if compactacao == 1 else 'PRESENTE'}\n\n")
        
        # Recomendações
        self.result_text.insert(tk.END, "💡 RECOMENDAÇÕES:\n\n")
        
        if resultado == 0:
            recomendacoes = []
            if abs(ph - 6.0) > 0.5:
                if ph < 6.0:
                    recomendacoes.append("📈 Aplicar calcário para corrigir acidez do solo")
                else:
                    recomendacoes.append("📉 Aplicar enxofre ou matéria orgânica para baixar pH")
            
            if drenagem == 0:
                recomendacoes.append("🚿 Implementar sistema de drenagem adequado")
                recomendacoes.append("🏗️  Construir canteiros elevados ou sulcos de drenagem")
            
            if compactacao == 0:
                recomendacoes.append("🚜 Fazer subsolagem para descompactar o solo")
                recomendacoes.append("⚠️  Evitar tráfego pesado em solo úmido")
            
            if potassio < 100:
                recomendacoes.append("⚡ Aplicar fertilizante potássico (cloreto ou sulfato de K)")
            
            if not recomendacoes:
                recomendacoes.append("🔍 Consultar técnico agrícola para análise mais detalhada")
            
            for i, rec in enumerate(recomendacoes, 1):
                self.result_text.insert(tk.END, f"{i}. {rec}\n")
        else:
            self.result_text.insert(tk.END, "✅ Solo adequado! Proceda com o plantio da mandioca.\n")
            self.result_text.insert(tk.END, "🌱 Mantenha as boas práticas de manejo do solo.\n")
            self.result_text.insert(tk.END, "📅 Monitore periodicamente as condições do solo.\n")
        
        self.result_text.insert(tk.END, "\n" + "="*70 + "\n")
        self.result_text.insert(tk.END, "📋 Análise concluída com sucesso!\n")
        self.result_text.insert(tk.END, "🤖 Sistema desenvolvido com Inteligência Artificial\n")
        
        # Scroll para o início
        self.result_text.see(1.0)
    
    def limpar_campos(self):
        """Limpa todos os campos"""
        self.ph_var.set("")
        self.potassio_var.set("")
        self.drenagem_var.set("1")
        self.compactacao_var.set("1")
        
        # Limpa resultado
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, 
                               "🗑️  Campos limpos!\n\n"
                               "📝 Preencha os novos dados do solo para análise.\n\n"
                               "⏳ Aguardando novos dados...")
    
    def carregar_exemplo(self):
        """Carrega dados de exemplo"""
        # Exemplo de solo bom para mandioca
        self.ph_var.set("6.2")
        self.potassio_var.set("155")
        self.drenagem_var.set("1")
        self.compactacao_var.set("1")
        
        messagebox.showinfo("Exemplo Carregado", 
                           "✅ Dados de exemplo carregados!\n\n"
                           "Este é um exemplo de solo adequado para mandioca:\n"
                           "• pH próximo ao ideal (6.2)\n"
                           "• Potássio adequado (155 mg/dm³)\n"
                           "• Boa drenagem\n"
                           "• Sem compactação\n\n"
                           "Clique em 'ANALISAR SOLO' para ver o resultado!")

def main():
    """Função principal"""
    root = tk.Tk()
    app = SoloMandiocaGUI(root)
    
    # Tratamento de fechamento
    def on_closing():
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
