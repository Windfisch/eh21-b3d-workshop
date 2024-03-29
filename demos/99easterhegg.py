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

# TODO:
# - thicken the ears and place them somewhere
# - turn the solid head box into a collection of 6 faceplates
# - make the "eyes" cutouts
# - make all the finger joints
# - finger joints look broken when faces don't meet in a 90 deg angle
#   use lasercut_tools.straighten_cuts to fix that.
# - export a svg (c.f. lasercut_tools)

show(ear_r, ear_l, tooth_r, tooth_l, head, zero, one)