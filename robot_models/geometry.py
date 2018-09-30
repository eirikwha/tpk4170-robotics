from pythreejs import Group
from pythreejs import Mesh
from pythreejs import Geometry, Line, SphereGeometry
from pythreejs import LineBasicMaterial, MeshLambertMaterial
from pythreejs import AxesHelper as Axes


class Grid(Group):
    def __init__(self, num_cells=5, color='#cccccc', linewidth=1, cellsize=0.5):
        Group.__init__(self)
        material = LineBasicMaterial(color=color, linewidth=linewidth)
        for i in range(num_cells+1):
            edge = cellsize * num_cells / 2
            position = edge - (i * cellsize)
            geometry_h = Geometry(vertices=[(-edge, position, 0),
                                            (edge, position, 0)])
            geometry_v = Geometry(vertices=[(position, -edge, 0),
                                            (position, edge, 0)])
            self.add(Line(geometry=geometry_h, material=material))
            self.add(Line(geometry=geometry_v, material=material))


class Ball(Mesh):
    def __init__(self, color='red', radius=0.025):
        Mesh.__init__(self, geometry=SphereGeometry(radius=radius),
                      material=MeshLambertMaterial(color=color))
