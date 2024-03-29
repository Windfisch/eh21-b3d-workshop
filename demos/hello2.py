# %%
from build123d import *
from ocp_vscode import *
# %%
sph = Location((10,0,20)) *  Sphere(radius = 10)
cyl = Location((0,0,0), (45, 45, 0)) * Cylinder(radius = 5, height = 10)
show(sph, cyl)
