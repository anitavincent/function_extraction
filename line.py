import cv2
import math


class Line:

    def __init__(self, line):
        self.set_values(line)
        self.reorder()

    def set_values(self, line_values):
        for x1, y1, x2, y2 in line_values:
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2

    def reorder(self):
        if self.get_direction() == "hori":
            if self.x1 > self.x2:
                self.set_values([[self.x2, self.y2, self.x1, self.y1]])

        if self.get_direction() == "vert":
            if self.y1 > self.y2:
                self.set_values([[self.x2, self.y2, self.x1, self.y1]])

    def draw(self, image, color, thickness=1):
        cv2.line(image, (self.x1, self.y1), (self.x2, self.y2),
                 color, thickness)

    def get_slope(self):
        # case vertical
        if self.x1 == self.x2:
            return None
        return float(self.y2 - self.y1) / float(self.x2 - self.x1)

    def interpolate(self, line):
        if self.get_direction() == "hori":
            small_x, small_y = self._find_low(line, "x")
            big_x, big_y = self._find_high(line, "x")

        elif self.get_direction() == "vert":
            small_x, small_y = self._find_low(line, "y")
            big_x, big_y = self._find_high(line, "y")

        self.set_values([[small_x, small_y, big_x, big_y]])

    def _find_high(self, line, axis):
        if axis == "x":
            if line.x2 > self.x2:
                return line.x2, line.y2
            return self.x2, self.y2
        if axis == "y":
            if line.y2 > self.y2:
                return line.x2, line.y2
            return self.x2, self.y2

    def _find_low(self, line, axis):
        if axis == "x":
            if line.x1 < self.x1:
                return line.x1, line.y1
            return self.x1, self.y1
        if axis == "y":
            if line.y1 < self.y1:
                return line.x1, line.y1
            return self.x1, self.y1

    def get_direction(self):

        slope = self.get_slope()

        if(slope is not None):
            slope = math.fabs(slope)
            if slope > 7.5:
                return "vert"
            elif slope < 0.15:
                return "hori"
            else:
                return "none"
        else:
            return "vert"

    def hashify(self):
        # returns a unique hash to represent the line
        return "{}.{}.{}.{}".format(self.x1, self.y1, self.x2, self.y2)

    def is_close_to(self, other_line, max_distance=30):
        thr = max_distance

        if self.get_direction() != other_line.get_direction():
            return False

        if self.get_direction() == "hori":
            if other_line.y1 >= (self.y1 - thr) and other_line.y1 <= (self.y1 + thr):
                return True
            elif other_line.y2 >= (self.y1 - thr) and other_line.y2 <= (self.y1 + thr):
                return True
            else:
                return False
        elif self.get_direction() == "vert":
            if other_line.x1 >= (self.x1 - thr) and other_line.x1 <= (self.x1 + thr):
                return True
            elif other_line.x2 >= (self.x1 - thr) and other_line.x2 <= (self.x1 + thr):
                return True
            else:
                return False
