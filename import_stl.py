from stl import mesh

m = mesh.Mesh.from_file('RESULTS\\biax\\Equiv_stress_1MPA.stl')

print(m.points[0])
