import random
# 5
# 3 4 5 7
# 8 1 2
# 2 3
# 5
# leitura do número de cidades
n = int(input())
# inicialização da matriz de adjacências
matriz_adj = []
for l in range(n):
    linha = []
    for c in range(n):
        linha.append(0)
    matriz_adj.append(linha)
# leitura do triângulo superior da matriz
for l in range(n - 1):
    valores = input().split()
    for c in range(n - 1 - l):
        valor = float(valores[c])
        col = l + 1 + c
        matriz_adj[l][col] = valor
        matriz_adj[col][l] = valor
        
# construir uma solução inicial
def construir_solucao_1():
    solucao = [-1] * n
    visitadas = [False] * n
    atual = random.randrange(0, n)
    solucao[0] = atual
    visitadas[atual] = True
    for i in range(n - 1):
        prox = -1
        menor_custo = 1000000000
        for j in range(n):
            if j == atual or visitadas[j]:
                continue
            if matriz_adj[atual][j] < menor_custo:
                prox = j
                menor_custo = matriz_adj[atual][j]
        solucao[i + 1] = prox
        visitadas[prox] = True
        atual = prox
    return solucao

def construir_solucao_2(inicio):
    solucao = [-1] * n
    visitadas = [False] * n
    atual = inicio
    solucao[0] = atual
    visitadas[atual] = True
    for i in range(n - 1):
        prox = -1
        menor_custo = 1000000000
        for j in range(n):
            if j == atual or visitadas[j]:
                continue
            if matriz_adj[atual][j] < menor_custo:
                prox = j
                menor_custo = matriz_adj[atual][j]
        solucao[i + 1] = prox
        visitadas[prox] = True
        atual = prox
    return solucao

def construir_solucao_3(inicio):
    solucao = [-1] * n
    visitadas = [False] * n
    ultimo = inicio
    primeiro = inicio
    solucao[0] = inicio
    visitadas[inicio] = True
    for i in range(n - 1):
        anterior = -1
        proximo = -1
        menor_custo = 1000000000
        for j in range(n):
            if visitadas[j]:
                continue
            if matriz_adj[j][inicio] < menor_custo:
                anterior = j
                menor_custo = matriz_adj[j][inicio]
        for j in range(n):
            if visitadas[j]:
                continue
            if matriz_adj[ultimo][j] < menor_custo:
                proximo = j
                menor_custo = matriz_adj[ultimo][j]
        if proximo != -1:
            solucao[i + 1] = proximo
            visitadas[proximo] = True
            ultimo = proximo
        else:
            for k in range(i + 1, 0, -1):
                solucao[k] = solucao[k - 1]
            solucao[0] = anterior
            visitadas[anterior] = True
            inicio = anterior
    return solucao

def copia_solucao(origem, destino):
    for i in range(n):
        destino[i] = origem[i]

def troca(solucao_atual, solucao_vizinha, p1, p2):
    copia_solucao(solucao_atual, solucao_vizinha)
    solucao_vizinha[p1] = solucao_atual[p2]
    solucao_vizinha[p2] = solucao_atual[p1]

def busca_em_vizinhanca(solucao_atual, melhor_vizinho):
    '''Busca em vizinhança com operador Troca.'''
    valor_melhor_vizinho = custo_solucao(solucao_atual)
    vizinho = [0] * n
    encontrou_melhoria = False
    for p1 in range(n - 1): # p1 = [0, 1, 2, 3] para n = 5
        for p2 in range(p1 + 1, n): # se p1 = 0, p2 = [1, 2, 3, 4] para n = 5 
            troca(solucao_atual, vizinho, p1, p2)
            custo_vizinho = custo_solucao(vizinho)
            if custo_vizinho < valor_melhor_vizinho:
                valor_melhor_vizinho = custo_vizinho
                copia_solucao(vizinho, melhor_vizinho)
                encontrou_melhoria = True
    return encontrou_melhoria

def busca_local(solucao_atual):
    melhor_vizinho = [0] * n
    solucao_otima_local = [0] * n
    copia_solucao(solucao_atual, solucao_otima_local)
    encontrou_melhoria = True
    while encontrou_melhoria:
        encontrou_melhoria = busca_em_vizinhanca(solucao_otima_local, melhor_vizinho)
        if encontrou_melhoria:
            copia_solucao(melhor_vizinho, solucao_otima_local)
            custo_melhor_vizinho = custo_solucao(melhor_vizinho)
            print("Melhoria: Custo = {:.3f}, Solução: ", custo_melhor_vizinho, end='')
            imprimir_solucao(solucao_otima_local)
    return solucao_otima_local

def imprimir_solucao(solucao):
    for i in range(n):
        print(str(solucao[i]) + ' ', end='')
    print()

def custo_solucao(solucao):
    ultima_cidade = solucao[n - 1]
    primeira_cidade = solucao[0]
    custo = matriz_adj[ultima_cidade][primeira_cidade]
    for i in range(n - 1):
        cidade_atual = solucao[i]
        proxima_cidade = solucao[i + 1]
        custo += matriz_adj[cidade_atual][proxima_cidade]
    return custo

# melhor_solucao = []
# menor_custo = 10000000
# for i in range(n):
#     s = construir_solucao_1(i)
#     imprimir_solucao(s)
#     custo = custo_solucao(s)
#     print(str(custo))
#     if custo < menor_custo:
#         melhor_solucao = s
#         menor_custo = custo
# print("melhor solução: ", end='')
# imprimir_solucao(melhor_solucao)
# print("custo: " + str(menor_custo))
solucao_inicial = construir_solucao_1()
solucao_otima_local = busca_local(solucao_inicial)