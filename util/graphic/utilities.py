from tkinter import CENTER
from tkinter import filedialog
from PIL import Image, ImageTk

# Fazer uma forma da imagem sempre abrir redimensionada para a dimensão atual da janela?

def setImageWithDialog(canvasObj):
        filename = filedialog.askopenfilename(
            initialdir="/", 
            title="Selecione uma imagem", 
            filetypes=(("PNG files", "*.png"), ("TIFF files", "*.tiff"), ("DICOM files", "*.dcm"))
        )
        
        try:
            img = Image.open(filename)
        except AttributeError:
            print('Nenhuma imagem selecionada ou imagem inválida!')
            return
        
        photo = ImageTk.PhotoImage(img)
        
        canvasObj.create_image(
            canvasObj.winfo_width()/2, 
            canvasObj.winfo_height()/2, 
            image=photo, 
            anchor=CENTER
        )
        
        canvasObj.image = photo
        canvasObj.update()
