class Snake():

    def __init__(self, x, y, w, h):
        self.x, self.y = x, y
        self.w, self.h = w, h
        print('yo')


    def move(self, x_change, y_change):
        self.x += x_change
        self.y += y_change

    #def show(self):

