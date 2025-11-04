# bizarro_slayer_selector.py
import tkinter as tk
from tkinter import ttk, messagebox

# Configuración
max_pros = 3
max_contras = 3

pros = {
    "Fuerza +5": {"atk": 5},
    "Vida +20": {"hp": 20},
    "Crítico +10%": {"crit": 0.10},
    "Regeneración +3/turno": {"regen": 3},
    "Velocidad +2": {"speed": 2},
    "Evasión +10%": {"evade": 0.10},
    "Oro +25%": {"gold_mult": 1.25},
}

contras = {
    "Fragilidad -15 HP": {"hp": -15},
    "Sangrado constante -2/turno": {"bleed": 2},
    "Pereza -2 velocidad": {"speed": -2},
    "Debilidad -3 fuerza": {"atk": -3},
    "Miedo -10% crítico": {"crit": -0.10},
    "Torpeza -10% esquiva": {"evade": -0.10},
    "Maldición: menos de 25% oro": {"gold_mult": 0.75}
}

class SelectorApp:
    def __init__(self, window, main_window):
        self.window = window
        self.main_window = main_window
        self.window.title("Selecciona Pros y Contras")
        self.window.geometry("600x500")
        self.window.configure(bg='#34495e')
        self.window.protocol("WM_DELETE_WINDOW", self.volver_menu)
        
        # Centrar ventana
        self.center_window(600, 500)
        
        # Variables para checkboxes
        self.pro_vars = {p: tk.IntVar() for p in pros}
        self.con_vars = {c: tk.IntVar() for c in contras}
        self.selected_pros = []
        self.selected_contras = []
        
        self.crear_interfaz()
    
    def center_window(self, width, height):
        """Centra la ventana en la pantalla"""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def crear_interfaz(self):
        """Crea la interfaz de selección"""
        # Título
        title_frame = ttk.Frame(self.window)
        title_frame.pack(pady=10, fill='x')
        
        ttk.Label(title_frame, text="Crea tu Personaje", 
                 font=('Helvetica', 16, 'bold')).pack(pady=5)
        
        # Nombre del jugador
        name_frame = ttk.Frame(self.window)
        name_frame.pack(pady=10, fill='x', padx=20)
        
        ttk.Label(name_frame, text="Nombre del jugador:").pack(side='left')
        self.nombre_entry = ttk.Entry(name_frame, width=20, font=('Helvetica', 12))
        self.nombre_entry.pack(side='left', padx=10)
        self.nombre_entry.insert(0, "Héroe")
        
        # Frame principal para pros y contras
        main_frame = ttk.Frame(self.window)
        main_frame.pack(pady=10, fill='both', expand=True, padx=20)
        
        # Frame para Pros
        pros_frame = ttk.LabelFrame(main_frame, text=f"Pros (elige hasta {max_pros})")
        pros_frame.pack(side='left', fill='both', expand=True, padx=5)
        
        # Frame para Contras
        contras_frame = ttk.LabelFrame(main_frame, text=f"Contras (elige hasta {max_contras})")
        contras_frame.pack(side='right', fill='both', expand=True, padx=5)
        
        # Checkboxes para Pros (SIN botones de información)
        for pro in pros:
            cb = ttk.Checkbutton(pros_frame, text=pro, variable=self.pro_vars[pro],
                               command=lambda p=pro: self.actualizar_pro(p))
            cb.pack(anchor='w', padx=5, pady=2)
        
        # Checkboxes para Contras (SIN botones de información)
        for contra in contras:
            cb = ttk.Checkbutton(contras_frame, text=contra, variable=self.con_vars[contra],
                               command=lambda c=contra: self.actualizar_contra(c))
            cb.pack(anchor='w', padx=5, pady=2)
        
        # Contadores
        self.contador_frame = ttk.Frame(self.window)
        self.contador_frame.pack(pady=10)
        
        self.contador_label = ttk.Label(self.contador_frame, 
                                       text="Pros: 0/3 | Contras: 0/3",
                                       font=('Helvetica', 12, 'bold'))
        self.contador_label.pack()
        
        # Botones
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Comenzar Juego", 
                  command=self.iniciar_juego).pack(side='left', padx=10)
        
        ttk.Button(button_frame, text="Volver al Menú", 
                  command=self.volver_menu).pack(side='left', padx=10)
    
    def actualizar_pro(self, pro):
        """Actualiza la selección de pros"""
        if self.pro_vars[pro].get():
            if len(self.selected_pros) < max_pros:
                self.selected_pros.append(pro)
            else:
                self.pro_vars[pro].set(0)
                messagebox.showwarning("Límite alcanzado", 
                                     f"Solo puedes elegir hasta {max_pros} pros")
        else:
            if pro in self.selected_pros:
                self.selected_pros.remove(pro)
        
        self.actualizar_contador()
    
    def actualizar_contra(self, contra):
        """Actualiza la selección de contras"""
        if self.con_vars[contra].get():
            if len(self.selected_contras) < max_contras:
                self.selected_contras.append(contra)
            else:
                self.con_vars[contra].set(0)
                messagebox.showwarning("Límite alcanzado", 
                                     f"Solo puedes elegir hasta {max_contras} contras")
        else:
            if contra in self.selected_contras:
                self.selected_contras.remove(contra)
        
        self.actualizar_contador()
    
    def actualizar_contador(self):
        """Actualiza el contador de selecciones"""
        self.contador_label.config(
            text=f"Pros: {len(self.selected_pros)}/{max_pros} | Contras: {len(self.selected_contras)}/{max_contras}"
        )
    
    def iniciar_juego(self):
        """Inicia el juego con las selecciones"""
        nombre = self.nombre_entry.get().strip()
        if not nombre:
            nombre = "Héroe"
        
        if len(self.selected_pros) == 0 and len(self.selected_contras) == 0:
            respuesta = messagebox.askyesno(
                "Confirmar", 
                "No has seleccionado ningún pro ni contra. ¿Quieres continuar así?"
            )
            if not respuesta:
                return
        
        self.window.destroy()
        self.main_window.deiconify()
        
        # Importar e iniciar el juego Pygame
        from bizarro_slayer_game import iniciar_juego_pygame
        iniciar_juego_pygame(nombre, self.selected_pros, self.selected_contras)
    
    def volver_menu(self):
        """Vuelve al menú principal"""
        self.window.destroy()
        self.main_window.deiconify()