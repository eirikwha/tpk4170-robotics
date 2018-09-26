from pythreejs import *
import numpy as np
from collada import Collada
from matplotlib.colors import to_hex
import ipywidgets
from transformations import quaternion_from_euler, quaternion_about_axis
import time
from traitlets import observe


def mesh_from_dae(dae, name='', scale=1.0):
    materials = materials_from_dae(dae)
    group = Group()
    for geometry in dae.geometries:
        for primitive in geometry.primitives:
            vertices = primitive.vertex[primitive.vertex_index] * scale
            normals = primitive.normal[primitive.normal_index]
            buffer_geometry = BufferGeometry(
                attributes={'position': BufferAttribute(array=vertices),
                            'normal': BufferAttribute(array=normals)})
            material = materials[primitive.material]
            mesh = Mesh(geometry=buffer_geometry, material=material)
            group.add(mesh)
    group.name = name
    return group


def materials_from_dae(dae):
    materials = {}
    for material in dae.materials:
        name = material.id
        color = to_hex(material.effect.diffuse)
        specular = to_hex(material.effect.specular)
        materials[name] = MeshPhongMaterial(color=color,
                                            specular=specular,
                                            shininess=30)
    return materials


def grid(num_cells=5, color='#cccccc', linewidth=1, cellsize=0.5):
    grid = Group()
    material = LineBasicMaterial(color=color, linewidth=linewidth)
    for i in range(num_cells+1):
        edge = cellsize * num_cells / 2
        position = edge - (i * cellsize)
        geometry_h = Geometry(vertices=[(-edge, position, 0),
                                        (edge, position, 0)])
        geometry_v = Geometry(vertices=[(position, -edge, 0),
                                        (position, edge, 0)])
        grid.add(Line(geometry=geometry_h, material=material))
        grid.add(Line(geometry=geometry_v, material=material))
    return grid


def ball(color='red', radius=0.025):
    ball = Mesh(geometry=SphereGeometry(radius=radius),
                material=MeshLambertMaterial(color=color))
    return ball


class Robot(object):
    def __init__(self):
        self._chain = None
        self._ee = None

    def display(self):
        key_light = DirectionalLight(color='white', position=[
                                     3, 3, 3], intensity=0.66)

        near = 0.01
        far = 1000
        width = 768
        height = 512

        c = PerspectiveCamera(40, width/height, near, far)
        c.position = [3, 3, 3]
        c.up = [0, 0, 1]

        c.add(key_light)

        pl = PointLight(color='0xffffff', intensity=0.1,
                        position=[3, 3, 3])

        axes = AxesHelper(size=0.5)

        # scene = Scene(background=None)
        scene = Scene()
        scene.background = "#111111"

        # scene = Scene()
        scene.add(axes)
        scene.add(AmbientLight())
        scene.add(pl)
        scene.add(grid())

        scene.add(self._chain)

        renderer = Renderer(camera=c,
                            scene=scene,
                            antialias=True,
                            controls=[OrbitControls(controlling=c)],
                            height=height, width=width)
        display(renderer)

    def _ee_debug_call_twice(self):
        self._ee.exec_three_obj_method('updateMatrixWorld')
        return np.array(self._ee.matrixWorld).reshape(4, 4).T


class KR6R900sixx(Robot):
    def __init__(self, q = np.array([0.0, -np.pi/2, np.pi/2, 0.0, np.pi/2, 0.0]), interact=False):

        self._q = q
        self._ee = None

        base_dae = Collada('kr6r900sixx/visual/base_link.dae')
        link_1_dae = Collada('kr6r900sixx/visual/link_1.dae')
        link_2_dae = Collada('kr6r900sixx/visual/link_2.dae')
        link_3_dae = Collada('kr6r900sixx/visual/link_3.dae')
        link_4_dae = Collada('kr6r900sixx/visual/link_4.dae')
        link_5_dae = Collada('kr6r900sixx/visual/link_5.dae')
        link_6_dae = Collada('kr6r900sixx/visual/link_6.dae')

        base_link = mesh_from_dae(base_dae, name='base_link', scale=0.001)
        link_1 = mesh_from_dae(link_1_dae, name='link_1', scale=0.001)
        link_2 = mesh_from_dae(link_2_dae, name='link_2', scale=0.001)
        link_2.rotateY(pi/2)
        link_3 = mesh_from_dae(link_3_dae, name='link_3', scale=0.001)
        link_3.position = [-0.025, 0.0, 0.0]
        link_4 = mesh_from_dae(link_4_dae, name='link_4', scale=0.001)
        link_5 = mesh_from_dae(link_5_dae, name='link_5', scale=0.001)
        link_6 = mesh_from_dae(link_6_dae, name='link_6', scale=0.001)

        self._chain = Object3D(name='base_frame', children=[base_link])

        j1 = Object3D(name='j1', position=[0.0, 0.0, 0.400])
        j1.add(link_1)
        j2 = Object3D(name='j2', position=[0.025, 0.0, 0.0])
        j2.add(link_2)
        j3 = Object3D(name='j3', position=[0.455, 0.0, 0.0])
        j3.add(link_3)
        j4 = Object3D(name='j4', position=[0.0, 0.0, 0.035])
        j4.add(link_4)
        j5 = Object3D(name='j5', position=[0.42, 0.0, 0.0])
        j5.add(link_5)
        j6 = Object3D(name='j6', position=[0.080, 0.0, 0.0])
        j6.add(link_6)

        # j1.add(AxesHelper(size=0.5))
        # j2.add(AxesHelper(size=0.5))
        # j3.add(AxesHelper(size=0.5))
        # j4.add(AxesHelper(size=0.5))
        # j5.add(AxesHelper(size=0.5))
        # j6.add(AxesHelper(size=0.5))

        tool0 = Object3D(name='tool0', position=[0.0, 0.0, 0.0])
        tool0.rotateY(pi/2)
        tool0.add(AxesHelper(size=0.5))

        tool0.add(ball())

        self._ee = tool0

        self._chain.add(j1)
        j1.add(j2)
        j2.add(j3)
        j3.add(j4)
        j4.add(j5)
        j5.add(j6)
        j6.add(tool0)

        self._joints = [j1, j2, j3, j4, j5, j6]

        self.q = self._q

        self.display()

        if interact:
            self.interact()

    def _show_axes_helpers(self, show=False):
        for j in self._joints:
            j.add(AxesHelper(size=0.5))

    def interact(self):
        def f(q1, q2, q3, q4, q5, q6):
            
            # self._joints[0].quaternion = quaternion_about_axis(
            #     q1, (0, 0, -1, 0)).tolist()
            # self._joints[1].quaternion = quaternion_about_axis(
            #     q2, (0, 1, 0, 0)).tolist()
            # self._joints[2].quaternion = quaternion_about_axis(
            #     q3, (0, 1, 0, 0)).tolist()
            # self._joints[3].quaternion = quaternion_about_axis(
            #     q4, (-1, 0, 0, 0)).tolist()
            # self._joints[4].quaternion = quaternion_about_axis(
            #     q5, (0, 1, 0, 0)).tolist()
            # self._joints[5].quaternion = quaternion_about_axis(
            #     q6, (-1, 0, 0, 0)).tolist()

            self.q = np.array([q1, q2, q3, q4, q5, q6])

        ipywidgets.interact(f,
                            q1=(np.deg2rad(-185), np.deg2rad(185)),
                            q2=(np.deg2rad(-155), np.deg2rad(35)),
                            q3=(np.deg2rad(-130), np.deg2rad(154)),
                            q4=(np.deg2rad(-350), np.deg2rad(350)),
                            q5=(np.deg2rad(-130), np.deg2rad(130)),
                            q6=(np.deg2rad(-350), np.deg2rad(350)))
        

        

    @property
    def q(self):
        return self._q

    @q.setter
    def q(self, q):
        self._q = np.copy(q)
        self._joints[0].quaternion = quaternion_about_axis(
            q[0], (0, 0, -1, 0)).tolist()
        self._joints[1].quaternion = quaternion_about_axis(
            q[1], (0, 1, 0, 0)).tolist()
        self._joints[2].quaternion = quaternion_about_axis(
            q[2], (0, 1, 0, 0)).tolist()
        self._joints[3].quaternion = quaternion_about_axis(
            q[3], (-1, 0, 0, 0)).tolist()
        self._joints[4].quaternion = quaternion_about_axis(
            q[4], (0, 1, 0, 0)).tolist()
        self._joints[5].quaternion = quaternion_about_axis(
            q[5], (-1, 0, 0, 0)).tolist()


class KR16(Robot):
    def __init__(self):

        self._q = np.array([0.0, -np.pi/2, np.pi/2, 0.0, 0.0, 0.0])

        base_dae = Collada('kr16_2/visual/base_link.dae')
        link_1_dae = Collada('kr16_2/visual/link_1.dae')
        link_2_dae = Collada('kr16_2/visual/link_2.dae')
        link_3_dae = Collada('kr16_2/visual/link_3.dae')
        link_4_dae = Collada('kr16_2/visual/link_4.dae')
        link_5_dae = Collada('kr16_2/visual/link_5.dae')
        link_6_dae = Collada('kr16_2/visual/link_6.dae')

        base_link = mesh_from_dae(base_dae, name='base_link')
        base_link.scale = [0.001, 0.001, 0.001]
        link_1 = mesh_from_dae(link_1_dae, name='link_1')
        link_1.position = [0.0, 0.0, -0.675]
        link_1.scale = [0.001, 0.001, 0.001]

        link_2 = mesh_from_dae(link_2_dae, name='link_2')
        link_2.scale = [0.001, 0.001, 0.001]
        link_2.rotateY(pi/2)
        link_2.position = [-0.675, 0.0, 0.26]

        link_3 = mesh_from_dae(link_3_dae, name='link_3')
        link_3.scale = [0.001, 0.001, 0.001]
        link_3.position = [-0.26, 0.0, -1.355]

        link_4 = mesh_from_dae(link_4_dae, name='link_4')
        link_4.scale = [0.001, 0.001, 0.001]
        link_4.position = [-0.93, 0.0, -1.32]

        link_5 = mesh_from_dae(link_5_dae, name='link_5')
        link_5.scale = [0.001, 0.001, 0.001]
        link_5.position = [-0.93, 0.0, -1.32]

        link_6 = mesh_from_dae(link_6_dae, name='link_6')
        link_6.scale = [0.001, 0.001, 0.001]
        link_6.position = [-0.93, 0.0, -1.32]

        self._chain = Object3D(name='base_frame', children=[base_link])

        j1 = Object3D(name='j1', position=[0.0, 0.0, 0.675])
        j1.add(link_1)
        # j1.add(AxesHelper(size=0.5))

        j2 = Object3D(name='j2', position=[0.26, 0.0, 0.0])
        j2.add(link_2)
        # j2.add(AxesHelper(size=0.5))

        j3 = Object3D(name='j3', position=[0.68, 0.0, 0.0])
        j3.add(link_3)
        # j3.add(AxesHelper(size=0.5))

        j4 = Object3D(name='j4', position=[0.67, 0.0, -0.035])
        j4.add(link_4)
        # j4.add(AxesHelper(size=0.5))

        j5 = Object3D(name='j5', position=[0.0, 0.0, 0.0])
        j5.add(link_5)
        # j5.add(AxesHelper(size=0.5))

        j6 = Object3D(name='j6', position=[0.0, 0.0, 0.0])
        j6.add(link_6)
        # j6.add(AxesHelper(size=0.5))

        tool0 = Object3D(name='tool0', position=[0.158, 0.0, 0.0])
        tool0.rotateY(pi/2)
        tool0.add(AxesHelper(size=0.5))

        self._chain.add(j1)
        j1.add(j2)
        j2.add(j3)
        j3.add(j4)
        j4.add(j5)
        j5.add(j6)
        j6.add(tool0)

        self._joints = [j1, j2, j3, j4, j5, j6]

        self.set_q(self._q)

    def interact(self):
        def f(q1, q2, q3, q4, q5, q6):
            self._q = np.array([q1, q2, q3, q4, q5, q6])

            self._joints[0].quaternion = quaternion_about_axis(
                q1, (0, 0, -1, 0)).tolist()
            self._joints[1].quaternion = quaternion_about_axis(
                q2, (0, 1, 0, 0)).tolist()
            self._joints[2].quaternion = quaternion_about_axis(
                q3, (0, 1, 0, 0)).tolist()
            self._joints[3].quaternion = quaternion_about_axis(
                q4, (-1, 0, 0, 0)).tolist()
            self._joints[4].quaternion = quaternion_about_axis(
                q5, (0, 1, 0, 0)).tolist()
            self._joints[5].quaternion = quaternion_about_axis(
                q6, (-1, 0, 0, 0)).tolist()

        ipywidgets.interact(f,
                            q1=(np.deg2rad(-185), np.deg2rad(185)),
                            q2=(np.deg2rad(-155), np.deg2rad(35)),
                            q3=(np.deg2rad(-130), np.deg2rad(154)),
                            q4=(np.deg2rad(-350), np.deg2rad(350)),
                            q5=(np.deg2rad(-130), np.deg2rad(130)),
                            q6=(np.deg2rad(-350), np.deg2rad(350)))

    @property
    def q(self):
        return self._q

    def set_q(self, q):
        self._q = np.copy(q)
        self._joints[0].quaternion = quaternion_about_axis(
            q[0], (0, 0, -1, 0)).tolist()
        self._joints[1].quaternion = quaternion_about_axis(
            q[1], (0, 1, 0, 0)).tolist()
        self._joints[2].quaternion = quaternion_about_axis(
            q[2], (0, 1, 0, 0)).tolist()
        self._joints[3].quaternion = quaternion_about_axis(
            q[3], (-1, 0, 0, 0)).tolist()
        self._joints[4].quaternion = quaternion_about_axis(
            q[4], (0, 1, 0, 0)).tolist()
        self._joints[5].quaternion = quaternion_about_axis(
            q[5], (-1, 0, 0, 0)).tolist()


class UR5(Robot):
    def __init__(self):
        self._q = np.array([0, 0, 0, 0, 0, 0])
        self._q_offset = np.array([0, np.pi/2, 0, np.pi/2, 0, 0])

        base_dae = Collada('ur5/visual/base.dae')
        forearm_dae = Collada('ur5/visual/forearm.dae')
        shoulder_dae = Collada('ur5/visual/shoulder.dae')
        upperarm_dae = Collada('ur5/visual/upperarm.dae')
        wrist1_dae = Collada('ur5/visual/wrist1.dae')
        wrist2_dae = Collada('ur5/visual/wrist2.dae')
        wrist3_dae = Collada('ur5/visual/wrist3.dae')

        base_link = mesh_from_dae(base_dae)
        shoulder_link = mesh_from_dae(shoulder_dae)
        upper_arm_link = mesh_from_dae(upperarm_dae)
        forearm_link = mesh_from_dae(forearm_dae)
        wrist1_link = mesh_from_dae(wrist1_dae)
        wrist2_link = mesh_from_dae(wrist2_dae)
        wrist3_link = mesh_from_dae(wrist3_dae)

        ee_link = Object3D()
        ee_link.add(AxesHelper())

        tool_0 = Object3D()
        tool_0.add(AxesHelper())

        self._chain = Object3D(children=[base_link])

        shoulder_pan_joint = Object3D(position=[0., 0., 0.089159])
        shoulder_pan_joint.add(shoulder_link)

        shoulder_lift_joint = Object3D(position=[0., 0.13585, 0.0])
        # shoulder_lift_joint.rotateY(np.pi/2)
        shoulder_lift_joint.add(upper_arm_link)

        elbow_joint = Object3D(position=[0., -0.1197, 0.425])
        elbow_joint.add(forearm_link)

        wrist_1_joint = Object3D(position=[0., 0., 0.39225])
        # wrist_1_joint.rotateY(np.pi/2)
        wrist_1_joint.add(wrist1_link)

        wrist_2_joint = Object3D(position=[0., 0.1095+0.1197-0.13585, 0.])
        wrist_2_joint.add(wrist2_link)

        wrist_3_joint = Object3D(position=[0., 0., 0.09465])
        wrist_3_joint.add(wrist3_link)

        ee_fixed_joint = Object3D(
            name='ee_fixed_joint', position=[0., 0.0823, 0.0])
        ee_fixed_joint.rotateZ(np.pi/2)
        ee_fixed_joint.add(ee_link)

        wrist_3_link_tool0_fixed_joint = Object3D(position=[0.0, 0.0823, 0.0])
        wrist_3_link_tool0_fixed_joint.rotateX(-np.pi/2)
        wrist_3_link_tool0_fixed_joint.add(tool_0)

        self._chain.add(shoulder_pan_joint)
        shoulder_pan_joint.add(shoulder_lift_joint)
        shoulder_lift_joint.add(elbow_joint)
        elbow_joint.add(wrist_1_joint)
        wrist_1_joint.add(wrist_2_joint)
        wrist_2_joint.add(wrist_3_joint)
        wrist_3_joint.add(ee_fixed_joint)
        # wrist_3_joint.add(wrist_3_link_tool0_fixed_joint)

        self._joints = [shoulder_pan_joint,
                        shoulder_lift_joint,
                        elbow_joint,
                        wrist_1_joint,
                        wrist_2_joint,
                        wrist_3_joint]

        self.set_q(self._q)

    def interact(self):
        def f(q1, q2, q3, q4, q5, q6):
            self._q = np.array([q1, q2, q3, q4, q5, q6])

            self._joints[0].quaternion = quaternion_about_axis(
                q1, (0, 0, 1, 0)).tolist()
            self._joints[1].quaternion = quaternion_about_axis(
                q2 + np.pi/2, (0, 1, 0, 0)).tolist()
            self._joints[2].quaternion = quaternion_about_axis(
                q3, (0, 1, 0, 0)).tolist()
            self._joints[3].quaternion = quaternion_about_axis(
                q4 + np.pi/2, (0, 1, 0, 0)).tolist()
            self._joints[4].quaternion = quaternion_about_axis(
                q5, (0, 0, 1, 0)).tolist()
            self._joints[5].quaternion = quaternion_about_axis(
                q6, (0, 1, 0, 0)).tolist()

        ipywidgets.interact(f,
                            q1=(np.deg2rad(-180), np.deg2rad(180)),
                            q2=(np.deg2rad(-180), np.deg2rad(180)),
                            q3=(np.deg2rad(-180), np.deg2rad(180)),
                            q4=(np.deg2rad(-180), np.deg2rad(180)),
                            q5=(np.deg2rad(-180), np.deg2rad(180)),
                            q6=(np.deg2rad(-180), np.deg2rad(180)))

    @property
    def q(self):
        return self._q

    def set_q(self, q):
        self._q = np.copy(q)

        self._joints[0].quaternion = quaternion_about_axis(
            q[0], (0, 0, 1, 0)).tolist()
        self._joints[1].quaternion = quaternion_about_axis(
            q[1] + np.pi/2, (0, 1, 0, 0)).tolist()
        self._joints[2].quaternion = quaternion_about_axis(
            q[2], (0, 1, 0, 0)).tolist()
        self._joints[3].quaternion = quaternion_about_axis(
            q[3], (0, 1, 0, 0)).tolist()
        self._joints[4].quaternion = quaternion_about_axis(
            q[4] + np.pi/2, (0, 0, 1, 0)).tolist()
        self._joints[5].quaternion = quaternion_about_axis(
            q[5], (0, 1, 0, 0)).tolist()


class DenavitHartenberg(object):
    def __init__(self, a, alpha, d, theta):
        self._a = np.array(a)
        self._alpha = np.array(alpha)
        self._d = np.array(d)
        self._theta = np.array(theta)

        self._n = len(a)

    def _transforms(self):
        trfs = []
        for ai, alphai, di, thetai in zip(self._a, self._alpha,
                                          self._d, self._theta):
            trfs.append(self.matrix(ai, alphai, di, thetai))

        itrfs = [trfs[0]]
        T0i = trfs[0]
        for i in range(1, 6):
            T0i = np.dot(T0i, trfs[i])
            itrfs.append(T0i)

        return trfs, itrfs

    def matrix(self, ai, alphai, di, thetai):
        ct = np.cos(thetai)
        st = np.sin(thetai)
        ca = np.cos(alphai)
        sa = np.sin(alphai)
        return np.array([[ct, -st * ca, st * sa, ai * ct],
                         [st,  ct * ca, -ct * sa, ai * st],
                         [0.0, sa, ca, di],
                         [0.0, 0.0, 0.0, 1.0]])

    def geometric_jacobian(self):
        _, Ts = self._transforms()
        p0 = np.array([0, 0, 0])
        z0 = np.array([0, 0, 1])
        pn = Ts[-1][:3, 3]
        J = np.zeros((6, self._n))
        J[:3, 0] = np.cross(z0, pn-p0)
        J[3:, 0] = z0
        for i in range(self._n-1):
            T = Ts[i]
            zi = T[:3, 2]
            pi = T[:3, 3]
            J[:3, i+1] = np.cross(zi, pn-pi)
            J[3:, i+1] = zi
        return J

    @property
    def angles(self):
        return np.array(self._theta)

    @angles.setter
    def angles(self, angles):
        self._theta = angles

    @property
    def ee(self):
        _, Ts = self._transforms()
        return Ts[-1]
