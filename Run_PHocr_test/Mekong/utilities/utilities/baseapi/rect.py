import sys

class Rectange:
    def __init__(self, x, y, w, h):
        self.left = self.get_side(x)
        self.bottom = self.get_side(y)
        self.width = self.get_w_h(w)
        self.height = self.get_w_h(h)
        self.right = self.left + self.width
        self.top = self.bottom + self.height
        self.area = self.width*self.height

    def get_side(self, value):
        try:
            return float(value)
        except:
            print "Rectangle: Input is not valid!"
            sys.exit(1)

    def get_w_h(self, value):
        num = self.get_side(value)
        if num < 0:
            print "Rectangle: Input is not valid!"
            sys.exit(1)
        return num

    def get_min(self, a, b):
        if a < b:
            return a
        else:
            return b

    def get_max(self, a, b):
        if a > b:
            return a
        else:
            return b

    def GetOverlapArea(self, rect):
        left = self.get_max(self.left, rect.left)
        right = self.get_min(self.right, rect.right)
        bot = self.get_max(self.bottom, rect.bottom)
        top = self.get_min(self.top, rect.top)
        width = right - left
        if width <= 0:
            return 0
        height = top - bot
        if height <= 0:
            return 0
        return width*height

    def GetOverlapPercent(self, rect):
        return self.GetOverlapArea(rect)/self.area

    def ToString(self):
        return "{0},{1},{2},{3}".format(self.left, self.bottom, self.width, self.height)
