from line import Line


class LineList:

    def __init__(self, lines=[]):
        self.lines = {}
        for line in lines:
            line = Line(line)
            self.lines[line.hashify()] = line

    def add_line(self, line):
        self.lines[line.hashify()] = line

    # reset hash
    def reset_hash(self, line, old_hash):
        del self.lines[old_hash]
        self.add_line(line)

    def remove_line(self, line):
        del self.lines[line.hashify()]

    def remove_diagonal_lines(self):
        copy = dict(self.lines)
        for line in copy.values():
            if line.get_direction() == "none":
                self.remove_line(line)

    # returns reduced set
    # for each line, looks for lines that are close
    # and merge them
    def group_lines(self):
        close_lines = dict(self.lines).values()
        while(True):
            # this means that no close lines groups were found
            # on the last for loop execution
            if len(close_lines) == 0:
                break
            for line in self.lines.values():
                close_lines = self.find_close_lines(line)
                if len(close_lines) != 0:
                    self.merge_close_lines(line, close_lines)
                    # break here to recalculate after merging
                    break

    # gets set of lines and a pivot line
    # looks for lines that are close in space to pivot line
    # returns set of lines that are close, including the pivot
    def find_close_lines(self, line):
        close_lines = []

        for line2 in self.lines.values():
            if line.hashify() == line2.hashify():
                continue
            if line.is_close_to(line2):
                close_lines.append(line2)

        return close_lines

    # receives set of close_lines (lines to be merged)
    # updates line dictionary with lines now merged
    def merge_close_lines(self, line, close_lines):
        for line2 in close_lines:
            old_hash = line.hashify()
            line.interpolate(line2)
            self.reset_hash(line, old_hash)

        for line2 in close_lines:
            self.remove_line(line2)

    # extrapolates all lines until they reach the borders
    def extrapolate_lines(self, image):
        for line in self.lines.values():
            old_hash = line.hashify()
            line.extrapolate(image)
            self.reset_hash(line, old_hash)
