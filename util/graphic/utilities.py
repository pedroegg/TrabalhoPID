from tkinter import CENTER
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import random
import time
import os

# Fazer uma forma da imagem sempre abrir redimensionada para a dimensão atual da janela?

def setDirectory():
    directory = filedialog.askdirectory(
        initialdir="/", 
        title="Selecione um diretório"
    )
    
    return directory

def getDirectoryImages(directory):   
    pastasImagens = {
        "1": [],
        "2": [],
        "3": [],
        "4": []
    }

    for direct in range(1, 5, 1):
        actualDirectory = directory + "/" + str(direct)
        
        print("-"*20)
        print("Diretório atual: {}".format(direct))
        print("-"*20)
        
        for filename in os.listdir(actualDirectory):
            print("Arquivo atual: {}".format(filename))
            
            imageDirectory = directory + "/" + str(direct) + "/" + filename
            
            pastasImagens[str(direct)].append(Image.open(imageDirectory))
            
    return pastasImagens
            

def setImageWithDialog(canvasObj, desenhosObj, directory):
    if directory is None:
        print("Diretório ainda não definido!")
        return
    
    filename = filedialog.askopenfilename(
        initialdir=directory, 
        title="Selecione uma imagem", 
        filetypes=(("PNG files", "*.png"), ("TIFF files", "*.tiff"), ("DICOM files", "*.dcm")),
    )
    
    try:
        img = Image.open(filename)
        desenhosObj.setImage(img)
    except AttributeError:
        print('Nenhuma imagem selecionada ou imagem inválida!')
        return
    
    width, height = img.size
    desenhosObj.setWidth(width)
    desenhosObj.setHeight(height)
    
    container = canvasObj.create_rectangle(0, 0, width, height, width=0)
    desenhosObj.setContainer(container)
    
    desenhosObj.show_image()


def selectRegion(canvasObj, desenhosObj):
    rectangle = canvasObj.create_rectangle(0, 0, 128, 128, fill=None, outline="green", width=2)
    
    desenhosObj.setRectangle(rectangle)