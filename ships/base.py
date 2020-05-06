class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = None
        self.img = None

    def write(self, window):
        window.blit(self.img, (self.x, self.y))

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()
