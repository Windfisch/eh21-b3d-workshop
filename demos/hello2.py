# %%
from build123d import *
from ocp_vscode import *
# %%
box = Location((10,0,20)) *  Sphere(radius = 10)
box2 = Location((0,0,0), (45, 45, 0)) * Cylinder(radius = 5, height = 10)
show(box, box2)
