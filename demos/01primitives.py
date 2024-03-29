# %%
from build123d import *
from ocp_vscode import *
set_defaults(
    reset_camera=False,
    default_opacity=0.7
)

# %%

box = Rotation((45,45,0)) * Box(5,7,9)
cyl = Location((0, 10, 0)) * Cylinder(radius = 4, height = 10)
cyl2 = Location((10, 10, 0)) * \
    Cylinder(radius = 4, height = 10, 
    align=(Align.CENTER, Align.CENTER, Align.MIN))
sph = Location((10, 0, 0)) * Sphere(4)

rect = Location((0, 20, 0)) * Rectangle(5, 8)
rrect = Location((10, 20, 0)) * RectangleRounded(5, 8, 1)
rrect_ex = Location((0,10)) * extrude(rrect, 3)
circle = Location((0, 30)) * Circle(4)
poly = Location((0,40)) * Polygon([(-10,-10), (8,10), (-5, 5)])

show(
    box, cyl, cyl2, sph, rect, rrect, circle, rrect_ex, poly,
    names = ["box", "cyl", "cyl2", "sph", "rect", "rrect", "circle", "rrect_ex", "poly"],
    colors = ["red", "blue", "lightblue", "green", "orange", "cyan", "magenta", "cyan", "teal"]
)