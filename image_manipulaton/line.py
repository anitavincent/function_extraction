import math
import cv2


class Line:

    def __init__(self, line):
        self.set_values(line)
        self._reorder()

    def set_values(self, line_values):
        for x1, y1, x2, y2 in line_values:
            self.x1 = x1
            self.y1 = y1
            self.x2 = x2
            self.y2 = y2

    # reorder so lowest values are always first
    def _reorder(self):
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
            if other_line.y1 >= (self.y1 - thr) and \
                    other_line.y1 <= (self.y1 + thr):
                return True
            elif other_line.y2 >= (self.y1 - thr) and \
                    other_line.y2 <= (self.y1 + thr):
                return True
            else:
                return False
        elif self.get_direction() == "vert":
            if other_line.x1 >= (self.x1 - thr) and \
                    other_line.x1 <= (self.x1 + thr):
                return True
            elif other_line.x2 >= (self.x1 - thr) and \
                    other_line.x2 <= (self.x1 + thr):
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

    # extrapolate line so it reaches border
    def extrapolate(self, image):
        height, width = image.shape[:2]
        slope = self.get_slope()

        if slope is None:
            self.set_values([[self.x1, 0, self.x2, height - 1]])
        elif slope == 0.0:
            self.set_values([[0, self.y1, width - 1, self.y2]])
        else:
            x1b = self.get_point(y=0, x=None)
            x2b = self.get_point(y=height-1, x=None)
            self.set_values([[int(x1b), 0, int(x2b), height - 1]])

    # get point on line based on one
    # of the axis
    def get_point(self, x, y):
        slope = self.get_slope()
        if slope is None:
            return (self.x1, y)
        if slope == 0.0:
            return (x, self.y1)

        m = slope
        b = self.y1 - m * self.x1
        if x is None:
            x = (y - b) / m
        if y is None:
            y = x * m + b

        return (x, y)

    # gets pixel by moving on the line
    # from starting point to starting point + distance
    def get_pixel_on_line(self, starting_point, distance):
        xi, yi = starting_point

        if self.get_direction() == "vert":
            x, y = self.get_point(x=None, y=(yi+distance))
            return (int(x), y)
        elif self.get_direction() == "hori":
            x, y = self.get_point(x=(xi+distance), y=None)
            return (x, int(y))

    def find_intersection(self, line):
        x1, y1, x2, y2 = [self.x1, self.y1, self.x2, self.y2]
        x3, y3, x4, y4 = [line.x1, line.y1, line.x2, line.y2]

        x1, y1, x2, y2 = [long(x1), long(y1), long(x2), long(y2)]
        x3, y3, x4, y4 = [long(x3), long(y3), long(x4), long(y4) ]

        # determinant
        px = ((x1 * y2 - y1 * x2) * (x3 - x4) -
              (x1 - x2) * (x3 * y4 - y3 * x4)) /  \
            ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        py = ((x1 * y2 - y1 * x2) * (y3 - y4) -
              (y1 - y2) * (x3 * y4 - y3 * x4)) /  \
            ((x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4))
        return px, py
