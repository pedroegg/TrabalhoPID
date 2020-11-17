import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *
import sys

import model.canvas.canvas as canvas
import util.graphic.utilities as util
import lib.haralick as haralick

class InterfaceGrafica:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "12")
        self.fonteTitulos = ("Arial", "12", "bold")
        
        self.directory = ''
        self.imagesByPath = None
        self.filename = None

        self.cls_svm = None
        self.train_features = None
        self.train_labels = None

        self.containerGeral = Frame(master)
        self.containerGeral.pack(fill=BOTH, expand=YES)

        self.containerMenu = Frame(self.containerGeral, bg='#cbccc6', width=100)
        self.containerMenu.pack(side=LEFT, anchor='nw', fill=Y)

        self.containerCanvas = Frame(self.containerGeral, bd=1)
        self.containerCanvas.pack(side=LEFT, anchor='nw', fill=BOTH, expand=YES)

        self.containerBotoes = Frame(self.containerMenu, bg='#cbccc6', pady=3)
        self.containerBotoes.pack(fill=X, anchor='nw')

        self.containerBotoes2 = Frame(self.containerMenu, bg='#cbccc6', pady=3)
        self.containerBotoes2.pack(fill=X, anchor='nw')
        
        self.containerBotoes3 = Frame(self.containerMenu, bg='#cbccc6', pady=3)
        self.containerBotoes3.pack(fill=X, anchor='nw')
        
        self.containerBotoes4 = Frame(self.containerMenu, bg='#cbccc6', pady=3)
        self.containerBotoes4.pack(fill=X, anchor='nw')

        self.containerTempoTreino = Frame(self.containerMenu, bg='#cbccc6', pady=20)
        self.containerTempoTreino.pack(fill=X, anchor='nw', side=BOTTOM)

        self.containerTempoClassificacao = Frame(self.containerMenu, bg='#cbccc6', pady=3)
        self.containerTempoClassificacao.pack(fill=X, anchor='nw', side=BOTTOM)
        
        self.containerBotaoDICOM = Frame(self.containerMenu, bg='#cbccc6')
        self.containerBotaoDICOM.pack(fill=X, anchor='se', side=BOTTOM)
        
        self.botaoAbrirDiretorio = Button(self.containerBotoes, text="Abrir Diretório", bd=2, font=self.fonteTitulos, command=self.SelecionarDiretorio)
        self.botaoAbrirDiretorio.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoCorDefault = self.botaoAbrirDiretorio['bg']
        
        self.botaoSelecionarCaracteristicas = Button(self.containerBotoes2, text="Selecionar Caracteristicas", bd=2, font=self.fonteTitulos)
        self.botaoSelecionarCaracteristicas.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoSelecionarRegiaoBool = False
        self.botaoSelecionarRegiao = Button(self.containerBotoes2, text="Selecionar região", bd=2, font=self.fonteTitulos, command=self.SelecionarRegiao)
        self.botaoSelecionarRegiao.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoCalcularCaracteristicas = Button(self.containerBotoes3, text="Calcular Caracteristicas", bd=2, font=self.fonteTitulos)
        self.botaoCalcularCaracteristicas.pack(side=LEFT)
        
        self.botaoClassificar = Button(self.containerBotoes3, text="Classificar", bd=2, font=self.fonteTitulos, command=self.Classificar)
        self.botaoClassificar.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoTreinarClassificador = Button(self.containerBotoes4, text="Treinar Classificador", bd=2, font=self.fonteTitulos, command=self.TreinarClassificador)
        self.botaoTreinarClassificador.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoDICOM = Button(self.containerBotaoDICOM, text="Melhorar Qualidade DICOM", bd=2, font=self.fonteTitulos)

        self.verticalBar = Scrollbar(self.containerCanvas, orient='vertical')
        self.verticalBar.pack(side=RIGHT)
        
        self.horizontalBar = Scrollbar(self.containerCanvas, orient='horizontal')
        self.horizontalBar.pack(side=BOTTOM)
        
        self.canvasElement = Canvas(self.containerCanvas, highlightthickness=0, xscrollcommand=self.horizontalBar.set, yscrollcommand=self.verticalBar.set)
        self.canvasElement.pack(anchor='nw', fill=BOTH, expand=YES)
        
        self.botaoAbrirImagem = Button(self.containerBotoes, text="Abrir imagem", bd=2, font=self.fonteTitulos, command=self.OpenImage)
        self.botaoAbrirImagem.pack(side=LEFT, fill=X, expand=YES)

        self.label_tempo_treino = Label(self.containerTempoTreino, text="Tempo de treinamento: ", font=self.fontePadrao)
        self.label_tempo_treino.pack(side=LEFT, fill=X, expand=YES)

        self.label_tempo_classificacao = Label(self.containerTempoClassificacao, text="Tempo de classificação: ", font=self.fontePadrao, pady=3)
        self.label_tempo_classificacao.pack(side=LEFT, fill=X, expand=YES)
        
        self.SetDesenhar()
        
        self.verticalBar.configure(command=self.desenhar.scroll_y)
        self.horizontalBar.configure(command=self.desenhar.scroll_x)
        
        self.SetCanvasBinds()
        
    def SetDesenhar(self):
        self.desenhar = None
        self.desenhar = canvas.DesenhosCanvas(self.canvasElement)
        self.desenhar.setImscale(1.0)
        self.desenhar.setDelta(1.3)
    
    def SetCanvasBinds(self):
        self.canvasElement.bind('<Configure>', self.desenhar.show_image)
        self.canvasElement.bind('<ButtonPress-1>', self.desenhar.move_start)
        self.canvasElement.bind("<ButtonRelease-1>", self.desenhar.move_stop)
        self.canvasElement.bind('<B1-Motion>', self.desenhar.move_to)
        
        if sys.platform == 'linux':
            self.canvasElement.bind('<Button-5>', self.desenhar.wheel)  # only with Linux, wheel scroll down
            self.canvasElement.bind('<Button-4>', self.desenhar.wheel)  # only with Linux, wheel scroll up
        else:
            self.canvasElement.bind('<MouseWheel>', self.desenhar.wheel)  # with Windows and MacOS, but not Linux
    
    def ResetAll(self):
        self.canvasElement.delete("all")
        self.canvasElement.destroy()
        self.canvasElement = Canvas(self.containerCanvas, highlightthickness=0, xscrollcommand=self.horizontalBar.set, yscrollcommand=self.verticalBar.set)
        self.canvasElement.pack(anchor='nw', fill=BOTH, expand=YES)
        
        self.SetDesenhar()
        self.SetCanvasBinds()
    
    def OpenImage(self):  
        self.ResetAll()
        
        self.filename = util.setImageWithDialog(self.canvasElement, self.desenhar)
        
        if self.filename.lower().split('.')[1] == 'dcm':
            self.botaoDICOM.pack(side=RIGHT)
        else:
            self.botaoDICOM.pack_forget()
    
    def SelecionarDiretorio(self):
        self.directory = util.getDirectory()
        self.imagesByPath = util.getDirectoryImages(self.directory)
    
    def SelecionarRegiao(self):
        self.botaoSelecionarRegiaoBool = not self.botaoSelecionarRegiaoBool
        # criar uma vez o retangulo
        if not self.desenhar.rectangleExist:
            util.selectRegion(self.canvasElement, self.desenhar)        
        self.desenhar.setIsRectangle(self.botaoSelecionarRegiaoBool)       
        # Controle de cor do botao
        self.botaoSelecionarRegiao['bg'] = ('#99ff99' if self.botaoSelecionarRegiaoBool else self.botaoCorDefault)
    
    def TreinarClassificador(self):
        self.cls_svm, tempo = haralick.train(self.directory)

        self.label_tempo_treino['text'] = 'Tempo de treinamento: ' + str(tempo) + ' s'

    def Classificar(self):
        predict, tempo = haralick.classify(self.filename, self.cls_svm)

        self.label_tempo_classificacao['text'] = 'Tempo de classificação: ' + str(tempo) + ' s'

        print("Classificou a imagem como BIRADS " + str(predict))
