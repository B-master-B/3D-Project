from infill_mod_e import modify_infill
from extrusionRatioLinear import extrusionRatioLinear
from extrusionRatioConst import extrusionRatioConst
from StressInterpolator2D import StressInterpolator2D
from ExtrusionRatioMapper2D import ExtrusionRatioMapper2D

# directory = 'D:\\OneDrive - Budapesti Műszaki és Gazdaságtudományi Egyetem\\Felevek\\2022-2023-1\\Teamwork project\\projects\\'
directory = 'C:\\Users\\Abel\\OneDrive - Budapesti Műszaki és Gazdaságtudományi Egyetem\\Felevek\\2022-2023-1\\Teamwork project\\projects\\'
filename = 'rombusz_d50'
filenameIn = f'{directory}{filename}.gcode'
filenameOut = f'{directory}{filename}_mod.gcode'

p0 = 0.5 # [1]
p1 = 0.05 # [1/MPa]

offsets = (195.0, 125.0, 0.0)

interpolator = StressInterpolator2D('RESULTS\\rombusz_equiv_stress_2D_15MPa.txt', plane='xy')
mapper = ExtrusionRatioMapper2D(interpolator, offsets, plane='xy')
mapper.config_linear(p0, p1)

modify_infill(filenameIn, filenameOut, mapper.map_linear)
