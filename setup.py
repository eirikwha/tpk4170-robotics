#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tpk4170',
      version='1.0',
      description='Python modules for the course TPK4170 Robotics at NTNU ',
      author='Lars Tingelstad',
      author_email='lars.tingelstad@ntnu.no',
      url='',
      packages=find_packages(exclude=['robot_models']),
      data_files=[
          ('share/tpk4170/models/ur5/visual/',
             [
                 'tpk4170/models/ur5/visual/base.dae',
                 'tpk4170/models/ur5/visual/forearm.dae',
                 'tpk4170/models/ur5/visual/shoulder.dae',
                 'tpk4170/models/ur5/visual/upperarm.dae',
                 'tpk4170/models/ur5/visual/wrist1.dae',
                 'tpk4170/models/ur5/visual/wrist2.dae',
                 'tpk4170/models/ur5/visual/wrist3.dae',
             ]),
          ('share/tpk4170/models/kr6r900sixx/visual/',
           [
               'tpk4170/models/kr6r900sixx/visual/base_link.dae',
               'tpk4170/models/kr6r900sixx/visual/link_1.dae',
               'tpk4170/models/kr6r900sixx/visual/link_2.dae',
               'tpk4170/models/kr6r900sixx/visual/link_3.dae',
               'tpk4170/models/kr6r900sixx/visual/link_4.dae',
               'tpk4170/models/kr6r900sixx/visual/link_5.dae',
               'tpk4170/models/kr6r900sixx/visual/link_6.dae',
           ]),
          ('share/tpk4170/models/kr16_2/visual/',
           [
               'tpk4170/models/kr16_2/visual/base_link.dae',
               'tpk4170/models/kr16_2/visual/link_1.dae',
               'tpk4170/models/kr16_2/visual/link_2.dae',
               'tpk4170/models/kr16_2/visual/link_3.dae',
               'tpk4170/models/kr16_2/visual/link_4.dae',
               'tpk4170/models/kr16_2/visual/link_5.dae',
               'tpk4170/models/kr16_2/visual/link_6.dae',
           ]),
      ],
      )
