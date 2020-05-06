class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = None
        self.img = None
        self.cool_down = 0

    def write(self, window):
        # Maybe move this? it's the only function in this class that gets called every frame
        if self.cool_down != 0 and self.cool_down < 30:
            self.cool_down += 1
        else:
            self.cool_down = 0

        window.blit(self.img, (self.x, self.y))

    def can_shoot(self):
        if self.cool_down == 0:
            self.cool_down += 1
            return True
        else:
            return False

    def get_width(self):
        return self.img.get_width()

    def get_height(self):
        return self.img.get_height()
