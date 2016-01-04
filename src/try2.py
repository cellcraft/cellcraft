import numpy as np
import sys
import pandas as pd


r = np.random.randn(50,3)
print r
H, edges = np.histogramdd(r, bins = (5, 8, 4))
# edges size = num cells = bin+1
H.shape, edges[0].size, edges[1].size, edges[2].size

print H,H.shape,edges[1].size

