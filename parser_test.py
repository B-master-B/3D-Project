from gcodeparser import GcodeParser

# open gcode file and store contents as variable
with open('pyramid.gcode', 'r') as f:
  gcode = f.read()

lines = GcodeParser(gcode).lines    # get parsed gcode lines
print('first G-code line is parsed as:', lines[0])

# convert back to string
print('original G-code string was:', lines[0].gcode_str)