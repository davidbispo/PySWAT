# -*- coding: utf-8 -*-
"""
Created on Sun Oct  7 22:50:26 2018

@author: David Bispo
"""
import matplotlib.pyplot as plt
from matplotlib import cm
print(cm.jet(0))


import numpy as np
a = np.arange(256).reshape(16,16)
plt.imshow(a)

aColor = np.linspace(0,255,3)