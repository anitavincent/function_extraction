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

    # reorder so lowest values are always first
    def reorder(self):
        if self.get_direction() == "hori":
            if self.x1 > self.x2:
                self.set_values([[self.x2, self.y2, self.x1, self.y1]])

        if self.get_direction() == "vert":
            if self.y1 > self.y2:
                self.set_values([[self.x2, self.y2, self.x1, self.y1]])

    # render line over image
    def draw(self, image, color, thickness=1):
        cv2.line(image, (self.x1, self.y1), (self.x2, self.y2),
                 color, thickness)

    def get_slope(self):
        # case vertical
        if self.x1 == self.x2:
            return None
        return float(self.y2 - self.y1) / float(self.x2 - self.x1)

    # interpolate self to other line
    def interpolate(self, line):
        if self.get_direction() == "hori":
            small_x, small_y = self._find_low(line, "x")
            big_x, big_y = self._find_high(line, "x")

        elif self.get_direction() == "vert":
            small_x, small_y = self._find_low(line, "y")
            big_x, big_y = self._find_high(line, "y")

        self.set_values([[small_x, small_y, big_x, big_y]])

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

    # returns a unique hash to represent the line
    def hashify(self):
        return "{}.{}.{}.{}".format(self.x1, self.y1, self.x2, self.y2)

    # jugdes if self is close to other line
    # to be 'close' they must have the same direction
    # and be close on that axis
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

    # auxiliar to interpolate
    def _find_high(self, line, axis):
        if axis == "x":
            if line.x2 > self.x2:
                return line.x2, line.y2
            return self.x2, self.y2
        if axis == "y":
            if line.y2 > self.y2:
                return line.x2, line.y2
            return self.x2, self.y2

    # auxiliar to interpolate
    def _find_low(self, line, axis):
        if axis == "x":
            if line.x1 < self.x1:
                return line.x1, line.y1
            return self.x1, self.y1
        if axis == "y":
            if line.y1 < self.y1:
                return line.x1, line.y1
            return self.x1, self.y1

    # extrapolate line so it reachs border
    def extrapolate(self, image):
        height, width = image.shape[:2]
        slope = self.get_slope()

        if slope is None:
            self.set_values([[self.x1, 0, self.x2, height - 1]])
        elif slope == 0.0:
            self.set_values([[0, self.y1, width - 1, self.y2]])
        else:
            m = slope
            b = self.y1 - m * self.x1
            x1b = (0 - b) / m
            x2b = (height - 1 - b) / m
            self.set_values([[int(x1b), 0, int(x2b), height - 1]])
