from descartes import PolygonPatch
import json
from matplotlib import pyplot as plt
from shapely.geometry import Polygon
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg


WIDTH = 1050
HEIGHT = 758

class File:
    def __init__(self, fn="", data=None):
        self.fn = fn
        self.data = data
        self.photo = None
    
    def ask(self):
        self.fn = askopenfilename()
        #print(self.fn)

        if ".json" in self.fn:
            with open(self.fn) as fn:
                data = json.load(fn)
                #fn.close()

            self.data = data['features'][0]['geometry']
                
            #print("debug: file selected!")
            show(file)
        else:
            pass
            #print("debug: wrong file selected!")



#window functions
def center(root, windowWidth=WIDTH, windowHeight=HEIGHT):
    screenWidth = root.winfo_screenwidth() # width of the screen
    screenHeight = root.winfo_screenheight() # height of the screen

    x = (screenWidth/2) - (windowWidth/2)
    y = (screenHeight/2) - (windowHeight/2)

    root.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))



def draw_figure(canvas, figure, loc=(0, 0)):
    """ Draw a matplotlib figure onto a Tk canvas

    loc: location of top-left corner of figure on canvas in pixels.
    Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
    """
    figure_canvas_agg = FigureCanvasAgg(figure)
    figure_canvas_agg.draw()
    figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
    figure_w, figure_h = int(figure_w), int(figure_h)
    photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)

    # Position: convert from top-left anchor to center anchor
    canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)

    # Unfortunately, there's no accessor for the pointer to the native renderer
    tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)

    # Return a handle which contains a reference to the photo object
    # which must be kept live or else the picture disappears
    return photo



file = File()

root = tk.Tk()
root.title("Coastline Measurer by Andrija Radica 4.b, 2018./2019.")

toolbar = tk.Frame(master=root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

log = tk.Frame(master=root)
log.pack(side=tk.TOP, fill=tk.X)



loadfile = tk.Button(master=toolbar, relief=tk.FLAT, text="Load File", command=file.ask, font="Helvetica 18")
loadfile.pack(side=tk.LEFT)

logcontent = tk.Label(master=log, font="Helvetica 18")
logcontent.pack()


q = tk.Button(master=root, text="Quit", command=root.destroy, font="Helvetica 18")
q.pack(side=tk.BOTTOM, padx=2, pady=2)



canvas = tk.Canvas(master=root, width=WIDTH, height=HEIGHT)
canvas.pack(fill=tk.BOTH)

""""""
fig_x, fig_y = 200, 100
#fig_photo = draw_figure(canvas, fig, loc=(fig_x, fig_y))
""""""

def show(file, canvas=canvas, loc=(fig_x, fig_y)):
    BLUE = '#6699cc'
    poly = file.data #['features'][0]['geometry']
    #print(poly)
    fig = plt.figure() 
    ax = fig.gca() 
    ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2 ))
    ax.axis('scaled')
    file.photo = draw_figure(canvas, fig, loc=loc)

def measure(file=file, logcontent=logcontent):
    poly = file.data
    tp = poly['type']
    #print(tp)
    if tp == "Polygon":
        coordinates = poly['coordinates']
    else:
    #print(poly)
        objs = len(poly['coordinates'])
        coordinates = [poly['coordinates'][i][0] for i in range(objs)]

    total = 0
    for c in coordinates:
        p = Polygon(c)
        total += p.length
    total = round(total, 2) * 100 #TODO: scale!

    logcontent["text"]="{}km".format(total)

m = tk.Button(master=toolbar, relief=tk.FLAT, text="Measure", command = measure, font="Helvetica 18")
m.pack(side=tk.LEFT)


center(root)
root.mainloop()
