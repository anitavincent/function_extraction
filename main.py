from find_contour import *
from show_pixels import *
from extract_skeleton import *

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

def run_all():
	for img in all_imgs:
		run_one_image(img)

def separate_name(st):
	lst = st.split('/')
	first = "{}/".format(lst[0])
	lst = lst[1].split('.')
	second = lst[0]
	third = ".{}".format(lst[1])
	print first, second, third
	return [first, second, third]

def run_one_image(st):
	group, filename, extension = separate_name(st)

	process_sk(group,filename,extension)
	# find_contour(group,filename,extension)
	# show_pixels(group, filename)

run_all()
# run_one_image("group2/grid2.png")