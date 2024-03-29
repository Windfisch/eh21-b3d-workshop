# %%
import lasercut_tools
from auto_finger_joint import auto_finger_joint, FingerType
from build123d import *
from ocp_vscode import *
from math import *

box = Box(50,50,50)
roof = Location((0,0,25), (45,0,0)) * Box(50, 1/sqrt(2)*50, 1/sqrt(2)*50)

house = box + roof

show(house)

elems = [extrude(face, -3) for face in house.faces()]

# applies combinator(a,b) for all of things and replaces them with the results.
def combine_pairwise(things, combinator):
    for i in range(len(things)):
        for j in range(i+1, len(things)):
            things[i], things[j] = combinator(things[i], things[j])
    
    return things

def auto_finger_joint_pairwise(things, min_finger_width: float, swap:bool = False, finger_type: FingerType = None):
    return combine_pairwise(things, lambda a,b : auto_finger_joint(a, b, min_finger_width, swap, finger_type))

elems = auto_finger_joint_pairwise(elems, 5)

elems = [lasercut_tools.straighten_cuts(e)[0] for e in elems]

lasercut_tools.make_svg(elems, "out/house.svg")


show(elems, house)

#lasercut_tools.
