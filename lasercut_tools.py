from build123d import *
from ocp_vscode import *

def project_to_plane(things, plane):
    """Projects things to plane, side-stepping (hopefully) all
    potential problems that might occur."""

    if isinstance(things, Part):
        faces = things.faces()
    else:
        faces = things

    def move_to_positive_plane_side(face, plane):
        z = plane.to_local_coords(face.center()).Z
        size = face.bounding_box().diagonal
        move_by = (size/2-z) * plane.z_dir
        return Location(move_by) * face
        
    faces = [face for face in faces if abs(face.normal_at().dot(plane.z_dir)) > 1e-5]
    faces = [move_to_positive_plane_side(face, plane) for face in faces]

    result = project(faces, plane)
    return result+result

def arrange1d(sketches, spacing = 1):
    """takes a list of sketches/faces and arranges them (very inefficiently)
    so that they don't collide."""
    x = 0
    result = []
    for s in sketches:
        print(s)
        bb = s.bounding_box(1)
        result.append(Location((x - bb.min.X, -bb.min.Y)) * s)
        x += bb.max.X - bb.min.X + spacing
    return result

def make_svg(things, svgfile, burn_width=0.15):
    """Takes a list of plate-like things and prepares an SVG
    suitable for laser-cutting. Performs automatic burn width compensation."""
    faces = []
    for thing in things:
        _, face = straighten_cuts(thing)
        try:
            face = offset(face, amount=burn_width/2)
        except ValueError:
            print("WTF, failed to offset face...")
        faces.append(face)

    arranged = arrange1d(faces)

    exporter = ExportSVG(scale=1)
    exporter.add_layer("Visible")
    exporter.add_shape(arranged, layer="Visible")
    exporter.write(svgfile)

    return arranged

def straighten_cuts(thing):
    """Takes a plate-like thing and turns all cutout directions perpendicular to
    the top/bottom faces. While doing that, it errs on the side of removing too much
    material rather than not enough."""
    face = thing.faces().sort_by(SortBy.AREA)[-1]
    other_face = thing.faces().sort_by(SortBy.AREA)[-2]

    thickness = -(face.center_location.inverse() * other_face.center_location).position.Z
    print(thickness)

    r = face.bounding_box().diagonal
    slice = face.center_location * Circle(r)
    slice = extrude(slice, -thickness)

    negative = slice - thing

    p = Plane(face.center_location)

    proj = p*Circle(r) - project_to_plane(negative, p)
    proj_ext = extrude(proj, -thickness)

    return proj_ext, face.center_location.inverse() * proj
