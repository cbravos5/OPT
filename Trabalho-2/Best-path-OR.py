#!/usr/bin/python3
import math 
import copy
import numpy as np
import time
import sys

#########################################################################
#retira todas as dependencias do nodo i 
def setDepNone(matrix_dependency,i):
    for j in range(n):
        matrix_dependency[i][j] = False
#########################################################################   

#########################################################################
#funcao checa a existencia de dependencia do nodo i
def dep_check(matrix_dependency,i):
    for j in range(n):
        if matrix_dependency[j][i] == True:
            return True
    return False
#########################################################################

#########################################################################
#funcao inicia os bounds de BP-OR1
def Init_bound():
    act_bound = 0
    if n == 2:
        act_bound += Min1(matrix_time,0) + Min1(matrix_time,1)
    else:
        for i in range(n):
            act_bound += (Min1(matrix_time, i) + Min2(matrix_time, i)) 
    return act_bound
#########################################################################

#########################################################################
#funcao copia o caminho atual para o caminho final
def copy2Final(act_path): 
    final_path[:n + 1] = act_path[:] 
    final_path[n] = act_path[0] 
#########################################################################

#########################################################################
# funcao que retorna o primeiro menor tempo de percurso para o nodo i  
def Min1(matrix_time, i): 
    fst = inf 
    for j in range(n): 
        if i == j: 
            continue
        if matrix_time[i][j] < fst: 
            fst = matrix_time[i][j] 
  
    return fst
#########################################################################

######################################################################### 
# funcao que retorna o segundo menor tempo de percurso para o nodo i
def Min2(matrix_time, i): 
    fst = inf
    scd = inf
    for j in range(n): 
        if i == j: 
            continue
        if matrix_time[i][j] < fst:
            scd = fst 
            fst = matrix_time[i][j]

  
        elif matrix_time[i][j] < scd: 
            scd = matrix_time[i][j] 
  
    return scd 
#########################################################################

#########################################################################  
# funcao com chamada recursiva interna que recebe a matriz de tempos, a matriz de dependencias,
# o limitante atual, a soma dos tempos atual, quantos nodos ja foram percorridos(lvl)
# a ordem em que os nodos foram percorridos ate o momento
# e quais nodos ja foram visitados
def BP_OR1(matrix_time, matrix_dependency, act_bound, act_time,  
              lvl, act_path, visited):
    global opt_time
    global nodes
    nodes +=1
    #base da recurssao 
    if lvl == n: 
          
        #caso exista um caminho para a casa entao o tempo e somado
        #e caso seja menor que a melhor caminho encontrado até agora
        #opt_time é substituido
        if matrix_time[act_path[lvl - 1]][act_path[0]] != 0: 
              
            # curr_res has the total weight 
            # of the solution we got 
            curr_res = act_time + matrix_time[act_path[lvl - 1]][act_path[0]] 
            if curr_res < opt_time: 
                copy2Final(act_path) 
                opt_time = curr_res 
        return
  
    #busca um caminho para todas as opcoes possiveis de nodos
    backup_path = copy.deepcopy(act_path)
    for i in range(n): 
          
        #se existe um caminho para o nodo entao o tempo atual eh acrescentado
        #um novo bound eh calculado e se for menor que o melhor tempo atual
        #mais um ramo eh criado, caso contrario a arvore eh "podada"
        if (matrix_time[act_path[lvl-1]][i] != 0 and visited[i] == False and dep_check(matrix_dependency,i) == False):
            temp = copy.deepcopy(act_bound) 
            act_time += matrix_time[act_path[lvl - 1]][i] 
            
            #caso esteja saindo de casa o calculo do bound eh diferente
            if lvl == 1: 
                act_bound -= ((Min1(matrix_time, act_path[lvl - 1]) + Min1(matrix_time, i)) / 2) 
            else: 
                act_bound -= ((Min2(matrix_time, act_path[lvl - 1]) + Min1(matrix_time, i)) / 2) 
  
            #bound atual + tempo para chegar ate nodo i deve ser menor que o melhor tempo
            if ((math.floor(act_bound) + act_time) < opt_time):
                new_dep = copy.deepcopy(matrix_dependency)
                setDepNone(new_dep,i)
                act_path[lvl] = i 
                visited[i] = True
                
                BP_OR1(matrix_time, new_dep, math.floor(act_bound), act_time,  
                       lvl + 1, act_path, visited) 
  
            #reset de variaveis para teste de outro nodo
            act_time -= matrix_time[act_path[lvl - 1]][i] 
            act_bound = copy.deepcopy(temp) 
  
            visited = [False] * len(visited) 
            for j in range(lvl): 
                if act_path[j] != -1: 
                    visited[act_path[j]] = True
            act_path = copy.deepcopy(backup_path)
#########################################################################

#########################################################################
def Bound_func1(matrix_time,matrix_dependency,act_path,visited):
    global start,end
    start = int(round(time.time() * 1000))
    act_bound = Init_bound() #calculo do bound inicial
    act_bound = math.ceil(act_bound / 2) #teto de bound/2
    BP_OR1(matrix_time, matrix_dependency, act_bound, 0, 1, act_path, visited) 
    end = int(round(time.time() * 1000))

#########################################################################

#########################################################################
#funcao para reduzir as colunas de uma matriz
def Min_column(matrix_time,i):
    fst = inf 
    for j in range(n):
        if i == j:
            continue
        if matrix_time[j][i] < fst:
            fst = matrix_time[j][i]

    return fst
#########################################################################

#########################################################################
#funcao que reduz uma matriz e retorna o custa da reducao
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
#########################################################################

#########################################################################
#funcao que seta M[i][0..n-1] e M[0..n-1][j] para infinito
#e tambem seta M[j][primeiro lugar visitado] para infinito
def Set_infinity(matrix_time,i,j):
    for k in range(n):
        matrix_time[i][k] = inf
        matrix_time[k][j] = inf
    matrix_time[j][0] = inf

    return matrix_time
#########################################################################

#########################################################################
# funcao com chamada recursiva interna que recebe a matriz de tempos(reduzida), a matriz de dependencias,
# o custo atual, quantos nodos ja foram percorridos(lvl)
# a ordem em que os nodos foram percorridos ate o momento(act_path)
# quais nodos ja foram visitados(visited)
# e uma lista de matrizes reduzidas ja inicializadas
def BP_OR2(matrix_time,matrix_dependency,cost,lvl,visited,act_path):
    global opt_time
    global nodes
    nodes += 1

    #final da recursao
    #se custo atual for menor que o melhor custo entao troca
    if lvl == n:
        if cost < opt_time:
            opt_time = cost
            copy2Final(act_path)
        return

    #Calculada a matriz reduzida para todo proximo nodo possivel
    #se o custo for menor que o menor tempo entao avanca para proximo nodo
    red_matrix_act = []
    cost_act = 0
    for i in range(n):

        if (visited[i] == False and dep_check(matrix_dependency,i) == False):
            red_matrix_act = Set_infinity(copy.deepcopy(matrix_time),act_path[lvl-1],i)
            cost_act = Get_reduced_cost(red_matrix_act)
            cost_act += cost + matrix_time[act_path[lvl-1]][i]
            #print(reduced_matrixes[i].cost)

            if (cost_act < opt_time):
                new_dep = copy.deepcopy(matrix_dependency)
                setDepNone(new_dep,i)
                act_path[lvl] = i 
                visited[i] = True
                BP_OR2(red_matrix_act,new_dep,cost_act,
                        lvl+1,visited,act_path)
                visited = [False] * len(visited) 
                for j in range(lvl): 
                    if act_path[j] != -1: 
                        visited[act_path[j]] = True
            red_matrix_act = []
            cost_act = 0
#########################################################################

#########################################################################
def Bound_func2(matrix_time,matrix_dependency,act_path,visited):
    global start,end
    ##################################
    #seta todos os zeros para infinito
    ##################################
    for i in range(n):
        for j in range(n):
            if matrix_time[i][j] == 0:
                matrix_time[i][j] = inf

    cost = Get_reduced_cost(matrix_time)
    start = int(round(time.time() * 1000))
    BP_OR2(matrix_time,matrix_dependency,cost,1,visited,act_path)
    end = int(round(time.time() * 1000))

#########################################################################
# leitura do numero de locais e numero de dependencias
n,OR = input().split(' ')
n = int(n) + 1
OR = int(OR)
#########################################################################

#########################################################################
#leitura da matriz com os tempos de deslocamento
matrix_time = list()

for i in range(n):
    entries = list(map(float, input().split()))
    matrix_time.append(entries)

matrix_time = np.array(matrix_time)
#########################################################################

#########################################################################
#leitura das dependencias e da criacao da matriz de dependencias
matrix_dependency = [[False for x in range(n)] for y in range(n)]

for i in range(OR):
    before,after = map(int, input().split())
    matrix_dependency[before][after] = True

matrix_dependency = np.array(matrix_dependency)
#########################################################################

#########################################################################
#atribuicoes de variaveis
inf = float('inf') 
  
opt_time = inf 

final_path = [None] * (n + 1) 

act_path = [-1] * (n + 1) #caminho atual
act_path[0] = 0 
  
visited = [False] * n #nodos visitados  
visited[0] = True 

nodes = 0

start = 0
end = 0
#########################################################################

#########################################################################
#chamada da funcao especificada na linha de comando
if(len(sys.argv) == 1):
    Bound_func2(matrix_time,matrix_dependency,act_path,visited)
else:
    Bound_func1(matrix_time,matrix_dependency,act_path,visited)
#########################################################################

#########################################################################
#impressao dos resultados
print(int(opt_time))
for i in range(1,n):
    print(final_path[i])
print("\n\n")
print(nodes," nodes")
print((end-start)," ms")
#########################################################################   