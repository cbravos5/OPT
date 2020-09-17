import math 
import copy
import numpy as np
import time

#retira todas as dependencias do nodo i 
def setDepNone(matrix_dependency,i):
    for j in range(n):
        matrix_dependency[i][j] = False
    

#funcao checa a existencia de dependencia do nodo i
def dep_check(matrix_dependency,i):
    for j in range(n):
        if matrix_dependency[j][i] == True:
            return True
    return False

def Init_bound():
    act_bound = 0
    for i in range(n): 
        act_bound += (Min1(matrix_time, i) + Min2(matrix_time, i)) 
    return act_bound

def copy2Final(act_path): 
    final_path[:n + 1] = act_path[:] 
    final_path[n] = act_path[0] 

# funcao que retorna o primeiro menor tempo de percurso para o nodo i  
def Min1(matrix_time, i): 
    fst = inf 
    for j in range(n): 
        if i == j: 
            continue
        if matrix_time[i][j] < fst: 
            fst = matrix_time[i][j] 
  
    return fst
  
# funcao que retorna o segundo menor tempo de percurso para o nodo i
def Min2(matrix_time, i): 
    fst = inf
    scd = inf
    for j in range(n): 
        if i == j: 
            continue
        if matrix_time[i][j] < fst: 
            fst = matrix_time[i][j] 
  
        elif matrix_time[i][j] < scd: 
            scd = matrix_time[i][j] 
  
    return scd 
  
# funcao com chamada recursiva interna que recebe a matriz de tempos, a matriz de dependencias,
# o limitante atual, a soma dos tempos atual, quantos nodos ja foram percorridos(lvl)
# a ordem em que os nodos foram percorridos ate o momento
# e quais nodos ja foram visitados
def BP_OR(matrix_time, matrix_dependency, act_bound, act_time,  
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
    for i in range(n): 
          
        #se existe um caminho para o nodo entao o tempo atual eh acrescentado
        #um novo bound eh calculado e se for menor que o melhor tempo atual
        #mais um ramo eh criado, caso contrario a arvore eh "podada"
        if (matrix_time[act_path[lvl-1]][i] != 0 and visited[i] == False and dep_check(matrix_dependency,i) == False):
            temp = act_bound 
            backup_visited = copy.deepcopy(visited)
            act_time += matrix_time[act_path[lvl - 1]][i] 
            
            #caso esteja saindo de casa o calculo do bound eh diferente
            if lvl == 1: 
                act_bound -= ((Min1(matrix_time, act_path[lvl - 1]) + 
                                Min1(matrix_time, i)) / 2) 
            else: 
                act_bound -= ((Min2(matrix_time, act_path[lvl - 1]) +
                                 Min1(matrix_time, i)) / 2) 
  
            #bound atual + tempo para chegar ate nodo i deve ser menor que o melhor tempo
            if act_bound + act_time < opt_time:
                new_dep = copy.deepcopy(matrix_dependency)
                setDepNone(new_dep,i)
                act_path[lvl] = i 
                visited[i] = True
                   
                BP_OR(matrix_time, new_dep, act_bound, act_time,  
                       lvl + 1, act_path, visited) 
  
            #reset de variaveis para teste de outro nodo
            act_time -= matrix_time[act_path[lvl - 1]][i] 
            act_bound = temp 
  
            visited = backup_visited
  

 
# leitura do numero de locais e numero de dependencias
n,OR = input().split(' ')
n = int(n) + 1
OR = int(OR)

#leitura da matriz com os tempos de deslocamento
matrix_time = list()

for i in range(n):
    entries = list(map(int, input().split()))
    matrix_time.append(entries)

matrix_time = np.array(matrix_time)

#leitura das dependencias e da criacao da matriz de dependencias
matrix_dependency = [[False for x in range(n)] for y in range(n)]

for i in range(OR):
    before,after = map(int, input().split())
    matrix_dependency[before][after] = True

matrix_dependency = np.array(matrix_dependency)

#atribuicoes de variaveis
inf = float('inf') 
  
opt_time = inf 

final_path = [None] * (n + 1) 

act_path = [-1] * (n + 1) #caminho atual
act_path[0] = 0 
  
visited = [False] * n #nodos visitados  
visited[0] = True 

act_bound = Init_bound() #calculo do bound inicial
act_bound = math.ceil(act_bound / 2) #teto de bound/2

nodes = 0

start = int(round(time.time() * 1000))
BP_OR(matrix_time, matrix_dependency, act_bound, 0, 1, act_path, visited) 
end = int(round(time.time() * 1000))
  
print(opt_time)
for i in range(1,n):
    print(final_path[i])
print("\n\n\n\n")
print(nodes," nodes")
print((end-start)," ms")





    