# %%
from build123d import *
from ocp_vscode import *
import copy
from math import *
set_defaults(
    reset_camera=False,
    default_opacity=0.7
)

# %%

box = Box(50,50,50)

roof = Location((0,0,25), (45,0,0)) * Box(50, 1/sqrt(2)*50, 1/sqrt(2)*50)
#roof = extrude(box.faces().sort_by(Axis.Z)[-1], 255, taper=35)
#roof = extrude(
#    Polygon([(-25, 0, 25), (25,0,25), (0,0,50)]),
#    25, both = True)

#face = roof.faces().sort_by(Axis.Z)[-2]
#roof += face.center_location * extrude(Circle(2), 5)

house = box + roof

house_orig = copy.copy(house)
house_orig.label = "original"
house_orig.color = "#ffffff00"

#house = chamfer(house.edges(), 3)
#house = fillet(house.edges(), 3)

#house = fillet(
#    house.edges().sort_by(Axis.Z)[0:4],
#    12
#)

#for face in house.faces():
#    circle = face.center_location * Circle(10)
#    house += extrude(circle, 2)

show(house, house_orig)