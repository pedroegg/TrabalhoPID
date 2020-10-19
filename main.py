# -*- coding: utf-8 -*-
# Caso dê o erro ImportError: libtk8.6.so: cannot open shared object, instale o tkinter através
# Do comando sudo pacman -S tk

from tkinter import *
import _thread

import model.graphic.interface as gui

def atualizarInterface(a=None):
    while True:
        root.update_idletasks()
        root.update()
        
def iniciarThreadAtualizar():
    _thread.start_new_thread(atualizarInterface, tuple([1]))

root = Tk()
root.title("Trabalho Processamento de Imagens Digitais")
root.geometry("800x480")
interface = gui.InterfaceGrafica(root)
root.after(100, iniciarThreadAtualizar)
root.mainloop()