def extrusionRatio(x, y, z):
    xmin = 170
    xmax = 220
    ymin = 100
    ymax = 150

    pedge = 1.0
    pinner = 0.5
    distmax = 20

    dist = min(x - xmin, xmax - x, y - ymin, ymax - y, distmax)
    return pedge + (pinner - pedge)*dist/distmax
