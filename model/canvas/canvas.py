from PIL import Image, ImageTk

class DesenhosCanvas:

    def __init__(self, canvas):
        self.canvas = canvas
        self.container = None
        self.width = 0
        self.height = 0
        self.imscale = 0
        self.delta = 0
        self.image = None
        self.rectangle = None
        self.isRectangle = False
        self.rectangleExist = False
        self._drag_data = {"x": 0, "y": 0}
        
    def setWidth(self, width):
        self.width = width
    
    def setHeight(self, height):
        self.height = height
    
    def setImscale(self, imscale):
        self.imscale = imscale
    
    def setDelta(self, delta):
        self.delta = delta
        
    def setImage(self, image):
        self.image = image
        
    def setContainer(self, container):
        self.container = container
    
    def setRectangle(self, rectangle):
        self.rectangle = rectangle
        
    def setIsRectangle(self, isRectangle):
        self.isRectangle = isRectangle
    
    def setRectangleExist(self, rectangleExist):
        self.rectangleExist = rectangleExist
        
    def scroll_y(self, *args, **kwargs):
        ''' Scroll canvas vertically and redraw the image '''
        self.canvas.yview(*args, **kwargs)  # scroll vertically
        self.show_image()  # redraw the image

    def scroll_x(self, *args, **kwargs):
        ''' Scroll canvas horizontally and redraw the image '''
        self.canvas.xview(*args, **kwargs)  # scroll horizontally
        self.show_image()  # redraw the image

    def move_start(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        
    def move_stop(self, event):
        """End drag of an object"""
        self._drag_data["x"] = 0
        self._drag_data["y"] = 0

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        if self.isRectangle:
            delta_x = event.x - self._drag_data["x"]
            delta_y = event.y - self._drag_data["y"]
            
            self.canvas.move(self.rectangle, delta_x, delta_y)

            self._drag_data["x"] = event.x
            self._drag_data["y"] = event.y
        else:
            self.canvas.scan_dragto(event.x, event.y, gain=1)
            self.show_image()  # redraw the image
            
    def cut_by_box(self):
        # self.setContainer(self.rectangle)
        self.show_image()

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        bbox = self.canvas.bbox(self.container)  # get image area
        
        if (bbox[0] < x < bbox[2]) and (bbox[1] < y < bbox[3]): 
            pass  # Ok! Inside the image
        else: 
            return  # zoom only inside image area
        
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        
        if event.num == 5 or event.delta == -120:  # scroll down
            i = min(self.width, self.height)
            if int(i * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.delta
            scale        /= self.delta
            
        if event.num == 4 or event.delta == 120:  # scroll up
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height())
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.delta
            scale        *= self.delta
            
        self.canvas.scale('all', x, y, scale, scale)  # rescale all canvas objects
        self.show_image()
        
    def show_image(self, event=None):
        if self.container is None:
            return
        
        ''' Show image on the Canvas '''
        bbox1 = self.canvas.bbox(self.container)  # get image area
        # Remove 1 pixel shift at the sides of the bbox1
        bbox1 = (bbox1[0] + 1, bbox1[1] + 1, bbox1[2] - 1, bbox1[3] - 1)
        
        bbox2 = (self.canvas.canvasx(0),  # get visible area of the canvas
                 self.canvas.canvasy(0),
                 self.canvas.canvasx(self.canvas.winfo_width()),
                 self.canvas.canvasy(self.canvas.winfo_height()))
        
        bbox = [min(bbox1[0], bbox2[0]), min(bbox1[1], bbox2[1]),  # get scroll region box
                max(bbox1[2], bbox2[2]), max(bbox1[3], bbox2[3])]
        
        if (bbox[0] == bbox2[0]) and (bbox[2] == bbox2[2]):  # whole image in the visible area
            bbox[0] = bbox1[0]
            bbox[2] = bbox1[2]
        if (bbox[1] == bbox2[1]) and (bbox[3] == bbox2[3]):  # whole image in the visible area
            bbox[1] = bbox1[1]
            bbox[3] = bbox1[3]
            
        self.canvas.configure(scrollregion=bbox)  # set scroll region
        
        x1 = max(bbox2[0] - bbox1[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(bbox2[1] - bbox1[1], 0)
        x2 = min(bbox2[2], bbox1[2]) - bbox1[0]
        y2 = min(bbox2[3], bbox1[3]) - bbox1[1]
        
        if (int(x2 - x1) > 0) and (int(y2 - y1) > 0):  # show image if it in the visible area
            x = min(int(x2 / self.imscale), self.width)   # sometimes it is larger on 1 pixel...
            y = min(int(y2 / self.imscale), self.height)  # ...and sometimes not
            
            image = self.image.crop((int(x1 / self.imscale), int(y1 / self.imscale), x, y))
            imagetk = ImageTk.PhotoImage(image.resize((int(x2 - x1), int(y2 - y1))))
            imageid = self.canvas.create_image(max(bbox2[0], bbox1[0]), max(bbox2[1], bbox1[1]), anchor='nw', image=imagetk)
            
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection