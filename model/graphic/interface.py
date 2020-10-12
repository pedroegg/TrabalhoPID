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

        # botoes
        self.botaoTreinoTeste = Button(self.containerBotoes, text="Treino/Teste", bd=2, font=self.fonteTitulos)
        self.botaoTreinoTeste.pack(side=LEFT)
        
        self.botaoCaracteristicas = Button(self.containerBotoes, text="Caracteristicas", bd=2, font=self.fonteTitulos)
        self.botaoCaracteristicas.pack(side=LEFT)
        
        self.botaoTreinarClassificador = Button(self.containerBotoes, text="Treinar Classificador", bd=2, font=self.fonteTitulos)
        self.botaoTreinarClassificador.pack(side=LEFT)
        
        self.botaoSelecionarRegiao = Button(self.containerBotoes, text="Selecionar região", bd=2, font=self.fonteTitulos)
        self.botaoSelecionarRegiao.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoCalcular = Button(self.containerBotoes, text="Calcular", bd=2, font=self.fonteTitulos)
        self.botaoCalcular.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoClassificar = Button(self.containerBotoes, text="Classificar", bd=2, font=self.fonteTitulos)
        self.botaoClassificar.pack(side=LEFT, fill=X, expand=YES)

        # barras
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