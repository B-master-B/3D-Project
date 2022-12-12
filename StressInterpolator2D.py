import csv
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math

class StressInterpolator2D:
    def __init__(self, filename, plane='xy'):
        match plane:
            case 'xy':
                col1 = 1
                col2 = 2
                self.xlab = 'X'
                self.ylab = 'Y'
            case 'yz':
                col1 = 2
                col2 = 3
                self.xlab = 'Y'
                self.ylab = 'Z'
            case 'xz':
                col1 = 1
                col2 = 3
                self.xlab = 'X'
                self.ylab = 'Z'
            case _:
                raise ValueError(f"Invalid plane '{plane}', should be 'xy', 'yz' or 'xz'.")
        self.plane = plane

        with open(filename, newline='') as csvfile:
            csvfile.readline()
            csvreader = csv.reader(csvfile, delimiter='\t')
            self.npoint = max(int(row[0]) for row in csvreader)
            self.points = np.empty([self.npoint, 2])
            self.stresses = np.empty(self.npoint)
            csvfile.seek(0)
            next(csvreader) # skip first row (header)
            for row in csvreader:
                id = int(row[0])
                self.points[id - 1, 0] = float(row[col1].replace(',','.'))
                self.points[id - 1, 1] = float(row[col2].replace(',','.'))
                self.stresses[id - 1] = float(row[4].replace(',','.'))
    
    def show(self, s = 1.0, alpha = 1.0, sigma_min = 0.0, sigma_max = 40.0):
        fig = plt.figure()
        ax = fig.add_subplot()
        sc = ax.scatter(self.points[:, 0], self.points[:, 1], s=s, alpha=alpha, c=self.stresses, cmap=cm.jet, vmin=sigma_min, vmax=sigma_max)
        ax.set_xlabel(self.xlab)
        ax.set_ylabel(self.ylab)
        ax.axis('equal')
        ax.grid()
        plt.colorbar(sc)
        plt.show()
    
    def interpolate(self, val1, val2, method='linear'):
        stress = griddata(self.points, self.stresses, (val1, val2), method=method)
        # if math.isnan(stress):
        #     print('nan')
        return stress
    
    def max_stress(self) -> float:
        return max(self.stresses)
