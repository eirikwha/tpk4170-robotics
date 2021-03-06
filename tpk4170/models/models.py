from pythreejs import Group
from pythreejs import Mesh
from pythreejs import Geometry, Line, SphereGeometry, BufferGeometry
from pythreejs import BufferAttribute
from pythreejs import LineBasicMaterial, MeshLambertMaterial, MeshPhongMaterial
from pythreejs import AxesHelper as Axes

from matplotlib.colors import to_hex
from collada import Collada


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


class ColladaMesh(Group):
    def __init__(self, filename, scale=1.0):
        Group.__init__(self)

        self._dae = Collada(filename)
        self._load_mesh(self._dae, scale=scale)

    def _load_mesh(self, dae, scale):
        materials = self._load_material(dae)
        for geometry in dae.geometries:
            for primitive in geometry.primitives:
                vertices = primitive.vertex[primitive.vertex_index] * scale
                normals = primitive.normal[primitive.normal_index]
                buffer_geometry = BufferGeometry(
                    attributes={'position': BufferAttribute(array=vertices),
                                'normal': BufferAttribute(array=normals)})
                material = materials[primitive.material]
                mesh = Mesh(geometry=buffer_geometry, material=material)
                self.add(mesh)

    def _load_material(self, dae):
        materials = {}
        for material in dae.materials:
            name = material.id
            color = to_hex(material.effect.diffuse)
            specular = to_hex(material.effect.specular)
            materials[name] = MeshPhongMaterial(color=color,
                                                specular=specular,
                                                shininess=30)
        return materials
