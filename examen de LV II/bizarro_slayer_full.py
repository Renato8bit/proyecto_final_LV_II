# menu_principal.py
import tkinter as tk
from tkinter import ttk
import sys
import os

# Añadir el directorio actual al path para importar los otros módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bizarro Slayer - Menú principal")
        self.root.geometry("500x450")
        self.root.configure(bg='#2c3e50')
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'), background='#2c3e50', foreground='#ecf0f1')
        
        # Título
        title_label = ttk.Label(root, text="BIZARRO SLAYER", style='Title.TLabel')
        title_label.pack(pady=30)
        
        # Frame para botones
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=20)
        
        # Botones
        self.new_game_btn = ttk.Button(button_frame, text="Nueva Partida", 
                                      command=self.nueva_partida, width=20)
        self.new_game_btn.pack(pady=10)
        
        self.history_btn = ttk.Button(button_frame, text="Ver Historial / Top", 
                                     command=self.ver_historial, width=20)
        self.history_btn.pack(pady=10)
        
        self.exit_btn = ttk.Button(button_frame, text="Salir", 
                                  command=self.salir, width=20)
        self.exit_btn.pack(pady=10)
        
        # Créditos
        credit_label = ttk.Label(root, text="Desarrollado con Python + Tkinter + Pygame", 
                                background='#2c3e50', foreground='#bdc3c7')
        credit_label.pack(side='bottom', pady=10)
    
    def nueva_partida(self):
        """Abre la ventana de selección de pros y contras"""
        self.root.withdraw()  # Oculta la ventana principal
        from selector_procon import SelectorApp
        selector_window = tk.Toplevel(self.root)
        SelectorApp(selector_window, self.root)
    
    def ver_historial(self):
        """Abre la ventana del historial"""
        from historial import HistorialApp
        historial_window = tk.Toplevel(self.root)
        HistorialApp(historial_window)
    
    def salir(self):
        """Cierra la aplicación"""
        self.root.quit()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()