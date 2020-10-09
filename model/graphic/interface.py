import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *
import sys

import model.canvas.canvas as canvas
import util.graphic.utilities as util

class InterfaceGrafica:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "12")
        self.fonteTitulos = ("Arial", "12", "bold")

        self.containerGeral = Frame(master)
        self.containerGeral.pack(fill=BOTH, expand=YES)

        self.containerMenu = Frame(self.containerGeral, bg='#cbccc6', width=100)
        self.containerMenu.pack(side=LEFT, anchor='nw', fill=Y)

        self.containerCanvas = Frame(self.containerGeral, bd=1)
        self.containerCanvas.pack(side=LEFT, anchor='nw', fill=BOTH, expand=YES)

        self.containerBotoes = Frame(self.containerMenu, bg='#cbccc6')
        self.containerBotoes.pack(fill=X, anchor='nw')

        self.containerBotoes2 = Frame(self.containerMenu, bg='#cbccc6')
        self.containerBotoes2.pack(fill=X, anchor='nw')

        self.botaoTranslacao = Button(self.containerBotoes, text="Translação", bd=2, font=self.fonteTitulos)
        self.botaoTranslacao.pack(side=LEFT)
        
        self.botaoRotacao = Button(self.containerBotoes, text="Rotação", bd=2, font=self.fonteTitulos)
        self.botaoRotacao.pack(side=LEFT)
        
        self.botaoEscala = Button(self.containerBotoes, text="Escala", bd=2, font=self.fonteTitulos)
        self.botaoEscala.pack(side=LEFT)
        
        self.botaoReflexao = Button(self.containerBotoes, text="Reflexões", bd=2, font=self.fonteTitulos)
        self.botaoReflexao.pack(side=LEFT, fill=X, expand=YES)
        
        self.verticalBar = Scrollbar(self.containerCanvas, orient='vertical')
        self.verticalBar.pack(side=RIGHT)
        
        self.horizontalBar = Scrollbar(self.containerCanvas, orient='horizontal')
        self.horizontalBar.pack(side=BOTTOM)
        
        self.canvasElement = Canvas(self.containerCanvas, highlightthickness=0, xscrollcommand=self.horizontalBar.set, yscrollcommand=self.verticalBar.set)
        self.canvasElement.pack(anchor='nw', fill=BOTH, expand=YES)
        
        self.botaoAbrirImagem = Button(self.containerBotoes2, text="Abrir imagem", bd=2, font=self.fonteTitulos,
            command=lambda: util.setImageWithDialog(self.canvasElement, self.desenhar)
        )
        self.botaoAbrirImagem.pack(side=LEFT)
        
        self.desenhar = canvas.DesenhosCanvas(self.canvasElement)
        self.desenhar.setImscale(1.0)
        self.desenhar.setDelta(1.3)
        
        self.verticalBar.configure(command=self.desenhar.scroll_y)
        self.horizontalBar.configure(command=self.desenhar.scroll_x)
        
        self.canvasElement.bind('<Configure>', self.desenhar.show_image)
        self.canvasElement.bind('<ButtonPress-1>', self.desenhar.move_from)
        self.canvasElement.bind('<B1-Motion>', self.desenhar.move_to)
        
        if sys.platform == 'linux':
            self.canvasElement.bind('<Button-5>', self.desenhar.wheel)  # only with Linux, wheel scroll down
            self.canvasElement.bind('<Button-4>', self.desenhar.wheel)  # only with Linux, wheel scroll up
        else:
            self.canvasElement.bind('<MouseWheel>', self.desenhar.wheel)  # with Windows and MacOS, but not Linux