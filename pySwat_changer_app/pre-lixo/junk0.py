# -*- coding: utf-8 -*-
"""
Created on Sun Sep 30 12:02:20 2018

@author: david
"""

import numpy as np

c = np.array([5,2,8,2,4])    
a = np.array([[ 0,  1,  2,  3,  4],
              [ 5,  6,  7,  8,  9],
              [10, 11, 12, 13, 14],
              [15, 16, 17, 18, 19],
              [20, 21, 22, 23, 24]])

i = np.argsort(c)
a = a[:,i]