# pip install pydicom
# pip install pypng

from tkinter import filedialog
from PIL import Image
import os
import pydicom
import numpy as np
import png

def openDicom(filepath, useVoiLut):
    ds = pydicom.dcmread(filepath)
    shape = ds.pixel_array.shape
    
    if useVoiLut:
        windowed = pydicom.pixel_data_handlers.util.apply_voi_lut(ds.pixel_array, ds)
    else:
        windowed = ds.pixel_array.astype(float)
    
    image_2d_scaled = (np.maximum(windowed,0) / windowed.max()) * 255.0
    image_2d_scaled = np.uint8(image_2d_scaled)
    filename = "a.png"
    with open(filename, 'wb') as png_file:
        w = png.Writer(shape[1], shape[0], greyscale=True)
        w.write(png_file, image_2d_scaled)
    
    return filename

def getDirectory():
    directory = filedialog.askdirectory(
        initialdir="/", 
        title="Selecione um diretório"
    )
    
    return directory

def getDirectoryImages(directory):
    if directory == () or directory is None or directory == "":
        print('Nenhum diretório selecionado ou diretório inválido!')
        return
    
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
            

def setImageWithDialog(canvasObj, desenhosObj):
    filename = filedialog.askopenfilename(
        initialdir="/", 
        title="Selecione uma imagem", 
        filetypes=(("PNG files", "*.png"), ("TIFF files", "*.tiff"), ("DICOM files", "*.dcm"), ("DICOM files", "*.DCM")),
    )
    
    try:
        if ".dcm" in str(filename) or ".DCM" in str(filename):
            img = Image.open(openDicom(filename, True))
        else:
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
    
    return filename

def selectRegion(canvasObj, desenhosObj):
    rectangle = canvasObj.create_rectangle(0, 0, 128, 128, fill=None, outline="green", width=2)
    desenhosObj.setRectangleExist(True)
    desenhosObj.setRectangle(rectangle)