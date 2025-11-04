# bizarro_slayer_historial.py
import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

save_file = "historial.csv"

def ensure_save_file():
    """Asegura que el archivo de guardado exista"""
    if not os.path.exists(save_file):
        with open(save_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Jugador", "Puntos", "Victorias", "Pros", "Contras"])

def load_top_players(limit=10):
    """Carga los mejores jugadores del historial"""
    ensure_save_file()
    players = []
    try:
        with open(save_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                players.append(row)
        
        # Ordenar por puntos (mayor a menor)
        players.sort(key=lambda x: int(x["Puntos"]), reverse=True)
        return players[:limit]
    except Exception as e:
        print(f"Error cargando historial: {e}")
        return []

class HistorialApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Historial de Jugadores")
        self.window.geometry("800x500")
        self.window.configure(bg='#34495e')
        
        # Centrar ventana
        self.center_window(800, 500)
        
        self.crear_interfaz()
        self.cargar_datos()
    
    def center_window(self, width, height):
        """Centra la ventana en la pantalla"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def crear_interfaz(self):
        """Crea la interfaz del historial"""
        # Título
        title_frame = ttk.Frame(self.window)
        title_frame.pack(pady=15, fill='x')
        
        ttk.Label(title_frame, text="🏆 TOP JUGADORES 🏆", 
                 font=('Helvetica', 18, 'bold')).pack()
        
        # Frame para la tabla
        table_frame = ttk.Frame(self.window)
        table_frame.pack(pady=10, fill='both', expand=True, padx=20)
        
        # Treeview para mostrar los datos
        self.tree = ttk.Treeview(table_frame, 
                                columns=("Posición", "Jugador", "Puntos", "Victorias", "Pros", "Contras"),
                                show="headings",
                                height=15)
        
        # Configurar columnas
        column_widths = {
            "Posición": 80,
            "Jugador": 120,
            "Puntos": 80,
            "Victorias": 80,
            "Pros": 180,
            "Contras": 180
        }
        
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=column_widths.get(col, 100))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Botones
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=15)
        
        ttk.Button(button_frame, text="🔄 Actualizar", 
                  command=self.cargar_datos).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="🗑️ Limpiar Historial", 
                  command=self.limpiar_historial).pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Cerrar", 
                  command=self.window.destroy).pack(side='left', padx=5)
        
        # Estadísticas
        self.stats_frame = ttk.Frame(self.window)
        self.stats_frame.pack(pady=10, fill='x', padx=20)
        
        self.stats_label = ttk.Label(self.stats_frame, text="", 
                                    font=('Helvetica', 10))
        self.stats_label.pack()
    
    def cargar_datos(self):
        """Carga los datos en la tabla"""
        # Limpiar tabla existente
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        players = load_top_players()
        
        if not players:
            self.tree.insert("", "end", values=("", "No hay datos", "", "", "", ""))
            self.stats_label.config(text="No hay partidas guardadas")
            return
        
        # Insertar datos
        for i, player in enumerate(players, 1):
            # Emojis para las posiciones
            if i == 1:
                posicion = "🥇 1°"
            elif i == 2:
                posicion = "🥈 2°"
            elif i == 3:
                posicion = "🥉 3°"
            else:
                posicion = f"{i}°"
            
            self.tree.insert("", "end", values=(
                posicion,
                player["Jugador"],
                player["Puntos"],
                player["Victorias"],
                player["Pros"].replace(";", ", ") or "Ninguno",
                player["Contras"].replace(";", ", ") or "Ninguno"
            ))
        
        # Actualizar estadísticas
        total_jugadores = len(players)
        max_puntos = max(int(p["Puntos"]) for p in players) if players else 0
        max_victorias = max(int(p["Victorias"]) for p in players) if players else 0
        
        self.stats_label.config(
            text=f"Total de jugadores: {total_jugadores} | "
                 f"Máximo puntaje: {max_puntos} | "
                 f"Máximo victorias: {max_victorias}"
        )
    
    def limpiar_historial(self):
        """Limpia el historial completo"""
        respuesta = messagebox.askyesno(
            "Confirmar", 
            "¿Estás seguro de que quieres eliminar todo el historial? Esta acción no se puede deshacer."
        )
        
        if respuesta:
            try:
                if os.path.exists(save_file):
                    os.remove(save_file)
                ensure_save_file()
                self.cargar_datos()
                messagebox.showinfo("Éxito", "Historial limpiado correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo limpiar el historial: {e}")