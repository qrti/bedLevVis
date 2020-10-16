# bedLevVis.py V0.9 201016 qrt@qland.de
# heatbed level visualizer 
#
# retrieve the stored mesh/matrix data (octoprint terminal)
# M420 V
#
# copy and paste mesh/matrix data to raw variable in this program (carefully keep the formatting)
# set the variables for bedform, bedsize, inset, zrange for your heatbed

from mpl_toolkits import mplot3d    # (pip install --upgrade pip setuptools wheel)
                                    # pip install --upgrade matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import re                           # regular expressions, pip install regex
import numpy as np                  # numpy,               pip install numpy

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

raw = """\
Recv:  0 -0.407 -0.300 -0.185 -0.121 +0.009 +0.088 +0.090
Recv:  1 -0.269 -0.226 -0.107 +0.014 +0.092 +0.057 +0.037
Recv:  2 -0.179 -0.101 -0.007 +0.087 +0.133 +0.086 -0.048
Recv:  3 -0.107 -0.082 +0.010 +0.093 +0.124 +0.072 -0.136
Recv:  4 -0.130 -0.118 -0.037 +0.026 +0.053 -0.015 -0.099
Recv:  5 -0.212 -0.178 -0.121 -0.057 -0.026 -0.068 -0.109
Recv:  6 -0.312 -0.265 -0.206 -0.123 -0.074 -0.074 -0.127"""

bedform = 'round'       # round or square
bedsize = 200           # mm
inset = 10              # mm, control point (maesurement) offset from edge of bed
zrange = 1              # mm, reduce to upscale bed level differences

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

data = [float(s) for s in re.sub(r"Recv: +\d+ +", "", raw).split()]     # strip text and store control points in a list of floats
p = int(np.sqrt(len(data)))                                             # get power of data
level = [data[p*i:p*(i+1)] for i in range(p)]                           # group control points to a nested list
bh = bedsize / 2                                                        # bed half size

# - - - - - - - - - - - - - - - - - - -

x = np.linspace(-bh+inset, bh-inset, p)                                 # x range of control points
y = np.linspace(-bh+inset, bh-inset, p)                                 # y

X, Y = np.meshgrid(x, y)                                                # x, y meshgrid of control points
Z = np.array(level)                                                     # numpy array of control points

fig = plt.figure()                                                      # create new figure
ax = fig.gca(projection='3d')                                           # add axes to figure (ax = plt.axes(projection='3d')

ax.set_xlim3d(-bh, bh)                                                  # axis limits
ax.set_ylim3d(-bh, bh)
ax.set_zlim3d(-zrange, zrange)                                          

ax.plot_wireframe(X, Y, Z, color='blue')                                # plot wireframe

# - - - - - - - - - - - - - - - - - - -

if bedform == 'round':                                                  # round bed
    theta = np.linspace(0, 2*np.pi, 100)                                # angel range 0..2*pi, 100 stations
    cx = bh * np.cos(theta)                                             # circle stations x
    cy = bh * np.sin(theta)                                             #                 y
elif bedform == 'square':                                               # square bed
    cx = [-bh, -bh, bh, bh, -bh]                                        # square stations x
    cy = [-bh, bh, bh, -bh, -bh]                                        #                 y

verts = [list(zip(cx, cy, [0] * 100))]                                  # vertices in xy-plane z=0
face = Poly3DCollection(verts, alpha=.25, facecolor='gray')             # face grey transparent
ax.add_collection3d(face)                                               # add face
ax.plot(cx, cy, 0, color="gray")                                        # plot edge grey opaque in xy-plane z=0

# - - - - - - - - - - - - - - - - - - -

ax.set_title('Heatbed Level')                                           # set title

ax.set_xlabel('x', fontsize=20)                                         # lable axis
ax.set_ylabel('y', fontsize=20)
ax.set_zlabel('z', fontsize=20)

plt.show()                                                              # show plot
