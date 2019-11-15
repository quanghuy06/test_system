# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class ObjectInfo:
    def __init__(self, obj_id, x, y, tag):
        self.obj_id = obj_id
        self.x = x
        self.y = y
        self.tag = tag

    def __repr__(self):
        return repr((self.obj_id, self.x, self.y, self.tag))
