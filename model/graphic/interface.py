import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *
import sys

import model.canvas.canvas as canvas
import util.graphic.utilities as util
import lib.haralick as haralick
from PIL import Image
import cv2.cv2 as cv2

class InterfaceGrafica:
    def __init__(self, master=None):
        self.fontePadrao = ("Arial", "12")
        self.fonteTitulos = ("Arial", "12", "bold")
        
        self.imagesByPath = None
        self.filename = None

        self.cls_svm = None
        self.train_features = None
        self.train_labels = None
        self.selected_caracteristics = []

        self.containerGeral = Frame(master)
        self.containerGeral.bind('<Right>', self.ProximaImagem)
        self.containerGeral.bind('<Left>', self.AnteriorImagem)
        self.containerGeral.bind('x', self.CalcularCaracteristicas)
        self.containerGeral.focus_set()
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

        self.containerTituloMatriz = Frame(self.containerMenu, bg='#cbccc6', pady=3)
        self.containerTituloMatriz.pack(fill=X, anchor='nw')

        self.containerTempoTreino = Frame(self.containerMenu, bg='#cbccc6', pady=20)
        self.containerTempoTreino.pack(fill=X, anchor='nw', side=BOTTOM)

        self.containerPorcentagemAcerto = Frame(self.containerMenu, bg='#cbccc6', pady=3)
        self.containerPorcentagemAcerto.pack(fill=X, anchor='nw', side=BOTTOM)

        self.containerEspecificidade = Frame(self.containerMenu, bg='#cbccc6', pady=3)
        self.containerEspecificidade.pack(fill=X, anchor='nw', side=BOTTOM)

        self.containerHomogeinidade = Frame(self.containerMenu, bg='#cbccc6', pady=3)
        self.containerHomogeinidade.pack(fill=X, anchor='nw', side=BOTTOM)

        self.containerTempoTeste = Frame(self.containerMenu, bg='#cbccc6', pady=1)
        self.containerTempoTeste.pack(fill=X, anchor='nw', side=BOTTOM)

        self.containerTempoClassificacao = Frame(self.containerMenu, bg='#cbccc6', pady=20)
        self.containerTempoClassificacao.pack(fill=X, anchor='nw', side=BOTTOM)

        self.containerMatriz = Frame(self.containerMenu, bg='#cbccc6', pady=5, padx=100)
        self.containerMatriz.pack(fill=X, anchor='nw', side=TOP)
        
        self.containerBotaoDICOM = Frame(self.containerMenu, bg='#cbccc6')
        self.containerBotaoDICOM.pack(fill=X, anchor='se', side=BOTTOM)
        
        self.botaoAbrirDiretorio = Button(self.containerBotoes, text="Abrir Diretório", bd=2, font=self.fonteTitulos, command=self.SelecionarDiretorio)
        self.botaoAbrirDiretorio.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoCorDefault = self.botaoAbrirDiretorio['bg']
        
        self.botaoSelecionarCaracteristicas = Menubutton(self.containerBotoes2, text="Selecionar Caracteristicas", bd=2, font=self.fonteTitulos, relief=RAISED)
        self.botaoSelecionarCaracteristicas.grid()
        self.botaoSelecionarCaracteristicas.menu = Menu(self.botaoSelecionarCaracteristicas, tearoff=0)
        self.botaoSelecionarCaracteristicas['menu'] = self.botaoSelecionarCaracteristicas.menu

        self.optEnergy = IntVar(value=1) #0
        self.optContrast = IntVar(value=1) #1
        self.optCorrelation = IntVar(value=0) #2
        self.optVariance = IntVar(value=1) #3
        self.optInverseDifferenceMoment = IntVar(value=0) #4
        self.optSumAverage = IntVar(value=0) #5
        self.optSumVariance = IntVar(value=0) #6
        self.optSumEntropy = IntVar(value=0) #7
        self.optEntropy = IntVar(value=1) #8
        self.optDifferenceVariance = IntVar(value=0) #9
        self.optDifferenceEntropy = IntVar(value=0) #10
        self.optIMC1 = IntVar(value=0) #11
        self.optIMC2 = IntVar(value=0) #12
        
        self.caracteristics_names_map = {
            '0': 'Energia',
            '1': 'Contraste',
            '2': 'Correlação',
            '3': 'Homogeinidade',
            '4': 'Inverso da diferença do momento',
            '5': 'Average da soma',
            '6': 'Soma da homogeinidade',
            '7': 'Soma da entropia',
            '8': 'Entropia',
            '9': 'Diferença da homogeinidade',
            '10': 'Diferença da entropia',
            '11': 'Measure da informação de correlação 1',
            '12': 'Measure da informação de correlação 2'
        }

        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Energia", variable=self.optEnergy)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Contraste", variable=self.optContrast)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Correlação", variable=self.optCorrelation)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Homogeinidade", variable=self.optVariance)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Inverso da diferença do momento", variable=self.optInverseDifferenceMoment)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Average da soma", variable=self.optSumAverage)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Soma da homogeinidade", variable=self.optSumVariance)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Soma da entropia", variable=self.optSumEntropy)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Entropia", variable=self.optEntropy)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Diferença da homogeinidade", variable=self.optDifferenceVariance)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Diferença da entropia", variable=self.optDifferenceEntropy)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Measure da informação de correlação 1", variable=self.optIMC1)
        self.botaoSelecionarCaracteristicas.menu.add_checkbutton(label="Measure da informação de correlação 2", variable=self.optIMC2)

        self.botaoSelecionarCaracteristicas.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoSelecionarRegiaoBool = False
        self.botaoSelecionarRegiao = Button(self.containerBotoes2, text="Selecionar região", bd=2, font=self.fonteTitulos, command=self.SelecionarRegiao)
        self.botaoSelecionarRegiao.pack(side=LEFT, fill=X, expand=YES)
        
        self.botaoCalcularCaracteristicas = Button(self.containerBotoes3, text="Calcular Caracteristicas", bd=2, font=self.fonteTitulos, command=self.CalcularCaracteristicas)
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

        self.label_titulo_matriz = Label(self.containerTituloMatriz, text="Matriz de Confusão:", font=self.fontePadrao)
        self.label_titulo_matriz.pack(side=LEFT, fill=X, expand=YES)

        self.label_tempo_treino = Label(self.containerTempoTreino, text="Tempo de treinamento: ", font=self.fontePadrao)
        self.label_tempo_treino.pack(side=LEFT, fill=X, expand=YES)

        self.label_porcentagem_acerto = Label(self.containerPorcentagemAcerto, text="Porcentagem acertos: ", font=self.fontePadrao)
        self.label_porcentagem_acerto.pack(side=LEFT, fill=X, expand=YES)

        self.label_especificidade = Label(self.containerEspecificidade, text="Especificidade: ", font=self.fontePadrao)
        self.label_especificidade.pack(side=LEFT, fill=X, expand=YES)

        self.label_homogeinidade = Label(self.containerHomogeinidade, text="Homogeinidade testes: ", font=self.fontePadrao)
        self.label_homogeinidade.pack(side=LEFT, fill=X, expand=YES)

        self.label_tempo_teste = Label(self.containerTempoTeste, text="Tempo de teste: ", font=self.fontePadrao)
        self.label_tempo_teste.pack(side=LEFT, fill=X, expand=YES)

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
    
    def SelecionarRegiao(self):
        self.botaoSelecionarRegiaoBool = not self.botaoSelecionarRegiaoBool
        # criar uma vez o retangulo
        if not self.desenhar.rectangleExist:
            util.selectRegion(self.canvasElement, self.desenhar)        
        self.desenhar.setIsRectangle(self.botaoSelecionarRegiaoBool)       
        # Controle de cor do botao
        self.botaoSelecionarRegiao['bg'] = ('#99ff99' if self.botaoSelecionarRegiaoBool else self.botaoCorDefault)

    def updateSelectedFeatures(self):
        self.selected_caracteristics.clear()
        if self.optEnergy.get() == 1:
            self.selected_caracteristics.append(0)
        if self.optContrast.get() == 1:
            self.selected_caracteristics.append(1)
        if self.optCorrelation.get() == 1:
            self.selected_caracteristics.append(2)
        if self.optVariance.get() == 1:
            self.selected_caracteristics.append(3)
        if self.optInverseDifferenceMoment.get() == 1:
            self.selected_caracteristics.append(4)
        if self.optSumAverage.get() == 1:
            self.selected_caracteristics.append(5)
        if self.optSumVariance.get() == 1:
            self.selected_caracteristics.append(6)
        if self.optSumEntropy.get() == 1:
            self.selected_caracteristics.append(7)
        if self.optEntropy.get() == 1:
            self.selected_caracteristics.append(8)
        if self.optDifferenceVariance.get() == 1:
            self.selected_caracteristics.append(9)
        if self.optDifferenceEntropy.get() == 1:
            self.selected_caracteristics.append(10)
        if self.optIMC1.get() == 1:
            self.selected_caracteristics.append(11)
        if self.optIMC2.get() == 1:
            self.selected_caracteristics.append(12)

    def CalcularCaracteristicas(self, event):
        imagem = self.desenhar.image.crop(self.canvasElement.bbox(self.desenhar.rectangle))
        imagem.save("imageToClassify.png")

        imagem = cv2.imread("imageToClassify.png")
        gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

        self.updateSelectedFeatures()

        features = haralick.extract_features(imagem, self.selected_caracteristics)

        text_caracteristics = ''
        count = 0
        for indice_caracteristica in self.selected_caracteristics:
            text_caracteristics += self.caracteristics_names_map[str(indice_caracteristica)] + ': ' + str(round(features[count], 8)) + '\n'
            count += 1

        moments = cv2.moments(gray)
        hu = cv2.HuMoments(moments).flatten()
        
        text_caracteristics += 'Momentos Hu: \n'

        for x in range(0, 7, 1):
            text_caracteristics += str(x+1) + ': ' + str(hu[x]) + '\n'

        tkinter.messagebox.showinfo('Características', text_caracteristics)

    def TreinarClassificador(self):
        self.updateSelectedFeatures()

        self.cls_svm, tempo, porcentagem_acerto, tempo_teste, matrix, especificidade, homogeneidade = haralick.train(self.imagesByPath, self.selected_caracteristics)

        self.label_tempo_treino['text'] = 'Tempo de treinamento: ' + str(tempo) + ' s'
        self.label_porcentagem_acerto['text'] = 'Porcentagem acertos: ' + str(porcentagem_acerto) + '%'
        self.label_especificidade['text'] = 'Especificidade: ' + str(especificidade)
        self.label_tempo_teste['text'] = 'Tempo de teste: ' + str(tempo_teste) + ' s'
        self.label_homogeinidade['text'] = 'Homogeinidade testes: ' + str(homogeneidade)

        for i in range(4):
            for j in range(4):
                b = Entry(self.containerMatriz, width=5)
                b.grid(row=i, column=j)
                b.insert(0, matrix[i][j])

    def Classificar(self):
        imagem = self.desenhar.image.crop(self.canvasElement.bbox(self.desenhar.rectangle))
        imagem.save("imageToClassify.png")

        self.updateSelectedFeatures()

        predict, tempo = haralick.classify("imageToClassify.png", self.cls_svm, False, self.selected_caracteristics)

        self.label_tempo_classificacao['text'] = 'Tempo de classificação: ' + str(tempo) + ' s'

        print("Classificou a imagem como BIRADS " + str(predict))
    
    def OpenImage(self, file):  
        self.ResetAll()

        util.setImage(file['image'], self.canvasElement, self.desenhar)

        self.filename = file['filename']
        
    def SelecionarDiretorio(self):
        directory = util.getDirectory()
        self.imagesByPath = util.getDirectoryImages(directory)
        
        self.OpenImage(self.imagesByPath[0])

    def ProximaImagem(self, event):
        for index, file in enumerate(self.imagesByPath):
            if file['filename'] == self.filename:
                if index < len(self.imagesByPath)-1:
                    return self.OpenImage(self.imagesByPath[index+1])

                break
    
    def AnteriorImagem(self, event):
        for index, file in enumerate(self.imagesByPath):
            if file['filename'] == self.filename:
                if index > 0:
                    return self.OpenImage(self.imagesByPath[index-1])

                break
        