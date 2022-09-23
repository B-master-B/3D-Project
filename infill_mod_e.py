from gcodeparser import GcodeParser
import re

with open('1d_piskota_infill_cross.gcode', 'r') as f:
  gcode = f.read()
lines = GcodeParser(gcode, True).lines

inInfill = False

prevE = 0
prevEnew = 0

for line in lines:
    if line.command[0] == ";" and line.comment.startswith("@AreaBegin \"Infill\""):
        inInfill = not inInfill
        match = re.search("Z([\d.]+)", line.comment)
        z = float(match.groups()[0]) # layer z coordinate
        p = 1 - 0.25*(z - 1) # extrusion percentage
        continue
    if not inInfill:
        continue
    if line.command_str == "G92":
        prevE = line.params['E']
        prevEnew = line.params['E']

    if line.command_str == 'G1':
        E = line.params['E']
        deltaE = E - prevE
        prevE = E
        if deltaE < 0: # retraction -> we don't modify the E value
            deltaEnew = deltaE
        else: # extrusion
            deltaEnew = deltaE * p
        Enew = prevEnew + deltaEnew
        prevEnew = Enew

        line.update_param('E', Enew)

with open('1d_piskota_infill_cross_mod.gcode', 'w') as f:
    for line in lines:
        f.write(f"{line.gcode_str}\n")