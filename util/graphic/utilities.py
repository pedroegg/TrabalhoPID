# pip install pydicom
# pip install pypng

from tkinter import filedialog
from PIL import Image
import os
import pydicom
import numpy as np
import png
import cv2.cv2 as cv2

def openDicom(filepath, useVoiLut):
    ds = pydicom.dcmread(filepath)
    shape = ds.pixel_array.shape
    
    if 'WindowWidth' in ds:
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

	files = []
	for filename in os.listdir(directory):
		print("Carregando arquivo: {}".format(filename))

		imageDirectory = directory + "/" + filename

		try:
			structure = {
				"filename": filename,
				"image": Image.open(imageDirectory),
			}

			files.append(structure)

		except:
			print('Nenhuma imagem selecionada ou imagem inválida!')

	return files

def setImage(imagem, canvasObj, desenhosObj):
	try:
		desenhosObj.setImage(imagem)

	except AttributeError:
		print('Nenhuma imagem selecionada ou imagem inválida!')
		return

	width, height = imagem.size
	desenhosObj.setWidth(width)
	desenhosObj.setHeight(height)

	container = canvasObj.create_rectangle(0, 0, width, height, width=0)
	desenhosObj.setContainer(container)

	desenhosObj.show_image()

def selectRegion(canvasObj, desenhosObj):
	rectangle = canvasObj.create_rectangle(1, 1, 127, 127, fill=None, outline="green", width=2)
	desenhosObj.setRectangleExist(True)
	desenhosObj.setRectangle(rectangle)