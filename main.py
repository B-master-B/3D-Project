from infill_mod_e import modify_infill
from extrusionRatioLinear import extrusionRatioLinear
from extrusionRatioConst import extrusionRatioConst
from StressInterpolator2D import StressInterpolator2D
from ExtrusionRatioMapper2D import ExtrusionRatioMapper2D

# directory = 'D:\\OneDrive - Budapesti Műszaki és Gazdaságtudományi Egyetem\\Felevek\\2022-2023-1\\Teamwork project\\projects\\'
directory = 'C:\\Users\\Abel\\OneDrive - Budapesti Műszaki és Gazdaságtudományi Egyetem\\Felevek\\2022-2023-1\\Teamwork project\\projects\\'
filename = 'Rombusz_MOD2_d50_db3'
filenameIn = f'{directory}{filename}.gcode'
filenameOut = f'{directory}{filename}_mod.gcode'

interpolator = StressInterpolator2D('RESULTS\\rombusz_equiv_stress_2D_15MPa.txt', plane='xy')

# Map 1 (obsolete, not dimensionless)
# p0 = 0.5 # [1]
# p1 = 0.05 # [1/MPa]

# Map 2 (obsolete, not dimensionless)
# p0 = 0.5 # [1]
# p1 = 0.025 # [1/MPa]

# Map 3 (obsolete, not dimensionless)
# p0 = 0.0 # [1]
# p1 = 0.03333 # [1/MPa]

# Map 4
# p0 = 0.5 # [1]
# p1 = 1.5 # [1]

# Map 5
p0 = 0 # [1]
p1 = 2 # [1]

offsets = (195.0, 125.0, 0.0)
periods = (80.0, 10000.0, 10000.0)

mapper = ExtrusionRatioMapper2D(interpolator, offsets, periods, plane='xy')
mapper.config_linear(p0, p1)

modify_infill(filenameIn, filenameOut, mapper.map_linear, pmin=0.5, pmax=2.0)
