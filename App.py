import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import time
import pygame
import random


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.title("BuscaMinas (SiPuedes)💣")
        self.resizable(False, False)
        self.geometry("580x580")
        self.inicio = ImageTk.PhotoImage(file="inicio.jpeg")
        self.frame = tk.Frame(self, bg="#588a35")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.superior_rectangle = tk.Frame(self.frame, bg="#4a752d", height=75)
        self.superior_rectangle.pack(fill=tk.X)
        self.superior_rectangle.grid_propagate(0)
        self.square = None
        self.grafo = {}
        self.bandera_img_slot = ImageTk.PhotoImage(file="bombaButton.jpeg")
        self.bomba_png = ImageTk.PhotoImage(file="bomba.png")
        self.reloj = ImageTk.PhotoImage(file="reloj.jpeg")
        self.hover_image = tk.PhotoImage(file="dificil.png")
        self.grid = []
        self.create_difficulty_buttons()

    def clean_widgets(self):
        for widget in self.frame.winfo_children():
            if widget != self.superior_rectangle:
                widget.destroy()

    def random_color(self):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return f'#{r:02x}{g:02x}{b:02x}'

    def create_difficulty_buttons(self):
        self.clean_widgets()
        for widget in self.superior_rectangle.winfo_children():
            widget.destroy()

        self.jugadas_disponibles = 12
        self.bombas_por_encontrar = 32

        self.musica_sin_bomba = pygame.mixer.music.load('intro.mp3')
        pygame.mixer.music.play(1)

        welcome_label = tk.Label(self.frame, text="𝕭𝖎𝖊𝖓𝖛𝖊𝖓𝖎𝖉𝖔 𝖆𝖑 𝕭𝖚𝖘𝖈𝖆 𝕸𝖎𝖓𝖆𝖘 💣", bg="#4a752d", fg="white")
        welcome_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        hard_button = ctk.CTkButton(master=self.frame,
                                     fg_color=("#92b361", "#4a752d"),
                                     text="𝔡𝔦𝔣í𝔠𝔦𝔩 😱",
                                     command=lambda difficulty="Difícl": self.explicacion(difficulty),
                                     width=200, height=50)
        hard_button.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

        medium_button = ctk.CTkButton(master=self.frame,
                                       fg_color=("#92b361", "#4a752d"),
                                       text="𝖒𝖊𝖉𝖎𝖔 🫣",
                                       command=lambda difficulty="Medio ": self.explicacion(difficulty),
                                       width=200, height=50)
        medium_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        easy_button = ctk.CTkButton(master=self.frame,
                                     fg_color=("#92b361", "#4a752d"),
                                     text="𝔣á𝔠𝔦𝔩 😐",
                                     command=lambda difficulty="Fácil": self.explicacion(difficulty),
                                     width=200, height=50)
        easy_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def explicacion(self, difficulty):
        dif = difficulty
        self.clean_widgets()

        label = tk.Label(self.frame, text="Si crees que hay una bomba\nhazle click al botón y\nluego a la posición para \nmarcarla y no perder jugadas", borderwidth=0, highlightthickness=0, bg="#4a752d", font="Arial,8")
        label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        listo = ctk.CTkButton(master=self.frame,
                               fg_color=("#92b361", "#4a752d"),
                               text="¿Estás Listo? 🤔",
                               command=lambda: self.open_grid(dif),
                               width=200, height=50)

        listo.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    def open_grid(self, difficulty):
        self.clean_widgets()
        self.informacion_chart()
        self.start_time = time.time()
        self.update_timer()
        self.crear_grafo()

        colors = ["#a3d14a", "#aad852"]
        square_size = 60
        frame_width = self.frame.winfo_width()
        frame_height = self.frame.winfo_height() - 50
        x_offset = (frame_width - 8 * square_size) // 2
        y_offset = ((frame_height - 8 * square_size) // 2) + 10

        num = 0
        for i in range(8):
            for j in range(8):
                color_index = (i + j) % 2
                square = tk.Frame(self.frame, bg=colors[color_index], width=square_size, height=square_size)
                square.place(x=x_offset + j * square_size, y=y_offset + i * square_size + 50)
                square.bind("<Button-1>", self.on_click)
                self.square = square
                self.grid.append(square)
                num += 1

    def on_click(self, event):
        widget = event.widget
        index = self.grid.index(widget)
        num = index + 1

        widget.unbind("<Button-1>")
        self.jugadas_disponibles -= 1
        self.label_jugadas_disponibles.config(text=f"Jugadas Restantes: {self.jugadas_disponibles}")

        if num in self.vertices:
            random_bg_color = self.random_color()
            self.label_bomba = tk.Label(self.frame, image=self.bomba_png, borderwidth=0, highlightthickness=0, bg=random_bg_color)
            self.label_bomba.place(x=widget.winfo_x(), y=widget.winfo_y())
            widget.config(bg=random_bg_color)

            self.explotar_bombas(num)

            self.musica_sin_bomba = pygame.mixer.music.load('Bombas.wav')
            pygame.mixer.music.play(1)
            self.bombas_por_encontrar -= 1
            self.bombas_label.config(text=f"Bombas por encontrar: {self.bombas_por_encontrar}")
           
                

        else:
            current_color = widget.cget("bg")
            new_color = "#d7b899" if current_color == "#aad852" else "#e4c29f"
            widget.config(bg=new_color)

            self.musica_sin_bomba = pygame.mixer.music.load('Sin-bomba.wav')
            pygame.mixer.music.play(1)

        self.update()
        # Esperar 3 segundos antes de limpiar los widgets y mostrar el mensaje
        
        if self.terminar_juego():
            self.clean_widgets()
            time.sleep(3)
            restart_button = ctk.CTkButton(master=self.frame,
                                            fg_color=("#92b361", "#4a752d"),
                                            text="¿Quieres volver a jugar?",
                                            command=lambda: self.create_difficulty_buttons(),
                                            width=200, height=50)
            restart_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

            if self.winner():
                winner_label = tk.Label(self.frame, text="¡Ganaste! 🎉", font=("Arial", 20), bg="#4a752d", fg="white")
                winner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            else:
                loser_label = tk.Label(self.frame, text="¡Perdiste!  😕", font=("Arial", 20), bg="#4a752d", fg="white")
                loser_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
            return

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        self.label_time = tk.Label(self.superior_rectangle, text=f"{minutes:02d}:{seconds:02d}", font=("Arial", 20), bg="#4a752d", fg="white")
        self.label_time.place(relx=0.95, rely=0.5, anchor=tk.CENTER)
        self.label_time.after(1000, self.update_timer)

    def informacion_chart(self):
        boton_bandera = tk.Button(self.superior_rectangle, text=" ", image=self.bandera_img_slot, borderwidth=0, highlightthickness=0, command=self.poner_bomba())
        boton_bandera.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        boton_reloj = tk.Label(self.superior_rectangle, text=" ", image=self.reloj, borderwidth=0, highlightthickness=0)
        boton_reloj.place(relx=0.85, rely=0.5, anchor=tk.CENTER)

        self.label_jugadas_disponibles = tk.Label(self.superior_rectangle, text=f"Jugadas Restantes: {self.jugadas_disponibles}", borderwidth=0, highlightthickness=0, bg="#4a752d")
        self.label_jugadas_disponibles.place(relx=0.15, rely=0.6, anchor=tk.CENTER)

        self.bombas_label = tk.Label(self.superior_rectangle, text=f"Bombas por Encontrar: {self.bombas_por_encontrar}", borderwidth=0, highlightthickness=0, bg="#4a752d")
        self.bombas_label.place(relx=0.15, rely=0.3, anchor=tk.CENTER)

    def poner_bomba(self):
        pass

    def terminar_juego(self):
        if self.jugadas_disponibles == 0 or self.bombas_por_encontrar == 0:
            return True
        else:
            return False

    def winner(self):
        if self.bombas_por_encontrar == 0:
            return True
        else:
            return False

    def crear_grafo(self):
        self.vertices = [1, 14, 8, 61, 6, 56, 45, 21, 35, 48, 36, 43, 3, 26, 17, 58, 46, 33, 51, 41, 62, 13, 30, 7, 47, 25, 15, 54, 20, 52, 12, 24]
        self.grafo = {
            14: {1: 1, 8: 2, 6: 3},
        1: {56: 1, 45: 2},
        8: {21: 1, 35: 2},
        61: {48: 1},
        6: {36: 1, 43: 2},
        56: {3: 1, 26: 2},
        45: {17: 1, 58: 2},
        21: {46: 1, 33: 2},
        35: {51: 1, 41: 2},
        48: {62: 1},
        36: {13: 1, 30: 2},
        43: {7: 1, 47: 2},
        3: {25: 1, 15: 2},
        26: {54: 1, 20: 2},
        17: {52: 1, 12: 2},
        58: {24: 1},
        # Añade dos vértices que no estén conectados
        46: {},
        33: {},
        # Resto de los vértices conectados con al menos una arista
        51: {},
        41: {},
        62: {},
        13: {},
        30: {},
        7: {},
        47: {},
        25: {},
        15: {},
        54: {},
        20: {},
        52: {},
        12: {},
        24: {}
    }

    def explotar_bombas(self, nodo):
        print (nodo)
        if nodo in self.grafo:
            bombas_reventadas = 0  # Contador de bombas reventadas
            if len(self.grafo[nodo]) == 1:  # Si el nodo tiene solo un vecino
                vecino = next(iter(self.grafo[nodo].keys()))  # Obtener el único vecino del nodo
                if vecino in self.vertices:
                    random_bg_color = self.random_color()
                    # Crear etiqueta con la imagen de la bomba y colocarla en la posición del cuadro vecino
                    label_bomba = tk.Label(self.frame, image=self.bomba_png, borderwidth=0, highlightthickness=0, bg=random_bg_color)
                    label_bomba.place(x=self.grid[vecino - 1].winfo_x(), y=self.grid[vecino - 1].winfo_y())
                    self.grid[vecino - 1].config(bg=random_bg_color)
                    # Reproducir sonido de explosión
                    self.musica_sin_bomba = pygame.mixer.music.load('Bombas.wav')
                    pygame.mixer.music.play(1)
                    # Incrementar el contador de bombas reventadas
                    bombas_reventadas += 1
                # Eliminar el vértice vecino del grafo para evitar la propagación de explosiones
                del self.grafo[vecino]
            else:  # Si el nodo tiene más de un vecino
                for vecino, peso in self.grafo[nodo].items():
                    if vecino in self.vertices:
                        random_bg_color = self.random_color()
                        # Crear etiqueta con la imagen de la bomba y colocarla en la posición del cuadro vecino
                        label_bomba = tk.Label(self.frame, image=self.bomba_png, borderwidth=0, highlightthickness=0, bg=random_bg_color)
                        label_bomba.place(x=self.grid[vecino - 1].winfo_x(), y=self.grid[vecino - 1].winfo_y())
                        self.grid[vecino - 1].config(bg=random_bg_color)
                        # Reproducir sonido de explosión
                        self.musica_sin_bomba = pygame.mixer.music.load('Bombas.wav')
                        pygame.mixer.music.play(1)
                        # Incrementar el contador de bombas reventadas
                        bombas_reventadas += 1
                
            # Actualizar el contador de bombas por encontrar restando el número de bombas reventadas
            self.bombas_por_encontrar -= bombas_reventadas
            self.bombas_label.config(text=f"Bombas por encontrar: {self.bombas_por_encontrar}")
            
            # Eliminar el vértice actual del grafo para evitar la propagación de explosiones
            del self.grafo[nodo]
        else:
            pass



if __name__ == "__main__":
    app = App()
    app.mainloop()
