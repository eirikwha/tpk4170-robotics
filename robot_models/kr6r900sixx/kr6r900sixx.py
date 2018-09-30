from models import ColladaMesh
from pythreejs import Object3D


class KR6R900sixx:
    def __init__(self):
        pass


class BaseLink(Object3D):
    def __init__(self):
        Object3D.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/base_link.dae', scale=0.001)
        self.add(mesh)


class Link1(Object3D):
    def __init__(self):
        Object3D.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_1.dae', scale=0.001)
        self.add(mesh)


class Link2(Object3D):
    def __init__(self):
        Object3D.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_2.dae', scale=0.001)
        self.add(mesh)


class Link3(Object3D):
    def __init__(self):
        Object3D.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_3.dae', scale=0.001)
        self.add(mesh)


class Link4(Object3D):
    def __init__(self):
        Object3D.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_4.dae', scale=0.001)
        self.add(mesh)


class Link5(Object3D):
    def __init__(self):
        Object3D.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_5.dae', scale=0.001)
        self.add(mesh)


class Link6(Object3D):
    def __init__(self):
        Object3D.__init__(self)
        mesh = ColladaMesh('kr6r900sixx/visual/link_6.dae', scale=0.001)
        self.add(mesh)


class Link():
    pass


class Joint:
    pass


class Chain:
    pass


class Link1(Link):
    pass
