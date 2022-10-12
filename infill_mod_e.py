# %%
from gcodeparser import GcodeParser
import re
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import math

from extrusionRatioLinear import extrusionRatioLinear
from extrusionRatioConst import extrusionRatioConst

# Parameters
segmentMaxLength = 1.0 # in [mm]
pmin = 0.5 # minimal extrusion ratio [%]
pmax = 2.0 # maximal extrusion ratio [%]

directory = 'D:\\OneDrive - Budapesti Műszaki és Gazdaságtudományi Egyetem\\Felevek\\2022-2023-1\\Teamwork project\\projects\\'
filename = '1d_piskota_d50_w100_db2'
filenameIn = f'{directory}{filename}.gcode'
filenameOut = f'{directory}{filename}_mod.gcode'

with open(filenameIn, 'r') as f:
  gcode = f.read()
linesIn = GcodeParser(gcode, True).lines

# Initialize loop variables
inInfill = False
retraction = False
printing = False
writeOrigCmd = True

prevX = 0.0
prevY = 0.0
prevZ = 0.0
F = 0
E = 0.0
Enew = 0.0

linesOut = []

for line in linesIn:
    writeOrigCmd = True
    if line.command[0] == ";" and line.comment.startswith("@AreaBegin \"Infill\""):
        inInfill = not inInfill
    if line.command_str == "G92": # set E parameter to the defined value
        E = line.params['E']
        Enew = line.params['E']
    if (line.command_str == 'G0' or line.command_str == 'G1') and 'F' in line.params.keys():
        F = line.params['F']
    if inInfill and line.command_str == 'G1': # printing move in an infill region
        deltaE = line.params['E'] - E
        E = line.params['E']
        if deltaE < 0: # retraction -> we don't modify the deltaE value
            retraction = True
            printing = False
            deltaEnew = deltaE
        else: # deltaE >= 0
            if retraction: # after retraction -> we don't modify the deltaE value
                retraction = False
                printing = False
                deltaEnew = deltaE
            else: # real extrusion -> we modify the deltaE value according to the p value
                printing = True
        
        if printing: # segmentation of big lines
            writeOrigCmd = False

            if 'X' in line.params.keys():
                endX = line.params['X']
            if 'Y' in line.params.keys():
                endY = line.params['Y']
            
            prevPos = np.array([prevX, prevY])
            endPos = np.array([endX, endY])
            diffVector = endPos - prevPos
            totalLength = np.linalg.norm(diffVector)
            noSegments = math.ceil(totalLength / segmentMaxLength)
            segmentLength = totalLength / noSegments
            unitVector = diffVector/totalLength
            segmentVector = unitVector*segmentLength
            actEndPos = prevPos
            deltaEsegment = deltaE / noSegments

            for i in range(noSegments):
                actStartPos = actEndPos
                actMidPos = actStartPos + segmentVector/2
                actEndPos = actStartPos + segmentVector
                p = extrusionRatioConst(actMidPos[0], actMidPos[1], prevZ) # extrusion percentage
                p = min(p, pmax)
                p = max(p, pmin)
                Enew += deltaEsegment*p
                command = f'G1 X{actEndPos[0]:.5f} Y{actEndPos[1]:.5f} E{Enew:.5f} F{F:d}\n'
                linesOut.append(command)
        else: # retraction or after retraction command
            Enew += deltaEnew
            line.update_param('E', round(Enew, 5))
    
    if writeOrigCmd:
        linesOut.append(line.gcode_str + '\n')
    
    if line.command_str == 'G0' or line.command_str == 'G1':
        if 'X' in line.params.keys():
            prevX = line.params['X']
        if 'Y' in line.params.keys():
            prevY = line.params['Y']
        if 'Z' in line.params.keys():
            prevZ = line.params['Z']

with open(filenameOut, 'w') as f:
    f.writelines(linesOut)

# %%
