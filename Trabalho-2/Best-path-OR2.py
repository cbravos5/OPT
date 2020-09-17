import math 
import copy
import numpy as np
import time


def setDepNone(matrix_dependency,i):
    for j in range(n):
        matrix_dependency[i][j] = False

def dep_check(matrix_dependency,i):
    for j in range(n):
        if matrix_dependency[j][i] == True:
            return True
    return False

def copy2Final(act_path): 
    final_path[:n + 1] = act_path[:] 
    final_path[n] = act_path[0] 

class Reduce:
	def __init__(self,cost):
	    self.cost = cost
	    self.red_matrix = []

	def set_red_matrix(self,reduced_matrix):
		self.red_matrix = copy.deepcopy(reduced_matrix)


def Min1(matrix_time, i): 
    fst = inf 
    for j in range(n): 
        if i == j: 
            continue
        if matrix_time[i][j] < fst: 
            fst = matrix_time[i][j] 
  
    return fst

def Min_column(matrix_time,i):
	fst = inf 
	for j in range(n):
		if i == j:
			continue
		if matrix_time[j][i] < fst:
			fst = matrix_time[j][i]

	return fst

def Init_reduced_array(cost,matrix_time):
	reduced = []
	reduced.append(Reduce(cost))
	reduced[0].set_red_matrix(matrix_time)
	for i in range(1,n):
		reduced.append(Reduce(0))
	return reduced



def Get_reduced_cost(matrix_time):
	cost = 0
	minimum = 0
	for i in range(n):
		minimum = Min1(matrix_time,i)
		if (minimum != inf and minimum != 0):
			for j in range(n):
				matrix_time[i][j] -= minimum
			cost += minimum

	for i in range(n):
		minimum = Min_column(matrix_time,i)
		if (minimum != inf and minimum != 0):
			for j in range(n):
				matrix_time[j][i] -= minimum
			cost += minimum	

	return cost

def Set_infinity(matrix_time,i,j):
	for k in range(n):
		matrix_time[i][k] = inf
		matrix_time[k][j] = inf
	matrix_time[j][0] = inf

	return matrix_time


def BP_OR2(matrix_time,matrix_dependency,cost,lvl,visited,act_path,reduced_matrixes):
	global opt_time
	global nodes
	nodes += 1

	if lvl == n:
		if cost < opt_time:
			opt_time = cost
			copy2Final(act_path)
		return

	backup_visited = copy.deepcopy(visited)
	less_cost = inf
	for i in range(n):

		if (visited[i] == False and dep_check(matrix_dependency,i) == False):
			reduced_matrixes[i].red_matrix = Set_infinity(copy.deepcopy(matrix_time),act_path[lvl-1],i)
			reduced_matrixes[i].cost = Get_reduced_cost(reduced_matrixes[i].red_matrix)
			reduced_matrixes[i].cost += cost + matrix_time[act_path[lvl-1]][i]
			if reduced_matrixes[i].cost < less_cost:
				less_cost = reduced_matrixes[i].cost

			if (reduced_matrixes[i].cost < opt_time):
				new_dep = copy.deepcopy(matrix_dependency)
				setDepNone(new_dep,i)
				act_path[lvl] = i 
				visited[i] = True
				BP_OR2(reduced_matrixes[i].red_matrix,new_dep,reduced_matrixes[i].cost,
						lvl+1,visited,act_path,copy.deepcopy(reduced_matrixes))
				visited = backup_visited














inf = float('inf')

# leitura do numero de locais e numero de dependencias
n,OR = input().split(' ')
n = int(n) + 1
OR = int(OR)

#leitura da matriz com os tempos de deslocamento
matrix_time = list()

for i in range(n):
    entries = list(map(float, input().split()))
    matrix_time.append(entries)

matrix_time = np.array(matrix_time)

##################################
#seta todos os zeros para infinito
##################################
for i in range(n):
	for j in range(n):
		if matrix_time[i][j] == 0:
			matrix_time[i][j] = inf





#leitura das dependencias e da criacao da matriz de dependencias
matrix_dependency = [[False for x in range(n)] for y in range(n)]

for i in range(OR):
    before,after = map(int, input().split())
    matrix_dependency[before][after] = True

matrix_dependency = np.array(matrix_dependency)


cost = Get_reduced_cost(matrix_time)

opt_time = inf

final_path = [None] * (n + 1) 

act_path = [-1] * (n + 1) #caminho atual
act_path[0] = 0 
  
visited = [False] * n #nodos visitados  
visited[0] = True

nodes = 0

reduced_matrixes = Init_reduced_array(cost,matrix_time)

start = int(round(time.time() * 1000))
BP_OR2(matrix_time,matrix_dependency,cost,1,visited,act_path,reduced_matrixes)
end = int(round(time.time() * 1000))

print(opt_time)
for i in range(1,n):
    print(final_path[i])
print("\n\n")
print(nodes," nodes")
print((end-start)," ms")