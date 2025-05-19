"""
    * Lissa Guirau Kawasaki, Theo Okagawa Rodrigues.
    * Algoritmos Genéticos_TSP - Caixeiro viajante.
    * INTELIGENCIA ARTIFICIAL - UNIVERSIDADE ESTADUAL DO PARANÁ.
"""

import tsplib95, random, math, numpy, time, argparse, sys

instancia = None
cidades = []
cidadesNum = 0

def carregar_instancia(intance_path):
    global instancia, cidades, cidadesNum
    try:
        instancia = tsplib95.load(intance_path)
        cidades = list(instancia.get_nodes())
        cidadesNum = len(cidades)
        return True
    except Exception as e: 
        file=sys.stderr
        return False
    
def criar_rota():
    if not cidades:
        print("Lista de cidades não inicializada.")
    rota = list(cidades)
    random.shuffle(rota)
    return rota

def criar_população(tamanhoPopulaçao):
    populacao = []
    for _ in range (tamanhoPopulaçao):
        populacao.append(criar_rota())
    return populacao 

def calcular_distancia(rota):
    if not instancia or cidadesNum == 0:
        print("Sem instâncias ou cidades.")
    distanciaTotal = 0
    for i in range(cidadesNum):
        cidadeAtual = rota[i]
        cidadeProx = rota[(i + 1) % len(rota)]
        distanciaTotal += instancia.get_weight(cidadeAtual, cidadeProx)
    return distanciaTotal

def calcular_fitness(rota):
    distancia = calcular_distancia(rota)
    return 1 / distancia

def roleta_selecao(populacao, valorFitness): 
    fitnessTotal = sum(valorFitness)
    if fitnessTotal == 0:
        return random.choice(populacao)
    
    probabilidade = [fitness / fitnessTotal for fitness in valorFitness]
    escolha = random.uniform(0,1)
    atual = 0
    for i, individual in enumerate(populacao):
        atual += probabilidade[i]
        if atual > escolha:
            return individual
    return populacao[-1]

def crossover(pai1, pai2, probabilidade):
    if random.random() > probabilidade:
        return pai1[:], pai2[:]

    tamanho = len(pai1)
    inicio = random.randint(0, tamanho - 2)
    fim = random.randint(inicio + 1, tamanho - 1)

    def ox(fonte1, fonte2):
        filho = [None] * tamanho
        # Copia o segmento do pai
        filho[inicio:fim+1] = fonte1[inicio:fim+1]
        # Preenche o restante com a ordem do outro pai, pulando os duplicados
        pos = (fim + 1) % tamanho
        for gene in fonte2:
            if gene not in filho:
                filho[pos] = gene
                pos = (pos + 1) % tamanho
        return filho

    return ox(pai1, pai2), ox(pai2, pai1)
