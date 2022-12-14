import numpy as np
from StressInterpolator2D import StressInterpolator2D
from mod_between import mod_between

class ExtrusionRatioMapper2D:
    def __init__(self, interpolator: StressInterpolator2D, offsets: tuple[float, float, float], periods: tuple[float, float, float], plane='xy'):
        """Creates an ExtrusionRatioMapper2D instance, which defines the extrusion percentage 
        of a 3D printed part at an arbitrary position based on a 2D stress map.
        The 2D stress map is provided via an interpolator instance.

        interpolator -- A StressInterpolator2D instance
        offsets -- The X, Y and Z coordinates of the origin of the stress map in the 
            coordinate system of the 3D printer (depends on the printer)
        plane -- The plane on which the extrusion ratio is changing ('xy' : default, 'yz' or 'xz')
        """
        if plane != 'xy' and plane != 'yz' and plane != 'xz':
            raise ValueError(f"Invalid plane '{plane}', should be 'xy', 'yz' or 'xz'.")

        self.interpolator = interpolator
        self.plane = plane
        self.x_off = offsets[0]
        self.y_off = offsets[1]
        self.z_off = offsets[2]
        self.x_per = periods[0]
        self.y_per = periods[1]
        self.z_per = periods[2]
    
    def config_linear(self, p0: float, p1: float) -> None:
        """Configurates the linear mapping coefficients p0 and p1 for
        p = p0 + p1*sigmabar, where p is the extrusion percentage [-]
        and sigmabar is dimensionless stress [-].
        """
        self.p0 = p0
        self.p1 = p1
    
    def map_linear(self, x: float, y: float, z: float) -> float:
        """Defines the extrusion percentage p for a 2D stress map as a linear function
        of the interpolated dimensionless stress value at the given (x,y,z) location as p = p0 + p1*sigmabar.
        The linear mapping coefficients p0 [1] and p1 [1] have to be configured first
        using the function config_linear.
        """
        xr = mod_between(np.array(x) - self.x_off, self.x_per)
        yr = mod_between(np.array(y) - self.y_off, self.y_per)
        zr = mod_between(np.array(z) - self.z_off, self.z_per)

        match self.plane:
            case 'xy':
                val1 = xr
                val2 = yr
            case 'yz':
                val1 = yr
                val2 = zr
            case 'xz':
                val1 = xr
                val2 = zr
        stress = self.interpolator.interpolate(val1, val2)
        max_stress = self.interpolator.max_stress()
        dimless_stress = stress / max_stress
        p = self.p0 + self.p1*dimless_stress
        return p
