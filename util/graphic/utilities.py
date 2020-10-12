from tkinter import CENTER
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw
import random
import time

# Fazer uma forma da imagem sempre abrir redimensionada para a dimensão atual da janela?

def setImageWithDialog(canvasObj, desenhosObj):
    filename = filedialog.askopenfilename(
        initialdir="/", 
        title="Selecione uma imagem", 
        filetypes=(("PNG files", "*.png"), ("TIFF files", "*.tiff"), ("DICOM files", "*.dcm"))
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