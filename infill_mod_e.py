# %%
from gcodeparser import GcodeParser
import re
from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
import math

# Parameters
segmentMaxLength = 1.0 # in [mm]

directory = 'D:\\OneDrive - Budapesti Műszaki és Gazdaságtudományi Egyetem\\Felevek\\2022-2023-1\\Teamwork project\\projects\\'
filename = 'segtest'
filenameIn = f'{directory}{filename}.gcode'
filenameOut = f'{directory}{filename}_mod.gcode'

with open(filenameIn, 'r') as f:
  gcode = f.read()
linesIn = GcodeParser(gcode, True).lines

inInfill = False
retraction = False
printing = False

# Initialize loop variables
prevX = 0.0
prevY = 0.0
F = 0.0
E = 0.0
Enew = 0.0
p = 0.0

with open(filenameOut, 'w') as f:
    for line in linesIn:
        if line.command[0] == ";" and line.comment.startswith("@AreaBegin \"Infill\""):
            inInfill = not inInfill
            continue
        if not inInfill:
            continue
        if line.command_str == "G92": # set E parameter to the defined value
            E = line.params['E']
            Enew = line.params['E']
            continue

        if line.command_str == 'G1':
            deltaE = line.params['E'] - E
            E = line.params['E']
            if deltaE < 0: # retraction -> we don't modify the deltaE value
                retraction = True
                printing = False
                deltaEnew = deltaE
            else: # deltaE > 0
                if retraction: # after retraction -> we don't modify the deltaE value
                    retraction = False
                    printing = False
                    deltaEnew = deltaE
                else: # extrusion -> we modify the deltaE value according to the p value
                    printing = True
            
            if printing:
                if 'X' in line.params.keys():
                    endX = line.params['X']
                if 'Y' in line.params.keys():
                    endY = line.params['Y']
                
                # segmentation of big lines
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
                    # determine p(actMidPos) fcn.
                    Enew += deltaEsegment*p
                    command = f'G1 X{actEndPos[0]} Y{actEndPos[1]} E{Enew} F{F}\n'
                    f.write(command)
                continue
            else: # retraction or after retraction command
                Enew += deltaEnew
                line.update_param('E', round(Enew, 5))
        
        f.write(line.gcode_str + '\n')
        
        if line.command_str == 'G0' or line.command_str == 'G1':
            if 'X' in line.params.keys():
                prevX = line.params['X']
            if 'Y' in line.params.keys():
                prevY = line.params['Y']
            if 'F' in line.params.keys():
                F = line.params['F']

# %%
