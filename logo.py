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

def face_to_solid(face):
    normal = face.normal_at(face.position_at(0.5, 0.5))
    return extrude(face, -3, dir = normal)

TAPER = 0 # 10

# Note: The importer uses the "id" field, not the "inkscape:label" field
# What you can edit in the "Objects/Layers" Tab in inkscape is only the "inkscape:label"
# property. You need to use the object settings to change "id"
svg = import_svg("img/logo_front_simplified.svg")
faces = { face.label: scale(face,2) for face in svg }

ear_r = faces['ear_r']
ear_l = faces['ear_l']
tooth_r = faces['tooth_r']
tooth_l = faces['tooth_l']
head = faces['head']
zero = faces['zero']
one = faces['one']

if TAPER != 0:
    head = extrude(head, 50, taper=TAPER)
else:
    head = extrude(head, -50)

# Create the teeth

# Make teeth from 3mm thick wood, and move them a bit
tooth_r = Location((0,0,-6)) * extrude(tooth_r, -3)
tooth_l = Location((0,0,-6)) * extrude(tooth_l, -3)

# Add some material for mounting so they don't float in the air.
# We're adding way too much because we're gonna correct that later
tooth_r += Location(tooth_r.center()) * Box(10,20,3, align=(Align.CENTER, Align.MIN, Align.CENTER))
tooth_l += Location(tooth_l.center()) * Box(10,20,3, align=(Align.CENTER, Align.MIN, Align.CENTER))

# Shorten that additional mounting tab by stripping away everything
# which would be "inside" the head.
tooth_r -= head
tooth_l -= head

# Lengthen that mounting tab again, but only by 3mm. (We need some
# overlap with the head, so we can stick it through a hole later)
tooth_r += extrude(tooth_r.faces().sort_by(Axis.Y)[-1], 3, dir = (0,1,0))
tooth_l += extrude(tooth_l.faces().sort_by(Axis.Y)[-1], 3, dir = (0,1,0))


# Make the head lasercuttable

head = [face_to_solid(h) for h in head.faces()]

# Find the front face, and remove the "eyes" from it.
head.sort(key = lambda f: -f.center().Z)
head[0]  -= extrude(zero + one, -3)

# The ears

# Make ears from 3mm thick wood, and move them to the back of the head.

ear_r = Location((0,-35 * tan(TAPER * pi / 180),-35)) * extrude(ear_r, -3)
ear_l = Location((0,-41 * tan(TAPER * pi / 180),-41)) * extrude(ear_l, -3)

# Extend the bottom face by 3mm, so we intersect with the head

ear_r += extrude(ear_r.faces().sort_by(Axis.Y)[0], 3)
ear_l += extrude(ear_l.faces().sort_by(Axis.Y)[0], 3)



# Make lasercut tabs

print("making tabs...")
head.sort(key = lambda f: f.center().Y)

print("ears")
head[-1], ear_r = auto_finger_joint(head[-1], ear_r, 6)
head[-1], ear_l = auto_finger_joint(head[-1], ear_l, 6)

print("teeth")
head[0], tooth_l = auto_finger_joint(head[0], tooth_l, 3)
head[0], tooth_r = auto_finger_joint(head[0], tooth_r, 3)

print("head")
for i in range(len(head)):
    for j in range(i+1, len(head)):
        head[i], head[j] = auto_finger_joint(head[i], head[j], 15)

print("post-processing")
head = [lasercut_tools.straighten_cuts(h)[0] for h in head]

# %%

show(ear_r, ear_l, tooth_r, tooth_l,  head, names= ["ear_r", "ear_l", "tooth_r", "tooth_l", "head"])

# %%
print("writing svg")
lasercut_tools.make_svg([ear_r, ear_l, tooth_r, tooth_l] + head, "out/rabbit.svg", burn_width = 0.17)
