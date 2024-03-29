# %%
from build123d import *
from ocp_vscode import *
import copy
from math import *
from auto_finger_joint import auto_finger_joint, FingerType

set_defaults(
    reset_camera=False,
    default_opacity=0.7
)

# %%

foo = Box(50,3,50, align = (Align.MIN, Align.MIN, Align.MIN))
bar = Box(3,50,50, align = (Align.MIN, Align.MIN, Align.MIN))

foo, bar = auto_finger_joint(foo, bar, 5)

show(foo,bar)

