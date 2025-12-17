# bizarro_slayer_menu.py
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import threading
import pygame

# Añadir el directorio actual al path para importar los otros módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MenuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bizarro Slayer - Menú principal")
        self.root.geometry("500x450")
        self.root.configure(bg='#2c3e50')
        
        # Centrar la ventana
        self.center_window(500, 450)
        
        # Estilo
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Helvetica', 12), padding=10)
        self.style.configure('Title.TLabel', font=('Helvetica', 24, 'bold'), background='#2c3e50', foreground='#ecf0f1')
        
        # Variables para controlar el juego
        self.juego_activo = False
        self.game_thread = None
        
        self.crear_interfaz()
        
        # Manejar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.salir_seguro)
    
    def center_window(self, width, height):
        """Centra la ventana en la pantalla"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def crear_interfaz(self):
        """Crea la interfaz del menú principal"""
        # Título
        title_label = ttk.Label(self.root, text="BIZARRO SLAYER", style='Title.TLabel')
        title_label.pack(pady=30)
        
        # Frame para botones
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Botones
        self.new_game_btn = ttk.Button(button_frame, text="Nueva Partida", 
                                      command=self.nueva_partida, width=20)
        self.new_game_btn.pack(pady=10)
        
        self.history_btn = ttk.Button(button_frame, text="Ver Historial / Top", 
                                     command=self.ver_historial, width=20)
        self.history_btn.pack(pady=10)
        
        self.exit_btn = ttk.Button(button_frame, text="Salir", 
                                  command=self.salir_seguro, width=20)
        self.exit_btn.pack(pady=10)
        
        # Créditos
        credit_label = ttk.Label(self.root, text="Desarrollado con Python + Tkinter + Pygame", 
                                background='#2c3e50', foreground='#bdc3c7')
        credit_label.pack(side='bottom', pady=10)
    
    def nueva_partida(self):
        """Abre la ventana de selección de pros y contras"""
        if self.juego_activo:
            messagebox.showinfo("Juego en curso", 
                               "Ya hay un juego en curso. Por favor espera a que termine.")
            return
            
        self.root.withdraw()  # Oculta la ventana principal
        
        # Importar aquí para evitar problemas de importación circular
        from bizarro_slayer_selector import SelectorApp
        
        selector_window = tk.Toplevel(self.root)
        
        # Crear callback para iniciar juego
        def iniciar_juego_callback(nombre, pros, contras):
            """Callback que se ejecuta cuando se inicia el juego desde el selector"""
            selector_window.destroy()
            self.iniciar_juego(nombre, pros, contras)
        
        # Pasar el callback al selector
        app = SelectorApp(selector_window, self.root, iniciar_juego_callback)
    
    def iniciar_juego(self, nombre, pros, contras):
        """Inicia el juego en un hilo separado"""
        if self.juego_activo:
            return
            
        self.juego_activo = True
        
        # Deshabilitar botones mientras el juego está activo
        self.new_game_btn.config(state='disabled')
        self.history_btn.config(state='disabled')
        
        # Crear un hilo para el juego
        self.game_thread = threading.Thread(
            target=self.ejecutar_juego,
            args=(nombre, pros, contras),
            daemon=True
        )
        self.game_thread.start()
    
    def ejecutar_juego(self, nombre, pros, contras):
        """Función que ejecuta el juego en un hilo separado"""
        try:
            # Importar aquí para evitar problemas de inicialización
            from bizarro_slayer_game import iniciar_juego_pygame
            
            print(f"Iniciando juego para {nombre}...")
            
            # Ejecutar el juego y capturar el resultado
            resultado = iniciar_juego_pygame(nombre, pros, contras)
            
            print(f"Juego terminado. Resultado: {resultado}")
            
        except Exception as e:
            print(f"Error en el juego: {e}")
            import traceback
            traceback.print_exc()
            
            # Mostrar error en la interfaz principal
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error en el juego: {str(e)}"))
        
        finally:
            # Cuando el juego termina, volver a habilitar botones
            self.juego_activo = False
            
            # Limpiar Pygame para la próxima partida
            try:
                pygame.quit()
            except:
                pass
            
            # Volver a mostrar el menú
            self.root.after(0, self.finalizar_juego)
    
    def finalizar_juego(self):
        """Limpia después de que termina el juego"""
        # Rehabilitar botones
        self.new_game_btn.config(state='normal')
        self.history_btn.config(state='normal')
        
        # Asegurarse de que la ventana principal sea visible
        self.root.deiconify()
        
        print("Juego terminado, mostrando menú...")
    
    def ver_historial(self):
        """Abre la ventana del historial"""
        if self.juego_activo:
            messagebox.showinfo("Juego en curso", 
                               "No puedes ver el historial mientras hay un juego en curso.")
            return
            
        try:
            from bizarro_slayer_historial import HistorialApp
            historial_window = tk.Toplevel(self.root)
            app = HistorialApp(historial_window)
        except Exception as e:
            print(f"Error al abrir historial: {e}")
            messagebox.showerror("Error", f"No se pudo abrir el historial: {str(e)}")
    
    def salir_seguro(self):
        """Cierra la aplicación de forma segura"""
        if self.juego_activo:
            respuesta = messagebox.askyesno(
                "Confirmar salida",
                "Hay un juego en curso. ¿Estás seguro de que quieres salir?"
            )
            if not respuesta:
                return
        
        # Cerrar pygame si está activo
        try:
            pygame.quit()
        except:
            pass
        
        self.root.quit()
        self.root.destroy()
        os._exit(0)  # Forzar cierre completo

def main():
    root = tk.Tk()
    app = MenuApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()