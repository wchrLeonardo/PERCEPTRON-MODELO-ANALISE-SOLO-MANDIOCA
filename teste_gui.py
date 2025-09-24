import tkinter as tk
from tkinter import messagebox

def test_gui():
    """Testa se a GUI funciona básicamente"""
    try:
        root = tk.Tk()
        root.title("Teste GUI")
        root.geometry("400x200")
        
        label = tk.Label(root, text="✅ GUI funcionando!", font=('Arial', 16))
        label.pack(pady=50)
        
        def show_success():
            messagebox.showinfo("Sucesso", "🎉 Sistema GUI está funcionando perfeitamente!")
            root.destroy()
        
        button = tk.Button(root, text="Testar Funcionalidade", command=show_success)
        button.pack(pady=20)
        
        root.after(3000, show_success)  # Auto-close após 3 segundos
        root.mainloop()
        
        return True
    except Exception as e:
        print(f"❌ Erro na GUI: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Testando sistema GUI...")
    if test_gui():
        print("✅ Teste concluído com sucesso!")
        print("🚀 Execute: python gui_mandioca_simples.py")
    else:
        print("❌ Problemas detectados na GUI")
