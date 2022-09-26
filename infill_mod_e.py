# %%
from gcodeparser import GcodeParser
import re
import matplotlib.pyplot as plt

with open('1d_piskota_infill_cross.gcode', 'r') as f:
  gcode = f.read()
lines = GcodeParser(gcode, True).lines

inInfill = False
afterRetraction = False

prevE = 0
prevEnew = 0

Epars = []

for line in lines:
    if line.command[0] == ";" and line.comment.startswith("@AreaBegin \"Infill\""):
        inInfill = not inInfill
        match = re.search("Z([\d.]+)", line.comment)
        z = float(match.groups()[0]) # layer z coordinate
        p = 1 - 0.25*(z - 1) # extrusion percentage
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
            afterRetraction = True
            deltaEnew = deltaE
        else: # deltaE > 0
            if afterRetraction: # after retraction -> we don't modify the deltaE value
                afterRetraction = False
                deltaEnew = deltaE
            else: # extrusion -> we modify the deltaE value according to the p value
                deltaEnew = deltaE * p
        
        Enew = prevEnew + deltaEnew
        prevEnew = Enew
        line.update_param('E', Enew)

with open('1d_piskota_infill_cross_mod.gcode', 'w') as f:
    for line in lines:
        f.write(f"{line.gcode_str}\n")

# %%
