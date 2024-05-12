from tkinter import *
from tkinter import messagebox
import random
import time

root = Tk()
frame = Frame(root)
frame.pack()
root.title("Buscaminas")
root.resizable(False, False)
frame.config(width=400, height=400, bg="#588a35")  # Cambio de color de fondo del frame

# --------------Variables--------------
win = False
listaBotones = []
banderasDisponibles = 10
tiempoInicio = time.time()
bandera = False

contadorTiempo = Label(frame)
contadorTiempo.grid(column=1, row=0, columnspan=4)

def tiempo():
    global contadorTiempo
    tiempoTranscurrido = int(time.time() - tiempoInicio)
    contadorTiempo.config(text="Tiempo transcurrido: " + str(tiempoTranscurrido), font=("Arial 15"), bg="#588a35", fg="white")  # Cambio de color de fondo y texto del contador
    contadorTiempo.after(200, tiempo)

def generarBotones():
    global listaBotones
    for c in range(64):
        color = "#a3d14a" if c % 2 == 0 else "#aad852"  # Alternar colores entre #a3d14a y #aad852
        listaBotones.append(Button(frame, width=6, height=3, text=" ", font=("Arial 12 bold"), command=lambda c=c: slotPulsado(c), fg="blue", bg=color))  # Cambio de color de fondo de los botones
        listaBotones[c].grid(column=(c % 8) + 1, row=(c // 8) + 1)

generarBotones()

# ---------------Bombas---------------
bombas = random.sample(range(64), 10)
print("Las ubicaciones de las bombas son:", bombas)

numeroPulsaciones = 0
imagenBomba = PhotoImage(file="Image/bomba.png")

def mostrarBombas():
    global imagenBomba
    for bomba in bombas:
        listaBotones[bomba].config(image=imagenBomba, width=32, height=32)

def slotPulsado(slot):
    global listaBotones, win, bandera, banderasDisponibles
    if win:
        return
    
    if slot in bombas:
        if bandera:
            ponerBandera()
        else:
            mostrarBombas()
            time.sleep(2)
            listaBotones[slot].config(image=imagenBomba, width=64, height=65, bg="#f17070")
    else:
        mostrarNumeros(slot)
        if bandera:
            ponerBandera()

def mostrarNumeros(slot):
    global listaBotones
    bombasCerca = sum(1 for i in [-9, -8, -7, -1, 1, 7, 8, 9] if (0 <= slot + i < 64) and ((slot % 8 != 0 or i not in [-9, -1, 7]) and ((slot + 1) % 8 != 0 or i not in [-7, 1])) and slot + i in bombas)
    if bombasCerca:
        listaBotones[slot].config(text=bombasCerca, fg="#2174ce", font=("Arial 12 bold"))
    else:
        listaBotones[slot].config(bg="#588a35", state="disabled")  # Cambio de color de fondo de los botones
        for i in [-9, -8, -7, -1, 1, 7, 8, 9]:
            if 0 <= slot + i < 64 and listaBotones[slot + i].cget("state") == "normal":
                mostrarNumeros(slot + i)

def checkWin():
    global listaBotones, win
    for i in range(64):
        if i not in bombas and listaBotones[i].cget("state") == "normal":
            return
    win = True
    txtWin1 = Label(frame, width=25, height=2, text="¡  G  A  N  A  S  T  E  !", font=("helvetica 27 bold"), bg="#fe4a4a")
    txtWin1.grid(row=10, column=1, columnspan=9)
    frame.config(bg="#fe4a4a")
    contadorTiempo.config(bg="#fe4a4a")
    mostrarBombas()

# -------------Banderas----------
def presionarBandera():
    global bandera
    bandera = True

banderaImg = PhotoImage(file="Image/bandera.png")
banderaImgSlot = PhotoImage(file="Image/banderaSlot.png")

def ponerBandera():
    global bandera, banderasDisponibles
    if bandera and banderasDisponibles > 0:
        banderasDisponibles -= 1
        contadorBanderas.config(text="Banderas disponibles: " + str(banderasDisponibles))
    bandera = False

contadorBanderas = Label(frame, text="Banderas disponibles: " + str(banderasDisponibles), font=("Arial 15"), bg="#588a35", fg="white")  # Cambio de color de fondo y texto
contadorBanderas.grid(column=6, row=0, columnspan=5)

botonBandera = Button(frame, text=" ", image=banderaImg, command=presionarBandera)
botonBandera.grid(column=5, row=0)

tiempo()
root.mainloop()
