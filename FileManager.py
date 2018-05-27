import cv2


class FileManager:

    results_folder = "./pictures/results/"
    originals_folder = "./pictures/originals/"

    all_imgs = ["group1/graph_simple.jpeg",
                "group1/graph_drawing.jpeg",
                "group1/graph_color.jpeg",
                "group1/graph_print.png",
                "group1/fun1.png",
                "group1/fun2.png",
                "group1/fun3.png",
                "group1/fun4.jpg",
                "group1/fun5.png",
                "group1/fun6.jpg",
                "group2/dotted1.jpeg",
                "group2/dotted2.jpeg",
                "group2/grid1.png",
                "group2/grid2.png",
                "group2/grid3.png",
                "group2/grid4.jpg",
                "group3/grid1.png",
                "group3/grid2.png",
                "group3/grid3.png",
                "group3/grid4.png",
                "group3/grid5.png"
                ]

    def __init__(self):
        pass

    def get_image_list(self):
        return self.all_imgs

    # def get_image(self):
    #     pass
    def _separate_name(self, path):
        lst = path.split('/')
        first = "{}/".format(lst[0])
        lst = lst[1].split('.')
        second = lst[0]
        third = ".{}".format(lst[1])
        print first, second, third
        return [first, second, third]

    def save_image(self, image, original_path, aditional_name):
        group, name, ext = self._separate_name(original_path)
        base = "{}{}{}".format(self.results_folder, group, name)
        cv2.imwrite("{}{}{}".format(base, aditional_name, ext), image)

    def get_image(self, path):
        print "{}{}".format(self.originals_folder, path)
        img = cv2.imread("{}{}".format(self.originals_folder, path))
        return img
