#!/usr/bin/python3
from scipy.optimize import linprog
class Hidreletrica:
	def __init__(self,M,F,Ch):
	    self.M = M
	    self.F = F
	    self.Ch = Ch

class Central:
	def __init__(self,D,Id):
	    self.D = D
	    self.Id = Id

class Link:
	def __init__(self,w,Cl,pos):
	    self.w = w
	    self.Cl = Cl
	    self.pos = pos

hdr = []
ctr = []


h,l,R = input().split()
h = int(h)
l = int(l)
R = int(R)

######### vetores de hidreletricas e centrais ###########
for x in range(h):
	M,F,Ch = input().split()
	hdr.append(Hidreletrica(int(M),int(F),int(Ch)))

for x in range(l):
	D = int(input())
	ctr.append(Central(D,x))
########################################################

#################### matriz links ######################
Dist_h = [[0 for x in range(l)] for y in range(h+l)]
m = h

for x in range(h+l):
	n = int(input())
	for y in range(n):
		Id,w,Cl = input().split()
		Dist_h[x][int(Id)-1] = Link(int(w),int(Cl),m)
		m += 1

#########################################################

######################## obj ############################ 
obj = []
for x in range(h):
	obj.append(hdr[x].Ch) #sum(Ch*V)

for x in range(h+l):
	for y in range(l):
		if(Dist_h[x][y] != 0):
			obj.append(Dist_h[x][y].Cl) #sum(Cl*w)
#########################################################

A_ineq = [[0 for x in range(len(obj))] for y in range(h)]
A_eq = [[0 for x in range(len(obj))] for y in range(l+h)]

###################### A_ineq ###########################
k = 0
for x in range(h): #atribuicao inequacoes
	A_ineq[x][k] = hdr[x].F
	k += 1;
#########################################################

##################### A_eq ##############################
for x in range(l):
	for y in range(h+l): #atribuicao tudo que entra
		if (Dist_h[y][x] != 0):
			A_eq[x][Dist_h[y][x].pos] = 1
	for y in range(l): #atribuicao tudo que sai
		if (Dist_h[x+h][y] != 0):
			A_eq[x][Dist_h[x+h][y].pos] = -1

k = 0
for x in range(l,l+h): #atribuicao V - sum(Si)
	A_eq[x][k] = hdr[k].F 
	for y in range(l):
		if(Dist_h[k][y] != 0):
			A_eq[x][Dist_h[k][y].pos] = -1
	k += 1
###########################################################

#################### b_ineq ###############################
b_ineq = []
for x in range(h):
	b_ineq.append(hdr[x].M)
###########################################################

#################### b_eq ###############################
b_eq = []
for x in range(l):
	b_eq.append(ctr[x].D)

for x in range(h):
	b_eq.append(0)

###########################################################

#################### bounds ###############################
bds = []
for x in range(h):
	bds.append((0,R))

for x in range(h+l):
	for y in range(l):
		if(Dist_h[x][y] != 0):
			bds.append((0,Dist_h[x][y].w))
###########################################################


opt = linprog(c=obj, A_ub=A_ineq, b_ub=b_ineq, 
	A_eq=A_eq, b_eq=b_eq, bounds=bds, method='simplex', callback=None, options=None)

for x in range(h):
	print(hdr[x].F*opt.x[x])
for x in range(h,len(obj)):
	print(opt.x[x])