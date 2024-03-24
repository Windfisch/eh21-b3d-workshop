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

# %%

thing = extrude(Rectangle(150, 150), 90, taper = 35)
thing += extrude(thing.faces().sort_by(Axis.Z)[-1], 120, taper=5)

#thing -= Sphere(36)
thing -= extrude(Rectangle(70, 70), 30, taper=30)
thing -= Location((0,0,48)) * extrude(Rectangle(45, 45), 30, taper=30)

show(thing)

# %%

part = thing & extrude(Plane.XZ * Rectangle(9999, 9999), 1.5, both=True)
part2 = thing & extrude(Plane.YZ * Rectangle(9999, 9999), 1.5, both=True)

show(part, part2)

# %%
def auto_slot_joint(a, b, height=0.5):
    sec = a & b
    edge = sec.edges().sort_by(SortBy.LENGTH)[-1]
    point = edge @ height
    z_dir = (edge @ 1 - edge @ 0).normalized()
    plane = Plane(origin = point, z_dir = z_dir)
    for_a = sec.split(plane, Keep.TOP).solids()
    for_b = sec.split(plane, Keep.BOTTOM).solids()
    return (a - for_b, b - for_a)

part, part2 = auto_slot_joint(part, part2, 0.3)

part = lasercut_tools.straighten_cuts(part)[0]
part2 = lasercut_tools.straighten_cuts(part2)[0]

svg = lasercut_tools.make_svg([part, part2], "out/eiffelturm.svg")



show(part, part2, svg)
# %%
