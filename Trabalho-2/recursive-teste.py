import copy
import numpy as np

matrix = [[0, 0, 0, 0], 
       [0, 0, 0, 0], 
       [0, 0, 0, 0], 
       [0, 0, 0, 0]] 

def recurse(m,i):
	print(i)
	print(m)
	if(i == 4):
		return
	if (i % 2 == 0):
		m[i][i] = 1
	recurse(copy.deepcopy(m),i + 1)
	print("return")
	print(m)

matrix = np.array(matrix)
recurse(matrix,0)
