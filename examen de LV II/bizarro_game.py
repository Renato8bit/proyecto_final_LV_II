"""
bizarro_game.py
Juego simple en Python + Tkinter:
- Menu principal
- Seleccion de Pros y Contras (elige un numero limitado)
- Combate por turnos contra monstruos bizarros
- Guardado simple en saves.csv

Autor: ejemplo para proyecto de Lenguajes Visuales II
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random
import csv
import os


# Datos: pros, contras, monstruos

PROS = {
    "Fuerza +2": {"atk": 2},
    "Vida +10": {"hp": 10},
    "Crítico +10%": {"crit_chance": 0.10},
    "Esquiva +10%": {"evade": 0.10},
    "Regeneración +3/turno": {"regen": 3},
}

CONTRAS = {
    "Torpe -10% esquiva": {"evade": -0.10},
    "Miedo a lo raro -5 atk vs bichos raros": {"atk_vs_rare": -5},
    "Fragilidad -10 HP": {"hp": -10},
    "Sangrado: -2 HP/turno": {"bleed": 2},
    "Codicia: +10% oro pero -5% XP": {"gold_mult": 0.10, "xp_mult": -0.05},
}

MONSTRUOS = [
    {"name": "Gusano de Reloj", "hp": 35, "atk": 6, "quirk": "retrasa_turno"},
    {"name": "Cangrejo Polifónico", "hp": 28, "atk": 8, "quirk": "vuelve_locos_los_controles"},
    {"name": "Hongo Hipnótico", "hp": 22, "atk": 5, "quirk": "dormir"},
    {"name": "Molusco Óseo", "hp": 40, "atk": 9, "quirk": "armadura"},
    {"name": "Rana Prisma", "hp": 30, "atk": 7, "quirk": "rebota_daño"},
]

SAVE_FILE = "saves.csv"


# Utilidades

def clamp(v, a, b):
    return max(a, min(b, v))

def ensure_save_file():
    if not os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name","hp_max","atk","wins"])

def save_player_summary(name, hp_max, atk, wins):
    ensure_save_file()
  
    with open(SAVE_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([name, hp_max, atk, wins])


# Clases del juego

class Character:
    def __init__(self, name="Héroe"):
        self.name = name
        self.base_hp = 50
        self.base_atk = 8
        self.hp = self.base_hp
        self.atk = self.base_atk
        self.crit_chance = 0.05
        self.evade = 0.0
        self.regen = 0
        self.effects = {}  
        self.gold = 0
        self.xp = 0
        self.wins = 0

    def apply_pro_con(self, pros_selected, cons_selected):
        
        self.base_hp = 50
        self.base_atk = 8
        self.hp = self.base_hp
        self.atk = self.base_atk
        self.crit_chance = 0.05
        self.evade = 0.0
        self.regen = 0
        self.effects = {}
        self.gold = 0
        self.xp = 0

       
        for p in pros_selected:
            data = PROS.get(p, {})
            self.atk += data.get("atk", 0)
            self.base_hp += data.get("hp", 0)
            self.crit_chance += data.get("crit_chance", 0)
            self.evade += data.get("evade", 0)
            self.regen += data.get("regen", 0)

        
        for c in cons_selected:
            data = CONTRAS.get(c, {})
            self.atk += data.get("atk_vs_rare", 0) 
            self.base_hp += data.get("hp", 0)
           
            if "bleed" in data:
                self.effects["bleed_init"] = data["bleed"]
            
            self.gold_mult = 1 + data.get("gold_mult", 0)
            self.xp_mult = 1 + data.get("xp_mult", 0)

        
        self.hp = self.base_hp

    def take_damage(self, d):
        self.hp = clamp(self.hp - d, 0, 9999)

    def heal(self, d):
        self.hp = clamp(self.hp + d, 0, self.base_hp)

    def is_alive(self):
        return self.hp > 0

    def attack_roll(self):
        crit = random.random() < self.crit_chance
        damage = self.atk * (2 if crit else 1)
        return int(damage), crit

class Monster:
    def __init__(self, template):
        self.name = template["name"]
        self.max_hp = template["hp"]
        self.hp = template["hp"]
        self.atk = template["atk"]
        self.quirk = template.get("quirk", None)
        
        self.armor = 0
        self.bounce = False
        if self.quirk == "armadura":
            self.armor = 3
        if self.quirk == "rebota_daño":
            self.bounce = True

    def take_damage(self, d):
      
        effective = max(0, d - self.armor)
        self.hp = clamp(self.hp - effective, 0, self.max_hp)
        return effective

    def is_alive(self):
        return self.hp > 0


# Interfaz con Tkinter

class BizarroGameApp(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("Bizarro Slayer - Tkinter")
        self.pack(fill="both", expand=True)
        self.style = ttk.Style()
        
        self.style.theme_use("clam")

      
        self.frames = {}
        for F in (MainMenu, SelectProsCons, BattleFrame):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenu")

        
        self.player = Character()
        self.current_monster = None

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show()

class MainMenu(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_app = parent
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text="Bizarro Slayer", font=("Helvetica", 20)).grid(row=0, pady=12)
        ttk.Button(self, text="Nueva partida", command=self.new_game).grid(row=1, pady=6)
        ttk.Button(self, text="Cargar/Ver guardados", command=self.show_saves).grid(row=2, pady=6)
        ttk.Button(self, text="Salir", command=self.parent_app.root.destroy).grid(row=3, pady=6)

    def new_game(self):
       
        self.parent_app.player = Character()
       
        self.parent_app.show_frame("SelectProsCons")

    def show_saves(self):
        ensure_save_file()
        lines = []
        with open(SAVE_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            lines = list(reader)
        if len(lines) <= 1:
            messagebox.showinfo("Guardados", "No hay partidas guardadas aún.")
            return
       
        top = tk.Toplevel(self)
        top.title("Guardados")
        tree = ttk.Treeview(top, columns=("name","hp","atk","wins"), show="headings")
        tree.heading("name", text="Nombre")
        tree.heading("hp", text="HP max")
        tree.heading("atk", text="Atq")
        tree.heading("wins", text="Victorias")
        for row in lines[1:]:
            tree.insert("", "end", values=row)
        tree.pack(fill="both", expand=True)

class SelectProsCons(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_app = parent
        self.selected_pros = []
        self.selected_cons = []
        self.max_pros = 2
        self.max_cons = 2

        ttk.Label(self, text="Elige tus PROS (elige hasta {})".format(self.max_pros), font=("Helvetica", 12)).grid(row=0, column=0, sticky="w", padx=10, pady=6)
        self.pro_vars = {}
        row = 1
        for p in PROS:
            var = tk.IntVar()
            cb = ttk.Checkbutton(self, text=p, variable=var, command=self.update_counts)
            cb.grid(row=row, column=0, sticky="w", padx=20)
            self.pro_vars[p] = var
            row += 1

        ttk.Label(self, text="Elige tus CONTRAS (elige hasta {})".format(self.max_cons), font=("Helvetica", 12)).grid(row=0, column=1, sticky="w", padx=10, pady=6)
        self.con_vars = {}
        row = 1
        for c in CONTRAS:
            var = tk.IntVar()
            cb = ttk.Checkbutton(self, text=c, variable=var, command=self.update_counts)
            cb.grid(row=row, column=1, sticky="w", padx=20)
            self.con_vars[c] = var
            row += 1

        ttk.Label(self, text="Nombre del héroe:").grid(row=7, column=0, padx=10, pady=8, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=7, column=1, padx=10, pady=8, sticky="w")

        ttk.Button(self, text="Comenzar partida", command=self.start_game).grid(row=8, column=0, pady=12)
        ttk.Button(self, text="Volver al menú", command=lambda: parent.show_frame("MainMenu")).grid(row=8, column=1, pady=12)

        self.info_label = ttk.Label(self, text="")
        self.info_label.grid(row=9, column=0, columnspan=2)

    def update_counts(self):
        pros = [k for k, v in self.pro_vars.items() if v.get()]
        cons = [k for k, v in self.con_vars.items() if v.get()]
        
        if len(pros) > self.max_pros:
           
            choice = pros.pop()
            self.pro_vars[choice].set(0)
            pros = [k for k, v in self.pro_vars.items() if v.get()]
        if len(cons) > self.max_cons:
            choice = cons.pop()
            self.con_vars[choice].set(0)
            cons = [k for k, v in self.con_vars.items() if v.get()]

        self.selected_pros = pros
        self.selected_cons = cons
        self.info_label.config(text=f"Pros: {len(self.selected_pros)}/{self.max_pros}  -  Contras: {len(self.selected_cons)}/{self.max_cons}")

    def start_game(self):
        name = self.name_entry.get().strip() or "Héroe"
        self.parent_app.player = Character(name)
   
        self.update_counts()
        self.parent_app.player.apply_pro_con(self.selected_pros, self.selected_cons)
        messagebox.showinfo("Partida", f"¡Bien {name}! Pros: {', '.join(self.selected_pros) or 'Ninguno'}\nContras: {', '.join(self.selected_cons) or 'Ninguno'}")
        self.parent_app.show_frame("BattleFrame")

class BattleFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent_app = parent
        self.turn = "player" 
        self.log_lines = []

    
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

       
        player_panel = ttk.Frame(self)
        player_panel.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        ttk.Label(player_panel, text="Jugador", font=("Helvetica", 12)).pack(anchor="w")
        self.player_stats = ttk.Label(player_panel, text="", justify="left")
        self.player_stats.pack(anchor="w", pady=4)

        # Monster panel
        monster_panel = ttk.Frame(self)
        monster_panel.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        ttk.Label(monster_panel, text="Monstruo", font=("Helvetica", 12)).pack(anchor="w")
        self.monster_stats = ttk.Label(monster_panel, text="", justify="left")
        self.monster_stats.pack(anchor="w", pady=4)

        
        self.log = tk.Text(self, height=12, state="disabled")
        self.log.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=8, pady=(0,8))

        # Controles
        controls = ttk.Frame(self)
        controls.grid(row=2, column=0, columnspan=2, pady=8)
        ttk.Button(controls, text="Atacar", command=self.player_attack).grid(row=0, column=0, padx=6)
        ttk.Button(controls, text="Curar (+5)", command=self.player_heal).grid(row=0, column=1, padx=6)
        ttk.Button(controls, text="Salvar partida", command=self.save_game).grid(row=0, column=2, padx=6)
        ttk.Button(controls, text="Volver al menú", command=self.quit_to_menu).grid(row=0, column=3, padx=6)

    def on_show(self):
       
        self.new_combat()

    def new_combat(self):
        template = random.choice(MONSTRUOS)
        self.parent_app.current_monster = Monster(template)
        self.turn = "player"
        self.log_lines = []
        self.append_log(f"¡Aparece {self.parent_app.current_monster.name}!")
        self.update_labels()

    def update_labels(self):
        p = self.parent_app.player
        m = self.parent_app.current_monster
        p_text = f"Nombre: {p.name}\nHP: {p.hp}/{p.base_hp}\nAtq: {p.atk}\nCrit: {int(p.crit_chance*100)}%\nEvade: {int(p.evade*100)}%\nEfectos: {', '.join([f'{k}:{v}' for k,v in p.effects.items()]) or 'Ninguno'}"
        m_text = f"Nombre: {m.name}\nHP: {m.hp}/{m.max_hp}\nAtq: {m.atk}\nQuirk: {m.quirk or 'Ninguno'}\nArmadura: {m.armor}"
        self.player_stats.config(text=p_text)
        self.monster_stats.config(text=m_text)
      
        self.log.config(state="normal")
        self.log.delete("1.0", "end")
        self.log.insert("end", "\n".join(self.log_lines[-200:]))
        self.log.config(state="disabled")

    def append_log(self, text):
        self.log_lines.append(text)
        self.update_labels()

    def player_attack(self):
        p = self.parent_app.player
        m = self.parent_app.current_monster
        if not p.is_alive() or not m.is_alive():
            messagebox.showinfo("Info", "La batalla terminó. Comienza otra.")
            self.new_combat()
            return

      
        if random.random() < m.atk * 0:  
            pass

        damage, crit = p.attack_roll()
        
        if any(c.startswith("Miedo a lo raro") for c in self.parent_app.frames["SelectProsCons"].selected_cons):
            
            if m.quirk:
                damage += -5  
        
        dealt = m.take_damage(damage)
        self.append_log(f"Tú atacas por {damage} ({'CRÍTICO! ' if crit else ''}efectivo {dealt}).")
       
        if m.bounce and dealt > 0:
            back = max(1, int(dealt * 0.4))
            p.take_damage(back)
            self.append_log(f"¡{m.name} rebota consecuencias! Recibes {back} de daño.")

        if "bleed_init" in p.effects:
            p.effects["bleed"] = p.effects.get("bleed", 0) + p.effects["bleed_init"]

        if not m.is_alive():
            self.append_log(f"¡Has derrotado a {m.name}!")
            p.wins += 1
            
            gold = random.randint(5, 20)
            xp = random.randint(10, 30)
           
            gold = int(gold * getattr(p, "gold_mult", 1))
            xp = int(xp * getattr(p, "xp_mult", 1))
            p.gold += gold
            p.xp += xp
            self.append_log(f"Recibes {gold} oro y {xp} XP.")
            
            save_player_summary(p.name, p.base_hp, p.atk, p.wins)
            
            self.append_log("Un nuevo monstruo aparece en segundos...")
            self.new_combat()
            return

        
        self.root_after(800, self.monster_turn)

    def player_heal(self):
        p = self.parent_app.player
        if p.hp >= p.base_hp:
            self.append_log("Estás al máximo de vida.")
            return
        amount = 5
        p.heal(amount)
        self.append_log(f"Te curas {amount} HP.")
       
        self.root_after(800, self.monster_turn)

    def monster_turn(self):
        p = self.parent_app.player
        m = self.parent_app.current_monster
        if not m.is_alive() or not p.is_alive():
            return
       
        if m.quirk == "dormir" and random.random() < 0.25:
            self.append_log(f"{m.name} parece somnoliento y pierde su turno.")
            self.update_labels()
            return

        
        damage = m.atk
      
        if random.random() < p.evade:
            self.append_log(f"Esquivaste el ataque de {m.name}!")
            self.update_labels()
            return
        p.take_damage(damage)
        self.append_log(f"{m.name} te golpea por {damage}.")

        if m.quirk == "retrasa_turno" and random.random() < 0.2:
            self.append_log(f"{m.name} manipula el tiempo: pierdes tu siguiente acción (¡extra raro!).")
            self.root_after(800, self.monster_turn)
            return

        if "bleed" in p.effects and p.effects["bleed"] > 0:
            b = p.effects["bleed"]
            p.take_damage(b)
            self.append_log(f"Sufres {b} de sangrado por efectos de contras.")
            p.effects["bleed"] = max(0, p.effects["bleed"] - 1)

        if not p.is_alive():
            self.append_log("Has muerto... Fin de la partida.")
            messagebox.showinfo("Perdiste", "Has muerto. Volviendo al menú.")
            self.parent_app.show_frame("MainMenu")
            return

        self.update_labels()

    def root_after(self, ms, func):
        self.after(ms, func)

    def save_game(self):
        p = self.parent_app.player
        save_player_summary(p.name, p.base_hp, p.atk, p.wins)
        messagebox.showinfo("Guardado", "Partida guardada (resumen).")

    def quit_to_menu(self):
        confirm = messagebox.askyesno("Confirmar", "Volver al menú detendrá la partida actual. ¿Continuar?")
        if confirm:
            self.parent_app.show_frame("MainMenu")


# Ejecutar App

def main():
    root = tk.Tk()
    app = BizarroGameApp(root)
    root.geometry("800x560")
    root.mainloop()

if __name__ == "__main__" :
    main()