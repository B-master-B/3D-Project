from infill_mod_e import modify_infill
from extrusionRatioLinear import extrusionRatioLinear
from extrusionRatioConst import extrusionRatioConst

# directory = 'D:\\OneDrive - Budapesti Műszaki és Gazdaságtudományi Egyetem\\Felevek\\2022-2023-1\\Teamwork project\\projects\\'
directory = 'C:\\Users\\Abel\\OneDrive - Budapesti Műszaki és Gazdaságtudományi Egyetem\\Felevek\\2022-2023-1\\Teamwork project\\projects\\'
filename = 'rombusz_full_diagonal'
filenameIn = f'{directory}{filename}.gcode'
filenameOut = f'{directory}{filename}_mod.gcode'

modify_infill(filenameIn, filenameOut, extrusionRatioLinear)
