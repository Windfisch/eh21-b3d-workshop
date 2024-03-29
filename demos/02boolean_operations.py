# %%
from build123d import *
from ocp_vscode import *
set_defaults(
    reset_camera=False,
    default_opacity=0.7
)

# %%

sphere = Sphere(10)
cyl = Cylinder(3, 30)
cylinders = Rot((0,0,0)) * cyl + \
    Rot((0,90,0)) * cyl + \
    Rot((90,0,0)) * cyl

show(
    Location((0, 0,0))   * (sphere + cylinders),
    Location((0, 40,0))  * (sphere - cylinders),
    Location((40, 0,0)) * (sphere & cylinders),
    Location((40, 40, 0)) * (Rectangle(20,20) - Circle(5))
)