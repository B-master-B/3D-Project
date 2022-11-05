import csv
import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class StressInterpolator:
    def __init__(self, filename):
        with open(filename, newline='') as csvfile:
            csvfile.readline()
            csvreader = csv.reader(csvfile, delimiter='\t')
            self.npoint = max(int(row[0]) for row in csvreader)
            self.points = np.empty([self.npoint, 3])
            self.stresses = np.empty(self.npoint)
            csvfile.seek(0)
            next(csvreader) # skip first row (header)
            for row in csvreader:
                id = int(row[0])
                self.points[id - 1, 0] = float(row[1].replace(',','.'))
                self.points[id - 1, 1] = float(row[2].replace(',','.'))
                self.points[id - 1, 2] = float(row[3].replace(',','.'))
                self.stresses[id - 1] = float(row[4].replace(',','.'))
    
    def show(self, view3d = True, plane = 'xy', offset = 0.0, range = 1.0, s = 1.0, alpha = 1.0):
        fig = plt.figure()
        if view3d:
            ax = fig.add_subplot(projection='3d')
            ax.scatter(self.points[:, 0], self.points[:, 1], self.points[:, 2],
                s=s, alpha=alpha, c=self.stresses, cmap=cm.jet)
            ax.set_xlabel('X')
            ax.set_ylabel('Y')
            ax.set_zlabel('Z')
        else:
            ax = fig.add_subplot()
            match plane:
                case 'xy':
                    col1 = 0
                    col2 = 1
                    col3 = 2
                    ax.set_xlabel('X')
                    ax.set_ylabel('Y')
                case 'yz':
                    col1 = 1
                    col2 = 2
                    col3 = 0
                    ax.set_xlabel('Y')
                    ax.set_ylabel('Z')
                case 'xz':
                    col1 = 0
                    col2 = 2
                    col3 = 1
                    ax.set_xlabel('X')
                    ax.set_ylabel('Z')
                case _:
                    raise ValueError(f"Invalid plane '{plane}', should be 'xy', 'yz' or 'xz'.")

            min3 = offset - range/2.0
            max3 = offset + range/2.0
            ind_in = (self.points[:, col3] >= min3) & (self.points[:, col3] <= max3)
            ax.scatter(self.points[ind_in, col1], self.points[ind_in, col2],
                s=s, alpha=alpha, c=self.stresses[ind_in], cmap=cm.jet)
        
        ax.axis('equal')
        ax.grid()
        plt.show()
    
    def interpolate(self, x, y, z, method='linear'):
        return griddata(self.points, self.stresses, (x, y, z), method=method)
