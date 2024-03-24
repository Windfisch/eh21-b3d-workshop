from build123d import *

# auto_finger_joint code taken from ZTKF
# slightly modified by Windfisch
from enum import Enum, auto
class FingerType(Enum):
    ODD = auto()
    EVEN = auto()

from build123d import sqrt
from build123d import floor
from itertools import product
from build123d import sin
from build123d import pi
from numpy import linspace

def auto_finger_joint(
        a: Part,
        b: Part,
        min_finger_width: float,
        swap: bool = False,
        finger_type: FingerType = None
    ) -> tuple[Part, Part]:

    # We're operating on the intersection of the two parts
    inter = a.intersect(b)
    if len(inter.faces()) == 0:
        return a,b

    edges = inter.edges().copy()
    edges.sort(key=lambda e: e.length, reverse=True)

    # The operation will be along the shortest of the longest 4
    # edges in the direction of the edge
    edge = edges[0]
    z_dir = (edge @ 1 - edge @ 0).normalized()

    # Determine the number of fingers, one is added to the base
    # count since there is technically a 0th cut. That flips some
    # of the even/odd logic 
    n_fingers = floor(edge.length/min_finger_width) + 1
    if finger_type == FingerType.EVEN and not n_fingers & 1:
        n_fingers -= 1
    elif finger_type == FingerType.ODD and n_fingers & 1:
        n_fingers -= 1
    
    # These are the arrays we'll be filling
    fingers_a, fingers_b = [], []

    # We'll use linspace to evenly space the fingers, skip the
    # first and last because they're outside the intersection
    alternate = (fingers_a, fingers_b)
    to_div = inter

    # 1 is added here since 
    for x in linspace(0.0, 1.0, n_fingers)[1:-1]:

        # Split by our plane along the edge
        plane = Plane(origin=edge @ x, z_dir=z_dir)
        divs = [shape for shape in to_div.split(plane, Keep.BOTH)]

        # Select the correct bottom/top
        if plane.to_local_coords(divs[0]).center().Z >= 0:
            alternate[0].append(divs[1])
            to_div = divs[0]
        else:
            alternate[0].append(divs[0])
            to_div = divs[1]

        # Swap the arrays
        alternate = (alternate[1], alternate[0])

    # The remainder will be the last finger
    alternate[0].append(to_div)

    if swap:
        return (a - fingers_b, b - fingers_a)
    else:
        return (a - fingers_a, b - fingers_b)
