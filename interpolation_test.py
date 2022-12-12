import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from StressInterpolator import StressInterpolator
from StressInterpolator2D import StressInterpolator2D

def func(x, y):
    return x*(1-x)*np.cos(4*np.pi*x) * np.sin(4*np.pi*y**2)**2

def test_griddata():
    grid_x, grid_y = np.mgrid[0:1:100j, 0:1:200j]

    rng = np.random.default_rng()
    points = rng.random((1000, 2))
    values = func(points[:,0], points[:,1])

    grid_z0 = griddata(points, values, (grid_x, grid_y), method='nearest')
    grid_z1 = griddata(points, values, (grid_x, grid_y), method='linear')
    grid_z2 = griddata(points, values, (grid_x, grid_y), method='cubic')

    plt.subplot(221)
    plt.imshow(func(grid_x, grid_y).T, extent=(0,1,0,1), origin='lower')
    plt.plot(points[:,0], points[:,1], 'k.', ms=1)
    plt.title('Original')
    plt.subplot(222)
    plt.imshow(grid_z0.T, extent=(0,1,0,1), origin='lower')
    plt.title('Nearest')
    plt.subplot(223)
    plt.imshow(grid_z1.T, extent=(0,1,0,1), origin='lower')
    plt.title('Linear')
    plt.subplot(224)
    plt.imshow(grid_z2.T, extent=(0,1,0,1), origin='lower')
    plt.title('Cubic')
    plt.gcf().set_size_inches(6, 6)
    plt.show()

def test_StressInterpolator():
    intrp = StressInterpolator('RESULTS\\biax\\rombusz_equiv_stress.txt')
    intrp.show(view3d=False, plane='xz', offset=-5.0, range=0.2, s=1.0, alpha=1.0)
    print(intrp.interpolate(0.0, 0.0, 0.0))

def test_StressInterpolator2D():
    intrp = StressInterpolator2D('RESULTS\\rombusz_equiv_stress_2D_15MPa.txt', plane='xy')
    intrp.show(s=1.0, alpha=1.0, sigma_max=80)

    grid_x, grid_y = np.mgrid[-35:35:100j, -55:55:100j]
    grid_0 = intrp.interpolate(grid_x, grid_y, method='nearest')
    grid_1 = intrp.interpolate(grid_x, grid_y, method='linear')
    grid_2 = intrp.interpolate(grid_x, grid_y, method='cubic')

    s = 1.0
    alpha = 1.0
    plt.subplot(221)
    plt.scatter(intrp.points[:, 0], intrp.points[:, 1], s=s, alpha=alpha, c=intrp.stresses, cmap=cm.jet)
    plt.axis('equal')
    plt.title('Input')
    plt.subplot(222)
    plt.scatter(grid_x, grid_y, s=s, alpha=alpha, c=grid_0, cmap=cm.jet)
    plt.axis('equal')
    plt.title('Nearest')
    plt.subplot(223)
    plt.scatter(grid_x, grid_y, s=s, alpha=alpha, c=grid_1, cmap=cm.jet)
    plt.axis('equal')
    plt.title('Linear')
    plt.subplot(224)
    plt.scatter(grid_x, grid_y, s=s, alpha=alpha, c=grid_2, cmap=cm.jet)
    plt.axis('equal')
    plt.title('Cubic')
    plt.show()

    print(intrp.interpolate(0.0, 0.0, method='linear'))

test_StressInterpolator2D()