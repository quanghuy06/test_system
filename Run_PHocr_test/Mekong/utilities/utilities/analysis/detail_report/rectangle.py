class Rectange:
    def __init__(self, x, y, w, h):
        self.x = int(x)
        self.y = int(y)
        self.w = int(w)
        self.h = int(h)
        self.area = self.w * self.h

    def copy(self, rect):
        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h
        self.area = self.w * self.h

    def is_overlap_with(self, rect):
        if self.is_same_with(rect):
            return True
        left_rect = get_left_rect(self, rect)
        under_rect = get_under_rect(self, rect)
        if (abs(self.x - rect.x) < left_rect.w) and (abs(self.y - rect.y) < under_rect.h):
            return True
        else:
            return False

    def is_same_with(self, rect):
        if (self.x == rect.x) and (self.y == rect.y) and (self.w == rect.w) and (self.h == rect.h):
            return True
        else:
            return False

    def get_overlap_area_with(self, rect):
        if self.is_same_with(rect):
            return self.area
        if self.is_overlap_with(rect):
            width = abs(self.x - rect.x)
            height = abs(self.y - rect.y)
            return width*height
        else:
            return 0

    def get_percent_overlap_width(self, rect):
        overlap_area = self.get_overlap_area_with(rect)
        bigger_area = get_max_value(self.area, rect.area)
        return overlap_area/bigger_area

def get_left_rect(rect1, rect2):
    result = Rectange(0, 0, 0, 0)
    if rect1.x < rect2.x:
        result.copy(rect1)
    if rect1.x == rect2.x:
        if rect1.w < rect2.w:
            result.copy(rect1)
        else:
            result.copy(rect2)
    if rect1.x > rect2.x:
        result.copy(rect2)
    return result

def get_right_rect(rect1, rect2):
    result = Rectange(0, 0, 0, 0)
    if rect1.x < rect2.x:
        result.copy(rect2)
    if rect1.x == rect2.x:
        if rect1.w < rect2.w:
            result.copy(rect2)
        else:
            result.copy(rect1)
    if rect1.x > rect2.x:
        result.copy(rect1)
    return result

def get_under_rect(rect1, rect2):
    result = Rectange(0, 0, 0, 0)
    if rect1.y < rect2.y:
        result.copy(rect1)
    if rect1.y == rect2.y:
        if rect1.h < rect2.h:
            result.copy(rect1)
        else:
            result.copy(rect2)
    if rect1.y < rect2.y:
        result.copy(rect2)
    return result

def get_upper_rect(rect1, rect2):
    result = Rectange(0, 0, 0, 0)
    if rect1.y < rect2.y:
        result.copy(rect2)
    if rect1.y == rect2.y:
        if rect1.h < rect2.h:
            result.copy(rect2)
        else:
            result.copy(rect1)
    if rect1.y < rect2.y:
        result.copy(rect1)
    return result

def get_min_value(value1, value2):
    if value1 < value2:
        return value1
    else:
        return value2

def get_max_value(value1, value2):
    if value1 > value2:
        return value1
    else:
        return value2
