from models import ColladaMesh
from pythreejs import Object3D, AxesHelper
import numpy as np
from transformations import quaternion_from_matrix


class KR6R900sixx:
    def __init__(self):
        pass


class Link(Object3D):
    def __init__(self):
        Object3D.__init__(self)

    def __call__(self, trf):
        self.quaternion = quaternion_from_matrix(trf).tolist()
        self.position = (trf[:3, 3]).tolist()


class BaseLink(Link):
    def __init__(self):
        Object3D.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/base_link.dae', scale=0.001)
        self.add(mesh)
        axes = AxesHelper(size=0.5)
        self.add(axes)


class Link1(Link):
    def __init__(self):
        Link.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_1.dae', scale=0.001)
        mesh.rotateX(np.pi/2)
        mesh.position = (-0.025, 0.0, 0.0)
        self.mesh = mesh
        self.add(mesh)
        axes = AxesHelper(size=0.5)
        self.add(axes)


class Link2(Link):
    def __init__(self):
        Link.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_2.dae', scale=0.001)
        mesh.rotateZ(np.pi/2)
        mesh.rotateX(np.pi/2)
        mesh.position = (-0.455, 0.0, 0.0)
        self.mesh = mesh
        self.add(mesh)
        axes = AxesHelper(size=0.5)
        self.add(axes)


class Link3(Link):
    def __init__(self):
        Link.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_3.dae', scale=0.001)
        mesh.position = (-0.035, 0.0, -0.025)
        mesh.rotateZ(np.pi)
        mesh.rotateY(-np.pi/2)
        self.mesh = mesh
        self.add(mesh)


class Link4(Link):
    def __init__(self):
        Link.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_4.dae', scale=0.001)
        mesh.rotateZ(np.pi/2)
        mesh.rotateX(np.pi/2)
        mesh.position = (0.0, -0.42, 0)
        self.mesh = mesh
        self.add(mesh)
        axes = AxesHelper(size=0.5)
        self.add(axes)


class Link5(Link):
    def __init__(self):
        Link.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_5.dae', scale=0.001)
        mesh.rotateX(np.pi)
        mesh.rotateY(np.pi/2)
        self.mesh = mesh
        self.add(mesh)
        axes = AxesHelper(size=0.5)
        self.add(axes)


class Link6(Link):
    def __init__(self):
        Link.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_6.dae', scale=0.001)
        mesh.rotateY(-np.pi/2)
        self.mesh = mesh
        self.add(mesh)
        axes = AxesHelper(size=0.5)
        self.add(axes)


class Joint:
    pass


class Chain:
    pass