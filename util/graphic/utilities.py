from tkinter import CENTER
from tkinter import filedialog
from PIL import Image, ImageTk
import random

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
        
        """photo = ImageTk.PhotoImage(img)
        
        canvasObj.create_image(
            canvasObj.winfo_width()/2, 
            canvasObj.winfo_height()/2, 
            image=photo, 
            anchor=CENTER
        )
        
        canvasObj.image = photo
        canvasObj.update()"""
        
        width, height = img.size
        desenhosObj.setWidth(width)
        desenhosObj.setHeight(height)
        
        container = canvasObj.create_rectangle(0, 0, width, height, width=0)
        desenhosObj.setContainer(container)
        
        desenhosObj.show_image()
