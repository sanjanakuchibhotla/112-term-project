class Button():
    def __init__(self, name, center):
        self.name = name
        self.width = 20
        self.height = 10
        self.center = center

    def getName(self):
        return self.name

    def getCenter(self):
        return self.center
    
    def clicked(self,mouseX,mouseY):
        (x,y) = self.center
        x0 = x - self.width/2
        y0 = y - self.height/2
        x1 = x + self.width/2
        y1 = y + self.height/2
        return x0 < mouseX < x1 and y0 < mouseY < y1
    
class Slider():
    def __init__(self, name, center):
        self.name = name
        self.width = 30
        self.height = 2
        self.center = center
    
