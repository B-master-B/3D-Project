# %%
from gcodeparser import GcodeParser
import re
from copy import deepcopy
import matplotlib.pyplot as plt


# Parameters
segmentLength = 1.0 # in [mm]

with open('etest.gcode', 'r') as f:
  gcode = f.read()
lines = GcodeParser(gcode, True).lines

inInfill = False
retraction = False
printing = False

prevX = -9999.9
prevY = -9999.9
prevE = 0.0
prevEnew = 0.0
p = -9999.9

for line in lines:
    if line.command[0] == ";" and line.comment.startswith("@AreaBegin \"Infill\""):
        inInfill = not inInfill
        # match = re.search("Z([\d.]+)", line.comment)
        # z = float(match.groups()[0]) # layer z coordinate
        # p = 1 - 0.25*(z - 1) # extrusion percentage
        continue
    if not inInfill:
        continue
    if line.command_str == "G92": # set E parameter to the defined value
        prevE = line.params['E']
        prevEnew = line.params['E']
        continue

    if line.command_str == 'G1':
        E = line.params['E']
        deltaE = E - prevE
        prevE = E
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
                p = (prevX - 170.0)/50.0
                deltaEnew = deltaE * p
        
        # if printing:
        #     endX = line.params['X']
        #     endY = line.params['Y']
        #     # we have to implement segmentation here
        #     # totalLength = norm([endX, endY] - [prevX, prevY])
        #     # ...

        # else: # retraction or after retraction command
        #     Enew = prevEnew + deltaEnew
        #     prevEnew = Enew
        #     line.update_param('E', round(Enew, 5))

        # this should be deleted when segmentation is implemented:
        Enew = prevEnew + deltaEnew
        prevEnew = Enew
        line.update_param('E', round(Enew, 5))
        # line.comment = f'prevX = {prevX}; p = {p}'
    
    if line.command_str == 'G0' or line.command_str == 'G1':
        if 'X' in line.params.keys():
            prevX = line.params['X']
        if 'Y' in line.params.keys():
            prevY = line.params['Y']

with open('etest_mod.gcode', 'w') as f:
    for line in lines:
        f.write(f"{line.gcode_str}\n")

# %%
