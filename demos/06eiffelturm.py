# %%

import lasercut_tools
from auto_finger_joint import auto_finger_joint, FingerType
from build123d import *
from ocp_vscode import *
from math import *

set_defaults(
    black_edges=True,
    render_joints=True,
    render_edges=True,
    reset_camera=False,
    default_opacity=0.7
)
# %%


svg = import_svg("img/eiffelturm.svg")
part = extrude(scale(svg.faces()[0], 3), 3.1/2, both=True)

center = part.center()
center.Z = 0

part = Location(-center) * part


part = Rot((90,0,0)) * part
part2 = Rot((0,0,90)) * part

show(part, part2)

# Might be useful to know:
# edge = foo.edges()[42]
# midpoint = edge @ 0.5

# your code here

def auto_slot_joint(foo, bar):
    print("TODO")
    # find intersection of the two parts

    # split the intersection into an upper and a lower half

    # remove half from foo, the other from bar

    # return the resulting (foomod, barmod) tuple

