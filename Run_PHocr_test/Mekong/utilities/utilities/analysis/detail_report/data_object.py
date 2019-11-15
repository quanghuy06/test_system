from baseapi.rect import Rectange

OVERLAP_THRES = 0.8

class Element:
    def __init__(self, content = "", x = 0, y = 0, w = 0, h = 0):
        self.content = content
        self.replace = ""
        self.bbox = Rectange(x, y, w, h)

    def IsSamePlace(self, other):
        if self.bbox.GetOverlapPercent(other.bbox) >= OVERLAP_THRES:
            return True
        return False
