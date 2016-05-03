EUR = 1
RSD = 2

lmap = {}
lmap['EUR'] = EUR
lmap['RSD'] = RSD

lrev = dict((y, x) for (x, y) in lmap.items())
